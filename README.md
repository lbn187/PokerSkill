# PokerSkill: LLMs Can Play Expert-Level Poker without Training or Solvers

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Paper](https://img.shields.io/badge/arXiv-2026.30094-b31b1b.svg)](https://arxiv.org/abs/2026.30094)

**Authors:** Boning Li, Baoxiang Wang, Longbo Huang  
**Affiliation:** Tsinghua University  
**Email:** li-bn22@mails.tsinghua.edu.cn

---

## Intro

PokerSkill is a training-free and solver-free framework that enables frontier LLMs to play expert-level heads-up no-limit Texas hold'em (HUNL). It uses detailed rule-based poker skills as a structured action-grounding interface for LLMs, requiring zero solver queries at inference time and zero offline learning.

<p align="center">
  <img src="figures/poker_ai_evolution.png" width="80%" alt="Evolution of Poker AI">
</p>

## Results

Against GTOWizard (a state-of-the-art GTO benchmark with AIVAT variance reduction):

| Agent | Method | mbb/hand |
|-------|--------|----------|
| GPT-5.5 XHigh | PokerSkill | -57 ± 21 |
| Claude Opus 4.6 | PokerSkill | -80 ± 29 |
| Claude Opus 4.7 | PokerSkill | -87 ± 64 |
| Rule-based (no LLM) | PokerSkill Only | -132 ± 19 |
| GPT-5.5 XHigh | Default Prompt | -132 ± 25 |
| Claude Opus 4.7 | Default Prompt | -170 ± 28 |
| Claude Opus 4.6 | Default Prompt | -204 ± 44 |

PokerSkill reduces losses by 49–61% compared to default-prompt baselines and outperforms the strong bot Slumbot.

<p align="center">
  <img src="figures/main_results.png" width="70%" alt="Main Results">
</p>

## Quick Start (Docker)

```bash
# Build the image
docker build -t pokerskill-agent .

# Play against GTO Wizard
docker run --rm \
  -e GTO_WIZARD_API_KEY=$GTO_WIZARD_API_KEY \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  pokerskill-agent play --num-hands 100 --model claude-opus-4-6
```

## Local Installation (Linux x86_64 + Python 3.9)

```bash
pip install .
pokerskill-agent --help
```

> The compiled extensions require Linux x86_64 with Python 3.9. For other platforms, use Docker.

## Usage

### Play Against GTO Wizard

```bash
# Claude (default)
pokerskill-agent play --num-hands 5000 --model claude-opus-4-6

# Claude with extended thinking
pokerskill-agent play --num-hands 5000 --model claude-opus-4-6 --thinking-budget 100000

# OpenAI
pokerskill-agent play --num-hands 1000 --model gpt-4o --backend openai

# OpenAI reasoning model
pokerskill-agent play --num-hands 1000 --model o3 --backend openai --thinking-budget 1

# Custom API base URL
pokerskill-agent play --model claude-opus-4-6 --base-url https://your-proxy.com
```

### Baseline Mode (No Skills)

Disable the PokerSkill strategy layers to run a default-prompt baseline:

```bash
pokerskill-agent play --num-hands 1000 --model claude-opus-4-6 --no-skills
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--num-hands, -n` | 100 | Number of hands to play |
| `--model, -m` | claude-opus-4-6 | LLM model name |
| `--backend, -b` | (auto) | claude / openai |
| `--concurrent` | 3 | Concurrent hands |
| `--thinking-budget` | 0 | Extended thinking tokens |
| `--no-skills` | false | Disable PokerSkill (baseline mode) |
| `--output, -o` | results_\<model\>.csv | CSV output path |
| `--base-url` | (default) | LLM API base URL override |
| `--temperature` | 0.3 | LLM temperature |
| `--max-tokens` | 1024 | Max response tokens |

## Environment Variables

| Variable | Required For | Description |
|----------|-------------|-------------|
| `GTO_WIZARD_API_KEY` | Always | GTO Wizard Researcher API key |
| `ANTHROPIC_API_KEY` | Claude backend | Anthropic API key |
| `OPENAI_API_KEY` | OpenAI backend | OpenAI API key |

## Output

CSV file with columns: `hand_id, position, llm_model, method, winnings_bb, aivat_bb, num_decisions, error`

Console output shows running totals and final summary:
```
==================================================
Completed: 5000 | Failed: 3
Total winnings: -430.5 BB
Avg winnings: -0.09 BB/hand
AIVAT: -309.0 BB total, -0.06 BB/hand
==================================================
```

## Architecture

PokerSkill uses a 5-layer priority architecture to construct structured prompts:

| Layer | Scope | Content |
|-------|-------|---------|
| P1 | Always | Game rules, execution framework, output format |
| P2 | Preflop | GTO range guidance for the detected scenario |
| P3 | Postflop | General principles + hand strength evaluation |
| P4 | Postflop | Targeted strategy (ATT/DEF budget, viable options) |
| P5 | River | Bluff/bluff-catch guidelines |

A deterministic context engine analyzes the current game state and retrieves only the relevant fragments from the layered skill library, constraining the LLM's choice to reasonable actions.

<p align="center">
  <img src="figures/overview.png" width="85%" alt="PokerSkill System Overview">
</p>

## Notes

- Supports graceful shutdown via SIGINT/SIGTERM
- API keys are only read from environment variables
- It is not allowed to be used in online poker room

## Human Testing

If you are good at playing poker and are interested in human testing against PokerSkill, please contact me for details.

We are also seeking poker professional players willing to participate in multiplayer poker testing too.

## Citation

```bibtex
@article{li2026pokerskill,
  title={PokerSkill: LLMs Can Play Expert-Level Poker without Training or Solvers},
  author={Li, Boning and Wang, Baoxiang and Huang, Longbo},
  journal={arXiv preprint},
  year={2026}
}
```

## License

This project is licensed under the CC BY-NC 4.0 License (non-commercial use only) - see the [LICENSE](LICENSE) file for details.
