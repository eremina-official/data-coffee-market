## Polish Independent Coffee Roasters – Market Analysis 🇵🇱☕

This project analyzes the Polish market of coffee sold by **independent/private roasting houses** (excluding mass-market brands), focusing on pricing, origin countries and brands. The goal is to collect, store and analyze market data over time and present insights via a BI/dashboard layer. 
The classification is based on seller identity and branding, not on official quality certifications.

---

### Data Source

Data is collected using the **Allegro REST API** `sale/products` endpoint, which provides listed product data ([documentation](https://developer.allegro.pl/documentation#tag/Products/operation/getFlatProductParametersUsingGET)).

Due to restrictions on the `offers/listing` endpoint (as of January 2026 available only for verified applications), pricing is not possible to collect via REST API.

---

### 🎯 Project Goals

* Collect coffee market data periodically (prices, brands, availability, ratings, etc.)
* Store historical data for time-based analysis
* Analyze trends (price changes, popularity, availability)
* Prepare clean datasets for BI tools (e.g. Power BI)

---

### 🧱 Tech Stack

- Python (Poetry, Pandas, SQLAlchemy)
- MySQL (time-based snapshots)
- DBeaver (database management)
- Power BI (data model & dashboards)

---

### 📁 Project Structure

```text
src/                       # Python scripts, modules
├── coffee_market_analysis/
│   ├── __init__.py
│   ├── config.py          # configuration & constants
│   ├── fetchers/          # API / scraping logic
│   ├── models/            # data models / schemas
│   ├── pipelines/         # ETL / data processing
│   └── utils/             # shared helpers
│
├── data/                    # database scripts
│   ├──            # table definitions
│   ├── indexes.sql          # optional indexes
│   └── sample_inserts.sql   # optional sample data
|
│── sql/
│   ├── raw/               # raw fetched data
│   └── processed/         # cleaned datasets
|
├── tests/
├── pyproject.toml
├── poetry.lock
└── README.md
```

---

### 🚀 Getting Started

#### 1️⃣ Requirements

* Python 3.11+
* This project uses **Poetry** for dependency management and reproducible builds.

---

#### 2️⃣ Clone & Setup

```bash
git clone <repo-url>
cd data-coffee-market
```

(Optional – keep venv inside project)

```bash
poetry config virtualenvs.in-project true --local
```

Install dependencies:

```bash
poetry install
```

---

#### 3️⃣ Activate Environment

```bash
poetry shell
```

or run commands directly:

```bash
poetry run python
```

---

#### 4 Install Packages

```bash
poetry add package-name
```

install dev dependancies:

```bash
poetry add --group dev package-name
```
---


### 📊 Data Workflow

1. **Fetch data** from APIs / sources
2. **Store raw data** (immutable)
3. **Transform & normalize** data
4. **Persist** to SQL database
5. **Expose** clean tables for BI

---

### 🗄️ Database Design (High Level)

* `brands`
* `products`
* `prices`
* `availability`
* `snapshots` (time dimension)

Designed to support **historical analysis** and trend comparisons.

---

### 📈 Analysis Examples

* Price evolution over time
* Brand popularity trends
* Availability by roastery
* Market segmentation (origin, roast level, processing)

---

### 🧪 Testing

```bash
poetry run pytest
```

---

### 🧩 BI / Reporting

Processed tables are optimized for:

* Power BI
* Star / snowflake schema
* Time-series analysis

---

### 🔒 Environment Variables

Create a `.env` file if needed:

```env
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

---

### 🛠️ Development Notes

* Prefer **append-only** tables for historical data
* Never overwrite raw data
* Keep transformations reproducible

---

### 📌 Roadmap

* [ ] Add data source adapters
* [ ] Automate scheduled data collection
* [ ] Expand BI dashboards
* [ ] Add anomaly detection (price spikes)

---

### 📄 License

MIT


1. Created project with poetry with local virtual env
2. Add readme
3. Add gitignore, run git init, add remote repo
4. Add .env
5. Add linter, prettier, improrts sorting, add config in pyproject.toml, set autoformat on save in vscode

6. Get data from Allegro REST API
7. Create database schema based on data structure
8. Create connection to local mysql db
9. Create python functions to insert one product to db
10. Insert 30 products to db in loop

