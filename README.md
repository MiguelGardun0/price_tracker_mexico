# Price Tracker MX

A web app that tracks product prices across Mexican marketplaces (MercadoLibre, Amazon MX, Walmart MX, Liverpool), stores the full price history, predicts when prices will drop, and sends alerts to the user.

## Tech Stack

| Layer       | Technology                              |
|-------------|-----------------------------------------|
| Language    | Python 3.10+                            |
| Scraping    | `requests` + `beautifulsoup4`           |
| Database    | PostgreSQL 17 (Docker)                  |
| Scheduling  | cron (MVP) → Airflow (production)       |
| ML          | Prophet, scikit-learn, NumPy            |
| API         | FastAPI                                 |
| Frontend    | React                                   |
| Alerts      | SendGrid (email), Twilio (WhatsApp)     |
| Auth        | NextAuth                                |
| Payments    | Stripe / MercadoPago                    |

## Project Structure

```
price_tracker/
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── pyproject.toml
│
├── scraper/
│   ├── __init__.py
│   ├── base.py
│   ├── mercadolibre.py
│   ├── amazon_mx.py
│   ├── walmart_mx.py
│   └── liverpool.py
│
├── db/
│   ├── __init__.py
│   ├── connection.py
│   └── migrations/
│       └── 01_schema.sql
│
├── etl/
│   ├── __init__.py
│   ├── transform.py
│   └── load.py
│
├── ml/
│   ├── __init__.py
│   ├── predictor.py
│   ├── anomaly.py
│   └── buy_score.py
│
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── routers/
│       ├── products.py
│       └── alerts.py
│
├── alerts/
│   ├── __init__.py
│   ├── email.py
│   └── whatsapp.py
│
├── dags/
│   └── scrape_prices.py
│
├── frontend/
│
├── tests/
│   ├── test_scraper.py
│   ├── test_etl.py
│   └── test_ml.py
│
└── logs/
    └── .gitkeep
```

## Getting Started

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Docker Desktop

### Setup

1. Clone the repository and install dependencies:

```bash
uv sync
```

2. Copy the environment variables file and fill in your values:

```bash
cp .env.example .env
```

3. Start the PostgreSQL container:

```bash
docker compose up -d
```

4. Run the database migrations:

```bash
docker exec -i postgres_db psql -U <POSTGRES_USER> -d <POSTGRES_DB> < db/migrations/01_schema.sql
```

## Useful Commands

Access the database interactively:

```bash
docker exec -it postgres_db psql -U <POSTGRES_USER> -d <POSTGRES_DB>
```

List tables once inside `psql`:

```
\dt
```

Inspect a table's structure:

```
\d products
\d prices
```

## Roadmap

- [ ] Phase 1 — Scraper + database schema
- [ ] Phase 2 — Predictive model + email alerts
- [ ] Phase 3 — Public web app + subscriptions
- [ ] Phase 4 — Scale to more marketplaces + WhatsApp alerts + affiliate links
