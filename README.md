# Asgard Agent Skill

Enable AI agents to trade leveraged positions on Solana via [Asgard Finance](https://asgard.finance).

Built on the [Agent Skills specification](https://agentskills.io) — works with Claude Code, Moltbot, OpenClaw, and other compatible agent frameworks.

## Why?

The internet is going agentic. Protocols that don't expose agent-friendly interfaces will lose volume to those that do. This skill makes Asgard accessible to AI agents, not just humans.

## What Agents Can Do

| Action | Description |
|--------|-------------|
| `markets` | List tradeable pairs, protocols, leverage ranges |
| `simulate-open` | Preview a position before executing |
| `open` | Open a leveraged long/short position |
| `simulate-close` | Preview closing a position |
| `close` | Close a position |
| `partial-close` | Partially close (Kamino/Drift only) |

## Quick Start

### 1. Install

```bash
git clone https://github.com/asgard-finance/asgard-agent-skill.git
cd asgard-agent-skill
pip install requests
```

### 2. Set API Key (optional)

```bash
export ASGARD_API_KEY="your-key"  # Get from @asgardfi on Telegram
```

Public access available at 1 req/sec without a key.

### 3. Test

```bash
python scripts/asgard.py markets
```

## Usage with Agent Frameworks

### Claude Code

```bash
# Copy skill to Claude Code skills directory
cp -r asgard-agent-skill ~/.claude/skills/asgard
```

### Moltbot / OpenClaw

Point your agent to the `SKILL.md` file or import the skill directory.

## Structure

```
asgard-agent-skill/
├── SKILL.md              # Agent instructions (loaded by frameworks)
├── scripts/
│   └── asgard.py         # CLI tool agents invoke
└── references/
    └── API.md            # Detailed API docs
```

## Supported Protocols

| Protocol | Partial Close |
|----------|---------------|
| Marginfi | No |
| Kamino | Yes |
| Solend | No |
| Drift | Yes |

## Example Agent Interaction

**User:** "Open a 3x long on SOL with 50 USDC"

**Agent:**
1. Queries available markets
2. Simulates the trade → "Entry $142.50, liquidation $102.30"
3. Asks for confirmation
4. Returns unsigned transaction for wallet signing

## Links

- [Asgard Finance](https://asgard.finance)
- [API Documentation](https://github.com/asgard-finance/api-docs)
- [Agent Skills Spec](https://agentskills.io)
- Contact: [@asgardfi on Telegram](https://t.me/asgardfi)

## License

MIT
