---
name: asgard
description: Trade leveraged long/short positions on Solana via Asgard Finance. Use when the user wants to open, close, or manage margin positions on SOL, ETH, or other tokens using lending protocols like Kamino, Marginfi, Solend, or Drift.
license: MIT
metadata:
  author: asgard-finance
  version: "0.1.0"
  chain: solana
compatibility: Requires Python 3.8+ with requests library. Requires network access to Asgard API.
allowed-tools: Bash(python:*) Read
---

# Asgard Trading Skill

Trade leveraged positions on Solana internet capital markets.

## Overview

Asgard provides structured products for margin trading on Solana. This skill enables you to:

- **Query** available markets and positions
- **Simulate** trades before execution
- **Execute** leveraged long/short positions
- **Manage** existing positions (partial close, add collateral)

## Authentication

Set the API key in environment (or use public access at 1 req/sec):

```bash
export ASGARD_API_KEY="your-key"
```

Get a key: Contact @asgardfi on Telegram

## Available Actions

### 1. Get Markets

List all tradeable pairs and their parameters:

```bash
python scripts/asgard.py markets
```

Returns: token pairs, supported protocols, leverage ranges, current rates.

### 2. Simulate Opening a Position

Always simulate before executing to show the user projected outcomes:

```bash
python scripts/asgard.py simulate-open \
  --wallet <WALLET_ADDRESS> \
  --pair SOL/USDC \
  --direction long \
  --collateral 100 \
  --leverage 3 \
  --protocol kamino
```

Returns: entry price, liquidation price, position size, fees.

### 3. Open a Position

Build a transaction to open a leveraged position:

```bash
python scripts/asgard.py open \
  --wallet <WALLET_ADDRESS> \
  --pair SOL/USDC \
  --direction long \
  --collateral 100 \
  --leverage 3 \
  --protocol kamino
```

Returns: unsigned transaction (base64) for wallet signing.

### 4. Simulate Closing a Position

Preview the outcome of closing:

```bash
python scripts/asgard.py simulate-close \
  --wallet <WALLET_ADDRESS> \
  --position <POSITION_ADDRESS>
```

Returns: exit price, realized PnL, fees.

### 5. Close a Position

Build a transaction to close:

```bash
python scripts/asgard.py close \
  --wallet <WALLET_ADDRESS> \
  --position <POSITION_ADDRESS>
```

### 6. Partial Close (Kamino/Drift only)

Close a percentage of a position:

```bash
python scripts/asgard.py partial-close \
  --wallet <WALLET_ADDRESS> \
  --position <POSITION_ADDRESS> \
  --percentage 0.5
```

## Workflow

Always follow this pattern:

1. **Query markets** to discover available pairs
2. **Simulate** to show user what will happen
3. **Get user confirmation**
4. **Execute** and return unsigned tx
5. **User signs** in their wallet

## Supported Protocols

| Protocol | ID | Partial Close |
|----------|-----|---------------|
| Marginfi | 0 | No |
| Kamino | 1 | Yes |
| Solend | 2 | No |
| Drift | 3 | Yes |

## Example Conversation

**User**: "Open a 3x long on SOL with 50 USDC"

**Agent**:
1. Calls `markets` to verify SOL/USDC is available
2. Calls `simulate-open` with the parameters
3. Reports: "Entry $142.50, liquidation at $102.30, fees $0.15"
4. Asks: "Proceed?"
5. On confirmation, calls `open` and returns unsigned tx
6. Says: "Please sign this transaction in your wallet"

## Safety Guidelines

- Always simulate before executing
- Cap leverage at 5x for agent-initiated trades
- Require human confirmation before signing
- Never store or request private keys

See [references/API.md](references/API.md) for full API documentation.
