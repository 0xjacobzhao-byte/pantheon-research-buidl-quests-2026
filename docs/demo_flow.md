# Demo Flow

## Prerequisites

1. Copy `.env.example` to `.env`
2. Keep `DEMO_MODE=offline` for offline demo (no API keys needed)
3. Optionally fill in `DASHSCOPE_API_KEY` and `DEEPSEEK_API_KEY` for live mode

## Step-by-Step Demo

### Step 1: Start the Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Step 2: Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

### Step 3: Open the App

Navigate to http://localhost:5173

### Step 4: Select a Ticker

Choose **MA** (Mastercard) or **NVDA** (NVIDIA) from the ticker panel.

### Step 5: Run Comparison

Click **"Run Comparison"**. The app will:

1. Load equity evidence data from `GET /api/evidence/{ticker}`
2. Generate (or load sample) Qwen Cloud qualitative overlay from `GET /api/overlay/qwen/{ticker}`
3. Generate (or load sample) DeepSeek qualitative overlay from `GET /api/overlay/deepseek/{ticker}`
4. Compare both overlays via `GET /api/comparison/{ticker}`
5. Display both side-by-side with agreement scoring, tone classification, and divergences

### Step 6: Review the Output

Each provider's panel shows:
- **Model name** (e.g., `qwen-plus`, `deepseek-chat`)
- **Status badge** (green=SUCCESS, blue=OFFLINE_SAMPLE, red=BLOCKED/ERROR)
- **Assessment fields**: business_quality, moat, pricing_power, capital_allocation, red_flags
- **Confidence bar** (0–100%)
- **Missing evidence** list

The comparison section shows:
- **Agreement score** (0–1) and level (HIGH / MEDIUM / LOW)
- **Tone badges** for each provider (positive, conservative_positive, cautious, neutral, negative)
- **Divergences** with severity (major, moderate, minor)
- **Evidence gaps** merged from both providers
- **Human review required** flag

### Step 7: Check Alibaba Cloud Proof

Scroll to the Alibaba Cloud Integration section to see:
- Cloud provider, backend runtime, reverse proxy, database service, Qwen provider
- Or call `GET /api/alibaba/proof` for the full JSON

## API Endpoints for Manual Testing

```bash
# Root info
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# Project metadata
curl http://localhost:8000/api/project

# Get evidence for a ticker
curl http://localhost:8000/api/evidence/MA

# Get Qwen overlay
curl http://localhost:8000/api/overlay/qwen/MA

# Get DeepSeek overlay
curl http://localhost:8000/api/overlay/deepseek/MA

# Get full comparison
curl http://localhost:8000/api/comparison/MA

# Get demo flow steps
curl http://localhost:8000/api/demo-flow

# Alibaba Cloud deployment proof
curl http://localhost:8000/api/alibaba/proof

# Qwen/DashScope configuration
curl http://localhost:8000/api/alibaba/qwen-config
```

## Docker Compose Demo

```bash
cp .env.example .env
docker-compose up --build
```

Both services start automatically. Frontend at :5173, backend at :8000.

## Switching to Live Mode

1. Set `DEMO_MODE=live` in `.env`
2. Set `DASHSCOPE_API_KEY=<your-key>`
3. Set `DEEPSEEK_API_KEY=<your-key>`
4. Restart the backend

Both providers will make real API calls concurrently.
