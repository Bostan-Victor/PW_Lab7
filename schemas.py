from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Bet(BaseModel):
    id: str
    date: str
    type: Literal["Winner", "Total", "Handicap", "Other"]
    amount: float
    odds: float
    outcome: Literal["Won", "Lost", "Draw", "Pending"]
    payout: float
    profit: float
    notes: Optional[str] = None
    favorite: bool

class WalletTransaction(BaseModel):
    id: str
    type: Literal["deposit", "withdrawal", "bet", "payout"]
    amount: float
    date: str 
    bet_id: Optional[str] = None

class Wallet(BaseModel):
    balance: float
    transactions: List[WalletTransaction]