# Lichess Data Pipeline

An end-to-end data engineering portfolio project that ingests chess game data from the Lichess API, parses and validates it with Python, loads validated data into Snowflake, and transforms it into analytics-ready models with dbt.

## Architecture

```text
Lichess API
    ↓
Python API ingestion
    ↓
PGN parsing
    ↓
Python validation and rejected-row handling
    ↓
Snowflake RAW layer
    ↓
dbt staging model
    ↓
dbt analytics marts
```

## Tech Stack

- Python
- pandas
- requests
- python-chess
- pytest
- Snowflake
- SQL
- dbt
- Git / GitHub

## Pipeline

### 1. Lichess API Ingestion

`src/lichess_api.py`

- Retrieves recent games from the Lichess API
- Handles rate limits, server errors, timeouts, and connection errors
- Uses retry logic for transient failures
- Saves raw PGN data for downstream processing

### 2. PGN Parsing

`src/parse_pgn.py`

Converts raw PGN data into structured game records including:

- game ID
- game date
- player names
- ratings
- game result
- ECO and opening
- time control
- move count
- player color
- opponent rating
- rating difference
- player-relative result

### 3. Data Validation

`src/pandas_etl.py`

Performs validation including:

- required-column checks
- blank-value validation
- duplicate game ID detection
- accepted-value validation
- rejected-row tracking
- validation reporting

Invalid records are written separately instead of being silently discarded.

Automated Python tests are included in:

```text
tests/test_pandas_etl.py
```

### 4. Snowflake RAW Layer

Validated game data is loaded into:

```text
CHESS_ANALYTICS.RAW.LICHESS_GAMES
```

The Snowflake loading process uses a staging table and `MERGE` logic so repeated loads do not create duplicate games.

SQL setup and loading scripts are stored in:

```text
sql/
├── 01_create_raw.sql
└── 02_incremental_load.sql
```

### 5. dbt Transformation Layer

dbt reads from the Snowflake RAW layer and creates analytics-ready models.

#### Staging

```text
ANALYTICS.STG_LICHESS_GAMES
```

The staging model:

- references the RAW table through a dbt source
- converts raw date strings into proper date values
- provides a clean base model for downstream analytics

#### Analytics Marts

```text
ANALYTICS.MART_PLAYER_PERFORMANCE
ANALYTICS.MART_PERFORMANCE_BY_COLOR
```

The marts provide metrics including:

- total games
- wins, losses, and draws
- win percentage
- average player rating
- average opponent rating
- performance grouped by White and Black

## Data Quality

Validation occurs at both the Python and warehouse transformation layers.

### Python Tests

Pytest covers:

- valid rows
- blank required values
- invalid game results
- invalid player colors
- invalid player-relative results
- duplicate game IDs

### dbt Tests

dbt tests verify:

- unique and non-null game IDs
- non-null game dates
- accepted game results
- accepted player colors
- accepted player-relative results
- required mart fields
- unique color-level mart rows

The full dbt project currently completes successfully with:

```text
PASS=20
WARN=0
ERROR=0
```

## Project Structure

```text
lichess-data-pipeline/
├── chess_analytics_dbt/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── dbt_project.yml
├── data/
├── sql/
│   ├── 01_create_raw.sql
│   └── 02_incremental_load.sql
├── src/
│   ├── lichess_api.py
│   ├── pandas_etl.py
│   └── parse_pgn.py
├── tests/
│   └── test_pandas_etl.py
├── README.md
└── requirements.txt
```

## Engineering Concepts Demonstrated

- REST API ingestion
- retry and error handling
- PGN parsing
- data validation
- rejected-record handling
- automated testing
- Snowflake data warehousing
- staging-table load patterns
- incremental and idempotent loading
- dbt sources and models
- warehouse data quality testing
- analytics transformations
- Git version control