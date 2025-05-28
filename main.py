from fastapi import FastAPI, HTTPException, status, Depends, Body
from typing import List, Optional
from schemas import Bet, Wallet, WalletTransaction
from models import bets, wallet, wallet_transactions
from auth import create_access_token, ROLES_PERMISSIONS

app = FastAPI()

# Create a new bet
@app.post("/bets", response_model=Bet, status_code=status.HTTP_201_CREATED)
def create_bet(bet: Bet):
    if bet.id in bets:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bet with this ID already exists.")
    bets[bet.id] = bet
    return bet

# Get all bets
@app.get("/bets", response_model=List[Bet], status_code=status.HTTP_200_OK)
def get_bets():
    return list(bets.values())

# Get a specific bet by ID
@app.get("/bets/{bet_id}", response_model=Bet, status_code=status.HTTP_200_OK)
def get_bet(bet_id: str):
    bet = bets.get(bet_id)
    if not bet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found.")
    return bet

# Update an existing bet
@app.put("/bets/{bet_id}", response_model=Bet, status_code=status.HTTP_200_OK)
def update_bet(bet_id: str, bet_update: Bet):
    if bet_id not in bets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found.")
    bets[bet_id] = bet_update
    return bet_update

# Delete a bet
@app.delete("/bets/{bet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bet(bet_id: str):
    if bet_id not in bets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found.")
    del bets[bet_id]
    return

# Get wallet info
@app.get("/wallet", response_model=Wallet, status_code=status.HTTP_200_OK)
def get_wallet():
    return wallet

# Get all wallet transactions
@app.get("/wallet/transactions", response_model=List[WalletTransaction], status_code=status.HTTP_200_OK)
def get_wallet_transactions():
    return list(wallet_transactions.values())

# Get a specific wallet transaction by ID
@app.get("/wallet/transactions/{transaction_id}", response_model=WalletTransaction, status_code=status.HTTP_200_OK)
def get_wallet_transaction(transaction_id: str):
    transaction = wallet_transactions.get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")
    return transaction

# Create a new wallet transaction
@app.post("/wallet/transactions", response_model=WalletTransaction, status_code=status.HTTP_201_CREATED)
def create_wallet_transaction(transaction: WalletTransaction):
    if transaction.id in wallet_transactions:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Transaction with this ID already exists.")
    wallet_transactions[transaction.id] = transaction
    wallet.transactions.append(transaction)
    if transaction.type == "deposit":
        wallet.balance += transaction.amount
    elif transaction.type == "withdrawal":
        wallet.balance -= transaction.amount
    return transaction

# Delete a wallet transaction
@app.delete("/wallet/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wallet_transaction(transaction_id: str):
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

# Generate a token for a user
@app.post("/token")
def generate_token(
    role: Optional[str] = Body(default="VISITOR"),
    permissions: Optional[List[str]] = Body(default=None)
):
    # Validate role
    if role not in ROLES_PERMISSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
    perms = permissions if permissions is not None else ROLES_PERMISSIONS[role]
    token_data = {
        "role": role,
        "permissions": perms,
    }
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}