#!/usr/bin/env python3
"""
Asgard CLI - Trade leveraged positions on Solana
"""

import os
import sys
import json
import argparse
import requests

BASE_URL = "https://v2-ultra-edge.asgard.finance/margin-trading"

PROTOCOLS = {
    "marginfi": 0,
    "kamino": 1,
    "solend": 2,
    "drift": 3
}


def get_headers():
    headers = {"Content-Type": "application/json"}
    api_key = os.environ.get("ASGARD_API_KEY")
    if api_key:
        headers["X-API-Key"] = api_key
    return headers


def api_get(endpoint, params=None):
    resp = requests.get(f"{BASE_URL}{endpoint}", headers=get_headers(), params=params)
    resp.raise_for_status()
    return resp.json()


def api_post(endpoint, data):
    resp = requests.post(f"{BASE_URL}{endpoint}", headers=get_headers(), json=data)
    resp.raise_for_status()
    return resp.json()


def parse_pair(pair: str) -> tuple:
    """Parse 'SOL/USDC' into ('SOL', 'USDC')"""
    parts = pair.upper().split("/")
    if len(parts) != 2:
        raise ValueError(f"Invalid pair format: {pair}. Use TOKEN_A/TOKEN_B")
    return parts[0], parts[1]


def cmd_markets(args):
    """Get available trading markets"""
    result = api_get("/markets")
    print(json.dumps(result, indent=2))


def cmd_simulate_open(args):
    """Simulate opening a position"""
    token_a, token_b = parse_pair(args.pair)
    result = api_post("/create-position-simulate", {
        "walletAddress": args.wallet,
        "tokenA": token_a,
        "tokenB": token_b,
        "direction": args.direction,
        "collateralAmount": args.collateral,
        "leverage": args.leverage,
        "lendingProtocol": PROTOCOLS.get(args.protocol, 1)
    })
    print(json.dumps(result, indent=2))


def cmd_open(args):
    """Create transaction to open a position"""
    token_a, token_b = parse_pair(args.pair)
    result = api_post("/create-position", {
        "walletAddress": args.wallet,
        "tokenA": token_a,
        "tokenB": token_b,
        "direction": args.direction,
        "collateralAmount": args.collateral,
        "leverage": args.leverage,
        "lendingProtocol": PROTOCOLS.get(args.protocol, 1)
    })
    print(json.dumps(result, indent=2))


def cmd_simulate_close(args):
    """Simulate closing a position"""
    result = api_post("/close-position-simulate", {
        "walletAddress": args.wallet,
        "positionAddress": args.position
    })
    print(json.dumps(result, indent=2))


def cmd_close(args):
    """Create transaction to close a position"""
    result = api_post("/close-position", {
        "walletAddress": args.wallet,
        "positionAddress": args.position
    })
    print(json.dumps(result, indent=2))


def cmd_partial_close(args):
    """Partially close a position (Kamino/Drift only)"""
    result = api_post("/position/partial-close", {
        "walletAddress": args.wallet,
        "positionAddress": args.position,
        "closePercentage": args.percentage
    })
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Asgard Trading CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # markets
    subparsers.add_parser("markets", help="List available markets")

    # simulate-open
    p = subparsers.add_parser("simulate-open", help="Simulate opening a position")
    p.add_argument("--wallet", required=True, help="Wallet address")
    p.add_argument("--pair", required=True, help="Trading pair (e.g., SOL/USDC)")
    p.add_argument("--direction", required=True, choices=["long", "short"])
    p.add_argument("--collateral", required=True, type=float, help="Collateral amount")
    p.add_argument("--leverage", required=True, type=float, help="Leverage multiplier")
    p.add_argument("--protocol", default="kamino", choices=list(PROTOCOLS.keys()))

    # open
    p = subparsers.add_parser("open", help="Open a position")
    p.add_argument("--wallet", required=True)
    p.add_argument("--pair", required=True)
    p.add_argument("--direction", required=True, choices=["long", "short"])
    p.add_argument("--collateral", required=True, type=float)
    p.add_argument("--leverage", required=True, type=float)
    p.add_argument("--protocol", default="kamino", choices=list(PROTOCOLS.keys()))

    # simulate-close
    p = subparsers.add_parser("simulate-close", help="Simulate closing a position")
    p.add_argument("--wallet", required=True)
    p.add_argument("--position", required=True, help="Position address")

    # close
    p = subparsers.add_parser("close", help="Close a position")
    p.add_argument("--wallet", required=True)
    p.add_argument("--position", required=True)

    # partial-close
    p = subparsers.add_parser("partial-close", help="Partially close a position")
    p.add_argument("--wallet", required=True)
    p.add_argument("--position", required=True)
    p.add_argument("--percentage", required=True, type=float, help="0.0 to 1.0")

    args = parser.parse_args()

    commands = {
        "markets": cmd_markets,
        "simulate-open": cmd_simulate_open,
        "open": cmd_open,
        "simulate-close": cmd_simulate_close,
        "close": cmd_close,
        "partial-close": cmd_partial_close,
    }

    try:
        commands[args.command](args)
    except requests.HTTPError as e:
        print(json.dumps({"error": str(e), "response": e.response.text}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
