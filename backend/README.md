# Backend — Pantheon Research Qwen Hackathon

FastAPI backend that orchestrates dual-LLM qualitative equity analysis with agreement scoring, tone classification, and divergence detection.

## Endpoints

| Method | Path                              | Description                                       |
|--------|-----------------------------------|---------------------------------------------------|
| GET    | `/`                               | Root info                                         |
| GET    | `/health`                         | Health check                                      |
| GET    | `/api/project`                    | Project metadata                                  |
| GET    | `/api/evidence/{ticker}`          | Get equity evidence data for a ticker             |
| GET    | `/api/overlay/qwen/{ticker}`      | Run Qwen Cloud qualitative overlay                |
| GET    | `/api/overlay/deepseek/{ticker}`  | Run DeepSeek qualitative overlay                  |
| GET    | `/api/comparison/{ticker}`        | Full dual-provider comparison with agreement score|
| GET    | `/api/demo-flow`                  | Demo flow steps                                   |
| GET    | `/api/alibaba/proof`              | Alibaba Cloud deployment proof                    |
| GET    | `/api/alibaba/qwen-config`        | Qwen / DashScope configuration                    |

## Running

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Environment Variables

| Variable           | Description                        | Default     |
|--------------------|------------------------------------|-------------|
| DASHSCOPE_API_KEY  | Alibaba Cloud DashScope API key    | (optional)  |
| DEEPSEEK_API_KEY   | DeepSeek API key                   | (optional)  |
| DEMO_MODE          | `offline` for sample data, `live`  | `offline`   |
| QWEN_MODEL         | Qwen model override                 | `qwen-plus` |
| DEEPSEEK_MODEL     | DeepSeek model override             | `deepseek-chat` |

In offline mode (default), no API keys are needed. The app uses bundled sample data in `../data/`.

## Modules

- `main.py` — FastAPI app, route definitions, CORS
- `app/models.py` — Pydantic data models (EquityEvidence, OverlayAssessment, QualitativeOverlay, ComparisonResult)
- `app/sample_loader.py` — Load sample evidence data from `data/`
- `app/qwen_overlay.py` — Qwen Cloud (DashScope) integration
- `app/deepseek_overlay.py` — DeepSeek integration
- `app/comparison.py` — Tone classification, divergence detection, agreement scoring, full comparison
- `app/alibaba_cloud_proof.py` — Alibaba Cloud deployment proof endpoints

## Comparison Fields

Each overlay produces these structured assessment fields:

- `business_quality`
- `moat`
- `pricing_power`
- `capital_allocation`
- `red_flags`
- `confidence` (0–1)
- `missing_evidence` (list)

## Tests

```bash
python -m pytest
```
