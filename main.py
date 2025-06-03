from fastapi import FastAPI, HTTPException, status, Depends, Body, Query
from fastapi.openapi.utils import get_openapi
from typing import List
from schemas import Bet, Wallet, WalletTransaction
from models import bets, wallet, wallet_transactions
from auth import create_access_token, ROLES_PERMISSIONS, get_current_user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Bet Tracker API",
    description="API for Bet Tracker with JWT Auth. Manage bets, wallet, and transactions."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"HTTPBearer": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Permission dependency helpers
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

def require_read(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    return get_current_user(credentials, required_permissions=["READ"])

def require_write(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    return get_current_user(credentials, required_permissions=["WRITE"])

def require_delete(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    return get_current_user(credentials, required_permissions=["DELETE"])

@app.post(
    "/bets",
    response_model=Bet,
    status_code=status.HTTP_201_CREATED,
    tags=["Bets"],
    summary="Create a new bet",
    description="Create a new bet. Requires WRITE permission.",
)
def create_bet(
    bet: Bet,
    user=Depends(require_write)
):
    if bet.id in bets:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bet with this ID already exists.")
    bets[bet.id] = bet
    return bet

@app.get(
    "/bets",
    response_model=List[Bet],
    status_code=status.HTTP_200_OK,
    tags=["Bets"],
    summary="Get all bets",
    description="Get all bets with optional pagination and filtering. Requires READ permission.",
)
def get_bets(
    user=Depends(require_read),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max number of items to return"),
    outcome: str = Query(None, description="Filter by outcome (Won, Lost, Draw, Pending)"),
    type: str = Query(None, description="Filter by type (Winner, Total, Handicap, Other)"),
    favorite: bool = Query(None, description="Filter by favorite (true/false)"),
):
    all_bets = list(bets.values())
    # Filtering
    if outcome is not None:
        all_bets = [b for b in all_bets if b.outcome == outcome]
    if type is not None:
        all_bets = [b for b in all_bets if b.type == type]
    if favorite is not None:
        all_bets = [b for b in all_bets if b.favorite == favorite]
    # Pagination
    return all_bets[skip : skip + limit]

@app.get(
    "/bets/{bet_id}",
    response_model=Bet,
    status_code=status.HTTP_200_OK,
    tags=["Bets"],
    summary="Get a bet by ID",
    description="Get a specific bet by its ID. Requires READ permission.",
)
def get_bet(
    bet_id: str,
    user=Depends(require_read)
):
    bet = bets.get(bet_id)
    if not bet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found.")
    return bet

@app.put(
    "/bets/{bet_id}",
    response_model=Bet,
    status_code=status.HTTP_200_OK,
    tags=["Bets"],
    summary="Update a bet",
    description="Update an existing bet by ID. Requires WRITE permission.",
)
def update_bet(
    bet_id: str,
    bet_update: Bet,
    user=Depends(require_write)
):
    if bet_id not in bets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found.")
    bets[bet_id] = bet_update
    return bet_update

@app.delete(
    "/bets/{bet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Bets"],
    summary="Delete a bet",
    description="Delete a bet by ID. Requires DELETE permission.",
)
def delete_bet(
    bet_id: str,
    user=Depends(require_delete)
):
    if bet_id not in bets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found.")
    del bets[bet_id]
    return

@app.get(
    "/wallet",
    response_model=Wallet,
    status_code=status.HTTP_200_OK,
    tags=["Wallet"],
    summary="Get wallet info",
    description="Get wallet balance and transactions. Requires READ permission.",
)
def get_wallet(
    user=Depends(require_read)
):
    return wallet

@app.get(
    "/wallet/transactions",
    response_model=List[WalletTransaction],
    status_code=status.HTTP_200_OK,
    tags=["Wallet"],
    summary="Get wallet transactions",
    description="Get all wallet transactions with pagination. Requires READ permission.",
)
def get_wallet_transactions(
    user=Depends(require_read),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max number of items to return"),
):
    all_transactions = list(wallet_transactions.values())
    return all_transactions[skip : skip + limit]

@app.get(
    "/wallet/transactions/{transaction_id}",
    response_model=WalletTransaction,
    status_code=status.HTTP_200_OK,
    tags=["Wallet"],
    summary="Get wallet transaction by ID",
    description="Get a specific wallet transaction by ID. Requires READ permission.",
)
def get_wallet_transaction(
    transaction_id: str,
    user=Depends(require_read)
):
    transaction = wallet_transactions.get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")
    return transaction

@app.post(
    "/wallet/transactions",
    response_model=WalletTransaction,
    status_code=status.HTTP_201_CREATED,
    tags=["Wallet"],
    summary="Create wallet transaction",
    description="Create a new wallet transaction. Requires WRITE permission.",
)
def create_wallet_transaction(
    transaction: WalletTransaction,
    user=Depends(require_write)
):
    if transaction.id in wallet_transactions:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Transaction with this ID already exists.")
    wallet_transactions[transaction.id] = transaction
    wallet.transactions.append(transaction)
    if transaction.type == "deposit":
        wallet.balance += transaction.amount
    elif transaction.type == "withdrawal":
        wallet.balance -= transaction.amount
    return transaction

@app.delete(
    "/wallet/transactions/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Wallet"],
    summary="Delete wallet transaction",
    description="Delete a wallet transaction by ID. Requires DELETE permission.",
)
def delete_wallet_transaction(
    transaction_id: str,
    user=Depends(require_delete)
):
    transaction = wallet_transactions.get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")
    wallet.transactions = [t for t in wallet.transactions if t.id != transaction_id]
    if transaction.type == "deposit":
        wallet.balance -= transaction.amount
    elif transaction.type == "withdrawal":
        wallet.balance += transaction.amount
    del wallet_transactions[transaction_id]
    return

@app.post(
    "/token",
    tags=["Auth"],
    summary="Generate JWT token",
    description="Generate a JWT token for a given role. Roles: USER, VISITOR.",
)
def generate_token(
    role: str = Body(default="VISITOR")
):
    if role not in ROLES_PERMISSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
    perms = ROLES_PERMISSIONS[role]
    token_data = {
        "role": role,
        "permissions": perms,
    }
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}