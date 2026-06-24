The proposed structure and why each folder exists:

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
│       └── 001_initial.sql
│
├── etl/
│   ├── __init__.py
│   ├── extract.py
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
│   ├── routers/
│   │   ├── products.py
│   │   └── alerts.py
│   └── schemas.py -> Pydantic
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