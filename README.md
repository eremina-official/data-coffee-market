## Polish Coffee Roasters – ETL project 🇵🇱☕

### Project Goals

A data-driven exploration the **Polish premium coffee market**, with a focus on coffee sold by **private roasting houses** (excluding mass-market brands). The **goal** is to **collect, clean and analyze market data** and present insights through an **interactive Power BI dashboard**. The focus is on product origins, taste profiles and brand strategies.

---

### Data Source

Data is collected using the **Allegro REST API** `sale/products` endpoint, which provides listed product data ([documentation](https://developer.allegro.pl/documentation#tag/Products/operation/getFlatProductParametersUsingGET)).

Due to restrictions on the `offers/listing` endpoint (as of January 2026 available only for verified applications), pricing data cannot be reliably collected via the REST API.

---

### 📊 Power BI Dashboard – Key Market Insights

☕ What the Data Reveals:

🌍 **Coffee origins that dominate the market**
Brazil, Peru and Colombia appear most frequently as origins in Allegro’s premium coffee listings.

📦 **How premium coffee is actually packaged**
Two sizes clearly win: 250 g (specialty-friendly) and 1000 g (bulk buyers and heavy drinkers). Everything else is niche.

🏷️ **Who bets on single-origin quality**
Blue Orca Coffee, Palarnia Kawy W&A and Nuno stand out for offering the highest number of single-origin coffees, signaling a quality-focused portfolio.

🧭 **Who explores the world the most**
Blue Orca Coffee, Nuno and Palarnia Kawy Magic Drum offer the widest diversity of countries of origin — a clear differentiation strategy.

🍫 **Taste profiles by country**
Coffees from Guatemala and India score highest on taste intensity in premium products.

For more insights and detailed analysis, check out the [Power BI dashboard](`/bi/coffee_market.pbix`).

---

### Project Architecture

This project is designed to run both **locally and in the cloud**, using the same logical data flow.

**Local setup (development & testing):**

`JSON → Python → Local DB → Power BI`


**Azure Cloud Setup:**

Cloud setup is described [here](https://github.com/eremina-official/azure-func-coffee-data-etl).

---

### 🧱 Tech Stack

- Python (Poetry, Pydantic, mysql-connector-python)
- MySQL
- DBeaver (database management)
- Power BI (data model & dashboards)

---

### Methodology

**Data Extraction**

Products were fetched using the `/sale/products` endpoint with keyword-based search (e.g. `kawa palarnia`).
Responses were stored as raw JSON files for traceability and repeatability. 

**Data Transformation**

A normalized **relational schema (snowflake-style)** was designed in MySQL.

Core entities include:
- products
- categories
- parameters (dictionary)
- parameter_values
- product_parameter_values (many-to-many mapping)

Reusable attributes (e.g. brand, origin, roast type) are stored once and linked to products. Images and descriptions are stored as JSON to preserve original structure.

**Data Loading**

- Python scripts load raw JSON files and insert data into MySQL. 
- Dictionary tables (parameters, parameter_values) are populated once and reused.
- Products are inserted idempotently to avoid duplication.
- Selected parameters (e.g. redundant weight attributes) are explicitly excluded during ingestion.

**Data Quality Rules**

- Ignore parameters without stable or reusable identifiers.
- Filter out non-coffee products returned by keyword-based searches.
- Standardize parameter names, values, and measurement units where possible.

**Analysis**

SQL queries are used to:
- Compare coffee origins, brands, and characteristics
- Count products by selected attributes
- Filter products based on parameter cardinality
The analysis focuses on market structure and product characteristics, not pricing or seller performance.

**Limitations**

- Prices and availability are not analyzed due to restricted access to live listings.
- Catalog products may exist without active offers.
- Results reflect catalog data, not real-time market dynamics.
- The classification is based on seller identity and branding, not on official quality certifications.

---

### 📁 Project Structure

```text
- fetchers/ – get raw JSON from API
- pipelines/ – ETL orchestration and data processing logic
- db/ – database insert logic
- models/ – data schemas and validation
- utils/ – shared helpers
```

---

### 🚀 Getting Started

#### 1️⃣ Requirements

* Python 3.11+
* This project uses **Poetry** for dependency management and reproducible builds.


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


#### 3️⃣ Activate Environment

```bash
poetry shell
```

or run commands directly:

```bash
poetry run python
```


#### 4 Install Packages

```bash
poetry add package-name
```

install dev dependancies:

```bash
poetry add --group dev package-name
```

#### 🔒 Environment Variables

Create a `.env` file if needed:

```env
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

#### 🧪 Testing

```bash
poetry run pytest
```

---

### 🛠️ Development Notes

* Prefer **append-only** tables for historical data
* Never overwrite raw data
* Keep transformations reproducible

---

### 📄 License

MIT
