# Asgard API Reference

Base URL: `https://v2-ultra-edge.asgard.finance/margin-trading`

## Authentication

| Method | Header | Rate Limit |
|--------|--------|------------|
| API Key | `X-API-Key: <key>` | Custom |
| Public | None | 1 req/sec (IP-based) |

Get an API key: [@asgardfi on Telegram](https://t.me/asgardfi)

---

## Endpoints

### GET /markets

Returns available trading strategies.

**Response:**
```json
{
  "markets": [
    {
      "tokenA": "SOL",
      "tokenB": "USDC",
      "protocols": [0, 1, 2, 3],
      "maxLeverage": 5.0,
      "minCollateral": 10
    }
  ]
}
```

---

### POST /create-position-simulate

Preview position creation without executing.

**Request:**
```json
{
  "walletAddress": "...",
  "tokenA": "SOL",
  "tokenB": "USDC",
  "direction": "long",
  "collateralAmount": 100,
  "leverage": 3.0,
  "lendingProtocol": 1
}
```

**Response:**
```json
{
  "entryPrice": 142.50,
  "positionSize": 300,
  "liquidationPrice": 102.30,
  "fees": 0.15,
  "borrowRate": 0.05
}
```

---

### POST /create-position

Build unsigned transaction to open a position.

**Request:** Same as simulate

**Response:**
```json
{
  "transaction": "<base64 encoded unsigned tx>",
  "positionAddress": "..."
}
```

---

### POST /submit-create-position-tx

Submit a signed transaction.

**Request:**
```json
{
  "signedTransaction": "<base64 encoded signed tx>"
}
```

---

### POST /close-position-simulate

Preview closing a position.

**Request:**
```json
{
  "walletAddress": "...",
  "positionAddress": "..."
}
```

**Response:**
```json
{
  "exitPrice": 150.00,
  "pnl": 22.50,
  "pnlPercent": 0.075,
  "fees": 0.12
}
```

---

### POST /close-position

Build unsigned transaction to close.

**Request:** Same as simulate

---

### POST /submit-close-position-tx

Submit signed close transaction.

---

### POST /position/partial-close

Partially close a position (Kamino & Drift only).

**Request:**
```json
{
  "walletAddress": "...",
  "positionAddress": "...",
  "closePercentage": 0.5
}
```

---

## Lending Protocols

| Name | ID | Partial Close Support |
|------|-----|----------------------|
| Marginfi | 0 | No |
| Kamino | 1 | Yes |
| Solend | 2 | No |
| Drift | 3 | Yes |

---

## Direction Mapping

The API abstracts token pairs:
- **Long**: Bullish on tokenA vs tokenB (collateral in tokenB, borrow tokenB to buy tokenA)
- **Short**: Bearish on tokenA vs tokenB (collateral in tokenA, borrow tokenA to sell)

---

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Invalid parameters |
| 401 | Invalid API key |
| 429 | Rate limit exceeded |
| 500 | Server error |

---

## Links

- [GitHub: asgard-finance/api-docs](https://github.com/asgard-finance/api-docs)
- [Asgard Finance](https://asgard.finance)
