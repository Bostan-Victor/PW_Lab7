from fastapi import FastAPI, HTTPException, status
from typing import List
from schemas import Bet
from models import bets

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