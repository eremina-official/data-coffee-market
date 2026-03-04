## Polish Coffee Roasters – ETL project 🇵🇱☕

### Project Goals

A data-driven exploration the **Polish premium coffee market**, with a focus on coffee sold by **private roasting houses** (excluding mass-market brands). The **goal** is to **collect, clean and analyze market data** and present insights through an **interactive Power BI dashboard**. The focus is on product origins, taste profiles and brand strategies.

---

### Data Source

Data is collected using the **Allegro REST API** `sale/products` endpoint, which provides listed product data ([documentation](https://developer.allegro.pl/documentation#tag/Products/operation/getFlatProductParametersUsingGET)).

Due to restrictions on the `offers/listing` endpoint (as of January 2026 available only for verified applications), pricing data cannot be reliably collected via the REST API.

---

### 📊 Interactive Power BI Dashboard – Key Market Insights

What the Data Reveals:

🌍 ***Coffee origins that dominate the market***
  
- **Brazil**, **Peru** and **Colombia** appear most frequently as origins in Allegro’s premium coffee listings.

📦 ***How premium coffee is actually packaged***

- **Two sizes clearly win**: 250 g (specialty-friendly) and 1000 g (bulk buyers and heavy drinkers). Everything else is niche.

🏷️ ***Who bets on single-origin quality***

- **Blue Orca Coffee**, **Palarnia Kawy W&A** and **Nuno** stand out for offering the highest number of single-origin coffees, signaling a quality-focused portfolio.

🧭 ***Who explores the world the most***

- **Blue Orca Coffee**, **Nuno** and **Palarnia Kawy Magic Drum** offer the widest diversity of countries of origin — a clear differentiation strategy.

🍫 ***Taste profiles by country***

- Coffees from **Guatemala** and **India** score highest on taste intensity in premium products.

---

#### Power BI Dashboard - Overview of Coffee Products

![Power BI Dashboard Screenshot](/bi/coffee-roasters-powerbi-overview.png)


#### Power BI Dashboard - Overview of Roasters

![Power BI Dashboard Screenshot](/bi/coffee-roasters-powerbi-brands.png)

These insights are generated from an automated ETL pipeline and explored interactively in Power BI, demonstrating how raw product data can be transformed into market-level intelligence. For more insights and detailed analysis, check out the [Power BI dashboard](/bi/coffee-market-2026.pbix).

---

### Project Architecture

This project is designed to run both **locally and in the cloud**, using the same logical data flow.


**Local Setup:**

`JSON → Python → Local DB → Power BI`


**Azure Cloud Setup:**

Cloud setup is described [here](https://github.com/eremina-official/azure-func-coffee-data-etl).

---

### 🧱 Tech Stack

- Python for data extraction and transformation (Poetry, Pydantic, mysql-connector-python)
- MySQL (structured data storage and analysis)
- DBeaver (database management)
- Power BI (DAX, data modeling, dashboards)

---

### Methodology

#### Data Extraction

Products were fetched using the `/sale/products` endpoint with keyword-based search (e.g. `kawa palarnia`).
Responses were stored as raw JSON files for traceability and repeatability.

***Engineering Decisions***

- Immutable ingestion layer (raw files are never modified)
- Idempotent re-fetching strategy (files are stored with deterministic filenames based on timestamp + query hash to avoid accidental overwrites)

#### Data Transformation

A normalized **relational schema (snowflake-style)** was designed in MySQL.

**Schema Design:**
- products
- categories
- parameters (dictionary)
- parameter_values
- product_parameter_values (many-to-many mapping)

***Engineering Decisions***

- Why snowflake schema? Product parameters are dinamic and multivalued (roast level, origin, processing method).
- Dictionary for product parameters: attributes (brand, origin, roast type) are stored once and referenced via foreign keys to reduces redundancy and allow for easier updates to attribute names/values.
- Parameters without stable identifiers or consistent naming were excluded to avoid polluting the dictionary tables.

#### Data Loading to MySQL

Python scripts process raw JSON and insert structured records into MySQL.

***Engineering Decisions***

- Products are inserted idempotently to avoid duplication (unique ids).
- Two phase loading: first dictionary tables (parameters, parameter_values) are populated, then products and their parameter mappings are inserted.

#### Data Analysis

**Power BI** consumes the curated tables (views) and presents dashboards. The Power BI model implements a **Fact Constellation schema** (few fact tables that share common dimensions). 

***Engineering Decisions***

- Why not **star schema** in Power BI? The product parameters are dynamic and multivalued, **analysis requires complicated quires with multiple joins**. A star schema would require denormalization and lead to data duplication, maintenance and performance issues.

---

#### Data Quality Rules

- Data quality is enforced during transformation, not at ingestion or postload. This allows for traceability and reprocessing if rules change.
- Filter out non-coffee products returned by keyword-based searches.
- Standardize parameter names, values, and measurement units where possible.

Trade-offs:
Strict filtering improves analytical consistency but may exclude edge-case products.

#### Analysis Strategy

SQL queries are used to:
- Compare coffee origins, brands, and characteristics.
- Count products by selected attributes.
- Filter products based on parameter cardinality.

#### Limitations

- The analysis focuses on market structure and product characteristics, not pricing or seller performance.
- Catalog products may exist without active offers.
- Results reflect catalog data, not real-time market dynamics.
- The classification is based on seller identity and branding, not on official quality certifications.

---

### 📁 Project Structure

```text
src/
  - fetchers/ – get raw JSON from API
  - pipelines/ – ETL orchestration and data processing logic
  - db/ – database insert logic
  - models/ – data schemas and validation
  - sql/ – SQL scripts for data analysis and Power BI views
  - utils/ – shared helpers
bi/ – Power BI dashboard files
```

---

### 🚀 Getting Started

#### Requirements

* Python 3.11+
* This project uses **Poetry** for dependency management and reproducible builds.


#### Clone, Activate Environment & Install Dependencies

```bash
git clone <repo-url>
cd data-coffee-market

poetry shell

poetry install
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

### 📄 License

MIT
