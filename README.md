# PokerSkill: LLMs Can Play Expert-Level Poker without Training or Solvers

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Paper](https://img.shields.io/badge/arXiv-2605.30094-b31b1b.svg)](https://arxiv.org/abs/2605.30094)

**Authors:** Boning Li, Baoxiang Wang, Longbo Huang  
**Affiliation:** Tsinghua University  
**Email:** li-bn22@mails.tsinghua.edu.cn

# 招实习生

我认为PokerSkill方法可直接应用到多人扑克、奥马哈、麻将、斗地主、象棋、围棋、军棋等游戏上。招本科实习生帮忙编写这些相关游戏的Agent和Skill。计算资源、API资源均十分充足。

# 招人类AI测试者

我认为PokerSkill，加上一定程度的对手剥削，能够在无限注单挑德州扑克上达到甚至超过职业牌手的水平。我乐意提供免费的对战API，供较高水平的玩家进行测试。

此外，我们的另一个扑克AI产品可以在2-9人的任意扑克场景下（任意规则、任意筹码量、任意人数、随便limp），给出实时的决策。我们的AI已经显著战胜了多位GPI排名前100的职业牌手，在6人扑克场景下的赢率达到接近百手10个大盲注，胜率两倍于之前发表在Science的多人扑克AI，Pluribus（且该AI只支持一个规则、固定筹码量）。为了提升产品的可靠性，我正在寻找GPI全球排名在最近10年达到过世界前10000的职业牌手进行测试，可提供较为丰厚的测试报酬（联系邮箱：li-bn22@mails.tsinghua.edu.cn）。我的愿景是：当这个产品完成以后，人人都可以低成本地获得高性能决策AI，在线扑克直接灰飞烟灭。

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
# Build the image (Ubuntu 24.04 + CPython 3.12, matching the compiled extensions)
docker build -t pokerskill-agent .

# Print the exact prompt for one decision; needs no API key
docker run --rm pokerskill-agent prompt --state /app/pokerskill_agent/examples/flop_cbet.json

# Play against GTO Wizard
docker run --rm \
  -e GTO_WIZARD_API_KEY=$GTO_WIZARD_API_KEY \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  pokerskill-agent gtowizard --num-hands 100 --model <model> --log-dir /work/logs
```

## Local Installation (Linux x86_64 + Python 3.12)

```bash
python3.12 -m venv .venv && . .venv/bin/activate
pip install .
pokerskill-agent --help
```

> Every module of `pokerskill_agent` is a compiled CPython extension built for
> **CPython 3.12 on x86-64 Linux** (glibc 2.39, Ubuntu 24.04). Other interpreter
> versions cannot import it; use the Docker image or match that interpreter. The
> only Python file in the package is a two-line `__init__.py` that re-exports the
> package API.

## Usage

### Inspect a prompt (no API key)

`prompt` prints the system and user prompt the agent would send for one decision.
It is deterministic and needs no network or model access:

```bash
pokerskill-agent prompt --state pokerskill_agent/examples/flop_cbet.json
pokerskill-agent prompt --state pokerskill_agent/examples/preflop_btn_open.json --layers p1,p2
pokerskill-agent prompt --state pokerskill_agent/examples/river_bluffcatch.json --no-skills
pokerskill-agent prompt --state pokerskill_agent/examples/flop_cbet.json --json
```

Three states are included (`pokerskill_agent/examples/`): a button open, a flop
c-bet decision, and a river bluff-catch. `--layers` selects the active skill
layers (`p1`–`p5` plus `vo` for the viable-option filter); `--no-skills` keeps
only the P1 system rules, which is the default-prompting baseline.

### Play Against GTO Wizard

```bash
export GTO_WIZARD_API_KEY=...
export OPENAI_API_KEY=...          # any OpenAI-compatible endpoint
export OPENAI_BASE_URL=...         # optional

pokerskill-agent gtowizard --num-hands 5000 --model <model> --concurrent 3 \
    --log-dir logs/run1
```

Each hand is created, played decision by decision, and closed through the
Researcher API; the server returns the AIVAT-adjusted result for the hand. The
run writes `results_<num-hands>h.csv` (one row per hand) and `benchmark.log` into
the log directory. Add `--log-prompts` to store every prompt and model response.

The paper's main results used `--num-hands 5000 --concurrent 3` (10,000 for the
ablation). All reported model endpoints were OpenAI-compatible, which is why a
single driver covers every model in the paper.

| Option | Default | Description |
|--------|---------|-------------|
| `--num-hands` | 100 | Number of hands to play |
| `--model` | gpt-5.5 | Model name at the OpenAI-compatible endpoint |
| `--base-url` | `OPENAI_BASE_URL` | API base URL override |
| `--concurrent` | 3 | Concurrent hands |
| `--temperature` | 0.3 | Sampling temperature |
| `--max-tokens` | 4096 | Max completion tokens |
| `--reasoning-effort` | (none) | `low` / `medium` / `high` / `xhigh` for reasoning models |
| `--log-prompts` | off | Store every prompt and response |
| `--log-dir` | `logs/<model>` | Output directory |
| `--no-skills` | off | Default-prompting baseline |
| `--strict-api` | off | Fail the hand instead of falling back to a default action when the model is unavailable |

### Play Against Slumbot

```bash
export SLUMBOT_USERNAME=...        # free account from slumbot.com
export SLUMBOT_PASSWORD=...

pokerskill-agent slumbot --num-hands 20000 --model <model> --delay 0.5 \
    --max-tokens 1024 --log-dir logs/slumbot1
```

Slumbot has no AIVAT and no reference strategy, so this driver reports raw
winnings. Hands are played one at a time; the running result is checkpointed to
`checkpoint.json` every 100 hands, and `--resume` continues from it. Outputs per
run: `checkpoint.json`, `slumbot_results.json` (per-hand winnings and stats),
`report.txt`, and one `hand_<id>.log` per hand. Slumbot is a single session per
account, so the paper ran 20 accounts as 20 processes, each with its own log
directory.

### Ablations

The leave-one-out ablation of the skill layers is a flag on the GTO Wizard
driver:

```bash
pokerskill-agent gtowizard --num-hands 10000 --model <model> --disable-p4 --log-dir logs/wo_p4
```

| Flag | Layer removed |
|------|---------------|
| `--disable-p1` | P1 system rules (falls back to a minimal system prompt) |
| `--disable-p2` | P2 preflop range table |
| `--disable-p3` | P3 general postflop principles |
| `--disable-p4` | P4 context-specific strategy |
| `--disable-p5` | P5 river blocker guidance |
| `--disable-viable-options` | the viable-option filter (`vo`) |

## Environment Variables

| Variable | Required For | Description |
|----------|-------------|-------------|
| `GTO_WIZARD_API_KEY` | `gtowizard` | GTO Wizard Researcher API key (or `--gto-api-key`) |
| `OPENAI_API_KEY` | `gtowizard`, `slumbot` | Key for the OpenAI-compatible model endpoint |
| `OPENAI_BASE_URL` | optional | Base URL of the model endpoint (or `--base-url`) |
| `SLUMBOT_USERNAME`, `SLUMBOT_PASSWORD` | `slumbot` | slumbot.com account (or `--username`/`--password`) |

No key, token, or account is stored in this package; nothing is written to disk
except run outputs.

## Determinism

For a fixed game state and a fixed set of skill layers, the prompt is a pure
function of its inputs and is byte-identical between calls. The model's answer is
not deterministic, and the preflop range table samples from a mixed strategy
using the `random` module, so two runs of the same command will not agree hand
for hand. The results in the paper are averages over thousands of hands.

## Package Layout

| Path | Contents |
|------|----------|
| `pokerskill_agent/prompt_builder.*.so` | prompt assembly, layer gating |
| `pokerskill_agent/skill_content.*.so` | skill library text and system prompts |
| `pokerskill_agent/action_line_context.*.so` | scenario IDs, weighted pressure, budgets |
| `pokerskill_agent/postflop_analyzer.*.so` | board/hand analysis, P3/P4/P5 retrieval |
| `pokerskill_agent/preflop_range.*.so` | preflop range table and mixed-strategy sampling |
| `pokerskill_agent/unwanted_outs.*.so` | turn/river card-removal analysis |
| `pokerskill_agent/response_parser.*.so` | model-output validation and bounds repair |
| `pokerskill_agent/_api.*.so`, `cli.*.so`, `schema.*.so` | package API, command line, input validation |
| `pokerskill_agent/driver_gto.*.so`, `driver_slumbot.*.so` | the two evaluation drivers |
| `pokerskill_agent/gpt_poker_agent.*.so`, `openai_client.*.so` | per-decision model loop and API client |
| `pokerskill_agent/gto_wizard_client.*.so`, `gto_wizard_runner.*.so` | Researcher API client and hand loop |
| `pokerskill_agent/slumbot_api.*.so`, `hunl_engine.*.so` | Slumbot HTTP API and hand-state bridge |
| `pokerskill_agent/config.*.so`, `__init__.py`, `examples/` | run configuration, re-export stub, example states |

Analysis, plotting, auditing, and experiment-launch scripts are not part of this
release, and neither is the code that produced the paper's figures and tables.
The two drivers above are the ones that produced every number in the paper. The
full source, including the skill library as readable text, is released upon
publication of the paper.

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

## Citation

```bibtex
@article{li2026pokerskill,
  title={PokerSkill: LLMs Can Play Expert-Level Poker without Training or Solvers},
  author={Li, Boning and Wang, Baoxiang and Huang, Longbo},
  journal={arXiv preprint arXiv:2605.30094},
  year={2026}
}
```

## License

This project is licensed under the CC BY-NC 4.0 License (non-commercial use only) - see the [LICENSE](LICENSE) file for details.
