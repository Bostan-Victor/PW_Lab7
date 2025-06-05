# Bet Tracker API (Lab 7 - Back-end)

**Author:** Bostan Victor  
**Group:** FAF-222

## Project Description

This project is the back-end API for the Bet Tracker application, created for Web Programming Lab 7. It provides a secure, documented, and efficient REST API for managing sports bets, wallet balances, and transactions, and is designed to integrate with the React front-end from Lab 6.

## Features

- **JWT Authentication & Authorization:**  
  All CRUD operations require a valid JWT token. Tokens encode user roles or permissions and have a short expiration (default: 1 minute for demo, configurable).
- **Role/Permission-based Access:**  
  Endpoints are protected based on user roles (e.g., USER, VISITOR) or permissions (READ, WRITE, DELETE).
- **CRUD API for Bets, Wallet, and Transactions:**  
  - Add, edit, delete, and list bets.
  - Manage wallet balance and transaction history.
- **Pagination & Filtering:**  
  - Bets endpoint supports pagination (`limit`, `skip`) and filtering by outcome, type, and favorite.
- **Swagger UI Documentation:**  
  - Interactive API docs available at `/docs`.
- **/token Endpoint:**  
  - Obtain JWT tokens by POSTing a role (e.g., `{ "role": "USER" }`) to `/token`.
- **CORS Enabled:**  
  - Allows integration with the React front-end running on a different port.

## API Overview

- `POST /token` — Obtain a JWT token for a given role.
- `GET /bets` — List bets (supports pagination and filtering).
- `POST /bets` — Add a new bet.
- `PUT /bets/{bet_id}` — Update a bet.
- `DELETE /bets/{bet_id}` — Delete a bet.
- `GET /wallet` — Get wallet info.
- `GET /wallet/transactions` — List wallet transactions.
- `POST /wallet/transactions` — Add a wallet transaction.
- `DELETE /wallet/transactions/{transaction_id}` — Delete a wallet transaction.

All endpoints (except `/token`) require a valid JWT in the `Authorization: Bearer <token>` header.

## Technologies Used

- **FastAPI** (Python) — REST API framework
- **Pydantic** — Data validation and serialization
- **python-jose** — JWT encoding/decoding
- **Swagger UI** — API documentation (auto-generated)
- **CORS Middleware** — For cross-origin requests from the React front-end

## How to Run

1. **Install dependencies:**
   ```sh
   pip install fastapi uvicorn python-jose[cryptography]
   ```

2. **Start the server:**
   ```sh
   uvicorn main:app --reload
   ```

3. **Access the API docs:**  
   [http://localhost:8000/docs](http://localhost:8000/docs)

4. **Integrate with the React front-end:**  
   - The React app should obtain a JWT from `/token` and send it with all API requests.

## Project Structure

```
main.py              # FastAPI app entry point
models.py            # In-memory data stores
schemas.py           # Pydantic models for Bet, Wallet, Transaction
auth.py              # JWT utilities and dependencies
routes/              # (Optional) Additional route modules
.gitignore
README.md
```

## Integration with Front-end

This API is designed to fully integrate with the [Bet Tracker React app](../6/bet-tracker), replacing IndexedDB with secure, real-time API calls. The front-end authenticates via `/token`, stores the JWT, and uses it for all requests.

