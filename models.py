from typing import Dict, List
from schemas import Bet, Wallet, WalletTransaction

bets: Dict[str, Bet] = {}
wallet: Wallet = Wallet(balance=0.0, transactions=[])
wallet_transactions: Dict[str, WalletTransaction] = {}