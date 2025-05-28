from fastapi import FastAPI, HTTPException, status
from typing import List
from schemas import Bet, Wallet, WalletTransaction
from models import bets, wallet, wallet_transactions

app = FastAPI()

# Create a new bet
@app.post("/bets", response_model=Bet, status_code=status.HTTP_201_CREATED)
def create_bet(bet: Bet):
    if bet.id in bets:
        raise HTTPException(status_code=400, detail="Bet with this ID already exists.")
    bets[bet.id] = bet
    return bet

# Get all bets
@app.get("/bets", response_model=List[Bet])
def get_bets():
    return list(bets.values())

# Get a specific bet by ID
@app.get("/bets/{bet_id}", response_model=Bet)
def get_bet(bet_id: str):
    bet = bets.get(bet_id)
    if not bet:
        raise HTTPException(status_code=404, detail="Bet not found.")
    return bet

# Update an existing bet
@app.put("/bets/{bet_id}", response_model=Bet)
def update_bet(bet_id: str, bet_update: Bet):
    if bet_id not in bets:
        raise HTTPException(status_code=404, detail="Bet not found.")
    bets[bet_id] = bet_update
    return bet_update

# Delete a bet
@app.delete("/bets/{bet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bet(bet_id: str):
    if bet_id not in bets:
        raise HTTPException(status_code=404, detail="Bet not found.")
    del bets[bet_id]

# Get wallet info
@app.get("/wallet", response_model=Wallet)
def get_wallet():
    return wallet

# Get all wallet transactions
@app.get("/wallet/transactions", response_model=List[WalletTransaction])
def get_wallet_transactions():
    return list(wallet_transactions.values())

# Get a specific wallet transaction by ID
@app.get("/wallet/transactions/{transaction_id}", response_model=WalletTransaction)
def get_wallet_transaction(transaction_id: str):
    transaction = wallet_transactions.get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    return transaction

# Create a new wallet transaction
@app.post("/wallet/transactions", response_model=WalletTransaction, status_code=status.HTTP_201_CREATED)
def create_wallet_transaction(transaction: WalletTransaction):
    if transaction.id in wallet_transactions:
        raise HTTPException(status_code=400, detail="Transaction with this ID already exists.")
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
        raise HTTPException(status_code=404, detail="Transaction not found.")
    wallet.transactions = [t for t in wallet.transactions if t.id != transaction_id]
    if transaction.type == "deposit":
        wallet.balance -= transaction.amount
    elif transaction.type == "withdrawal":
        wallet.balance += transaction.amount
    del wallet_transactions[transaction_id]