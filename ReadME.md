# AWS Agentic Cloud Cost Optimizer

An AI-powered CLI agent that lets you query your **AWS cloud spend in natural language**. Built with Google ADK and Gemini 2.5 Flash, backed by the AWS Cost Explorer API, with persistent conversation sessions via SQLite.

## Demo

```
You: What was the total cost of ECR between August 2025 and December 2025?

Agent: Let me calculate the total cost for Amazon ECR for you.

  • August 2025:    $0.000
  • September 2025: $0.000
  • October 2025:   $0.050
  • November 2025:  $0.378
  • December 2025:  $0.613

Total cost for ECR (Aug–Dec 2025): $1.04
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    CLI (agent.py)                    │
│                                                      │
│   User Input ──► Google ADK Agent (Gemini 2.5)      │
│                         │                            │
│              ┌──────────▼──────────┐                 │
│              │  Tool: get_cost_and │                 │
│              │  _usage()           │                 │
│              └──────────┬──────────┘                 │
│                         │                            │
│              AWS Cost Explorer API                   │
│              (boto3, grouped by SERVICE)             │
│                                                      │
│   Persistent session state ──► SQLite (aiosqlite)   │
└─────────────────────────────────────────────────────┘
```

## Tech Stack

| Component | Technology |
|---|---|
| AI Agent Framework | Google ADK (`google-adk`) |
| LLM | Gemini 2.5 Flash |
| AWS Integration | boto3 (Cost Explorer API) |
| Session Persistence | SQLite via `aiosqlite` |
| Runtime | Python 3.11+ (asyncio) |

## Repository Structure

```
.
├── agent.py          # Agent setup, session management, conversation loop
├── costAnalyser.py   # AWS Cost Explorer API tool (used by the agent)
├── requirements.txt  # Python dependencies
└── .env_copy         # Environment variable template
```

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/karthiks233/AWS_CostUsage_AgenticAI.git
cd AWS_CostUsage_AgenticAI
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env_copy .env
```

Edit `.env` with your credentials:

| Variable | Description |
|---|---|
| `GOOGLE_API_KEY` | Google AI Studio API key ([get one here](https://aistudio.google.com/app/apikey)) |
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |
| `AWS_DEFAULT_REGION` | AWS region (e.g. `us-east-1`) |

The IAM user requires the `ce:GetCostAndUsage` permission.

### 3. Run the agent

```bash
python agent.py
```

## Example Queries

```
What was my total AWS spend in January 2025?
Which service cost the most in Q3 2025?
What was the total cost of EC2 between March and June 2025?
Compare my S3 costs in November vs December 2025.
```

## How It Works

1. **`costAnalyser.py`** defines a `get_cost_and_usage()` function that calls AWS Cost Explorer, grouped by service with monthly granularity.
2. **`agent.py`** registers this function as a tool with the Google ADK Agent, which decides autonomously when to call it based on the user's natural-language question.
3. Sessions are stored in a local SQLite database (`agent_sessions.db`), so conversation history persists across runs.

## License

MIT License — see [LICENSE](LICENSE) for details.
