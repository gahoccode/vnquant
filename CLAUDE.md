# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`vnquant` is a Python package for downloading and visualizing Vietnam stock market data. It provides comprehensive financial information including historical prices, financial reports, business reports, and cashflow reports for Vietnamese stocks. The package supports multiple data sources (CAFE and VND/VNDIRECT) and offers advanced visualization with technical indicators like MACD, RSI, and Bollinger Bands.

## Package Configuration

This project uses modern Python packaging with `pyproject.toml` as the primary configuration file. The package metadata has been migrated from `setup.py` to `pyproject.toml`.

**IMPORTANT**: Keep `requirements.txt` and `pyproject.toml` dependencies synchronized at all times. When updating one, update the other.

### Installation

**Modern Installation with uv (Recommended):**
```bash
# Install in development mode
uv pip install -e .

# Or create virtual environment and install
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

**Traditional Installation:**
```bash
python setup.py install
```

Or using pip in editable mode:
```bash
pip install -e .
```

### Dependencies

Core dependencies (must be kept in sync between `requirements.txt` and `pyproject.toml`):
- pandas>=0.19.2
- numpy>=1.20.2
- requests>=2.3.0
- wrapt>=1.10.0
- lxml>=4.3.0
- pypandoc>=1.4
- plotly>=4.2.1
- bs4>=0.0.1
- matplotlib>=3.0.0

Python version requirement: >=3.10

## Architecture

### Core Components

1. **Data Loaders** (`vnquant/data/`)
   - `DataLoader`: Main class for downloading stock price data
     - Supports both single and multiple stock symbols
     - Returns data in three table styles: 'levels' (multi-index), 'prefix', or 'stack'
     - Can fetch minimal or full dataset
   - `FinanceLoader`: Downloads financial reports, business reports, cashflow reports, and basic indices
   - Data source implementations:
     - `DataLoaderCAFE` (`vnquant/data/loader/cafe.py`): Fetches from CAFE source
     - `DataLoaderVND` (`vnquant/data/loader/vnd.py`): Fetches from VNDIRECT API
   - Base class: `DataLoadProto` (`vnquant/data/loader/proto.py`)

2. **Visualization** (`vnquant/plot/`)
   - `vnquant_candle_stick()`: Main function for candlestick charts
     - Accepts either stock symbol (downloads data) or pandas DataFrame (OHLC/OHLCV format)
     - Supports advanced metrics: volume, MACD, RSI
     - Uses Plotly for interactive charts
   - `vnquant_candle_stick_source()`: Specifically for symbol-based visualization with advanced indicators

3. **Utilities** (`vnquant/utils/`)
   - `utils.py`: Helper functions including:
     - `_isOHLC()`: Validates if DataFrame has required OHLC columns
     - `_isOHLCV()`: Validates if DataFrame has required OHLCV columns
     - `convert_text_dateformat()`: Converts date format strings
   - `exceptions.py`: Custom exception classes

4. **Configuration** (`vnquant/configs/`)
   - `configs.py`: Centralized configuration for URLs, headers, column mappings, and regex patterns

5. **Logging** (`vnquant/log/`)
   - Custom logging setup for package operations

### Data Flow

1. User creates `DataLoader` or `FinanceLoader` with symbols and date range
2. Loader selects appropriate data source adapter (CAFE or VND)
3. Data is fetched via HTTP requests to external APIs
4. Raw data is transformed into pandas DataFrame with multi-index columns
5. Data can be visualized using `plot` module functions

## Common Development Tasks

### Running Tests

Execute the test file:
```bash
python test.py
```

Note: The `test.py` file contains commented-out test cases. Uncomment specific sections to test different functionalities.

### Building the Package

**Modern Build with uv (Recommended):**
```bash
uv build
```

**Traditional Build:**
```bash
python -m build
```

This creates distribution files in the `dist/` directory.

### Publishing the Package

**Publish with uv (Recommended):**
```bash
# Publish to PyPI with token
uv publish --token pypi-<your-pypi-token>

# Or set token as environment variable
export UV_PUBLISH_TOKEN=pypi-<your-pypi-token>
uv publish

# For Test PyPI
uv publish --publish-url https://test.pypi.org/legacy/ --token pypi-<your-test-token>
```

**Traditional Publishing:**
```bash
# With twine
python -m build
twine upload dist/* --token pypi-<your-pypi-token>
```

### Data Sources

- **CAFE**: CafeF.vn API endpoint (`configs.URL_CAFE`)
- **VND**: VNDIRECT API endpoint (`configs.API_VNDIRECT`)

### Key Data Structures

**Stock Data Columns** (minimal mode):
- `code`: Stock symbol
- `high`, `low`, `open`, `close`: Price data
- `adjust`: Adjusted price (renamed from `adjust_price` or `adjust_close` depending on source)
- `volume_match`: Matched volume
- `value_match`: Matched value

**Table Styles**:
- `levels`: Multi-index columns with 'Attributes' and 'Symbols' levels
- `prefix`: Flat columns with format `{SYMBOL}_{ATTRIBUTE}`
- `stack`: Single-level columns with additional 'code' column for symbol identification

## Technical Details

### Date Handling
- Input dates: String format 'YYYY-MM-DD' or datetime objects
- Internal conversions handle both '%d/%m/%Y' and '%Y-%m-%d' formats
- Date ranges are calculated to determine API pagination size

### API Pagination
- Both CAFE and VND loaders calculate page size based on date range (delta.days + 1)
- Single page request with size = total days to fetch all data at once

### Multi-Symbol Support
- When loading multiple symbols, data is concatenated along columns (axis=1)
- Each symbol's data becomes a separate column group in multi-index structure
- Data is sorted by date in descending order (most recent first)

### Visualization Technical Indicators

**MACD Calculation**:
- Fast EMA: 12-day exponential moving average
- Slow EMA: 26-day exponential moving average
- MACD Line: Fast EMA - Slow EMA
- Signal Line: 9-day EMA of MACD
- Histogram: MACD - Signal

**RSI Calculation**:
- Based on 14-period (com=13) exponential moving average
- Formula: 100 - (100/(1 + RS)) where RS = EMA(gains)/EMA(losses)
- Overbought line: 70
- Oversold line: 30

## Fork Maintenance

This is a fork of phamdinhkhanh/vnquant with modernized packaging and enhanced visualization features.

### Repository Structure
- **Origin**: `https://github.com/gahoccode/vnquant.git` (this fork)
- **Upstream**: `https://github.com/phamdinhkhanh/vnquant` (original project)
- **Branch Strategy**: Two-branch approach
  - `upstream-master`: Kept in sync with original project
  - `master`: Contains fork improvements (packaging modernization + enhanced features)

### Upstream Sync Workflow

**Regular Sync Process:**
```bash
# 1. Fetch latest changes from upstream
git fetch upstream

# 2. Update local upstream-master branch to match remote upstream/master
git checkout upstream-master
git merge upstream/master

# 3. Switch to master and merge upstream changes (excluding protected files)
git checkout master
git merge upstream-master
```

**Note**: `upstream-master` is a local tracking branch for `upstream/master` (the original project). Do not push this branch to origin.

### Protected Files (Never Merge from Upstream)

These files contain fork-specific improvements and should NEVER be overwritten by upstream changes:

1. **setup.py**
   - **Fork version**: Minimal (8 lines, delegates to pyproject.toml)
   - **Upstream version**: Full configuration (~60 lines)
   - **Reason**: Fork uses modern pyproject.toml packaging

2. **pyproject.toml**
   - **Status**: Fork-only file (doesn't exist in upstream)
   - **Reason**: Modern Python packaging configuration
   - **Version**: 0.1.21 (fork version)

3. **vnquant/plot/Plot.py**
   - **Fork changes**: +220 lines of enhanced visualization features
   - **Added features**: MACD and RSI technical indicators
   - **Reason**: Fork has advanced candlestick charting capabilities

### Merge Conflict Resolution

When merging `upstream-master` into `master`:

**If conflicts occur in protected files:**
```bash
# For setup.py
git checkout HEAD -- setup.py

# For pyproject.toml
git checkout HEAD -- pyproject.toml

# For vnquant/plot/Plot.py
git checkout HEAD -- vnquant/plot/Plot.py
```

**For other files:** Resolve conflicts normally, preserving fork improvements where applicable.

### Dependency Management

**CRITICAL**: Always keep dependency files synchronized:
- `pyproject.toml` `[project.dependencies]` section
- `requirements.txt`

**Current inconsistency to fix:**
- `pyproject.toml` includes `matplotlib>=3.0.0`
- `requirements.txt` missing `matplotlib>=3.0.0`

**When updating dependencies:**
1. Add to `pyproject.toml` `[project.dependencies]`
2. Add identical version to `requirements.txt`
3. Commit both files together

### Version Management

- **Upstream**: Currently at v0.1.2
- **Fork**: v0.1.21 (packaging modernization)
- **Strategy**: Fork version indicates packaging improvements while maintaining API compatibility

## Code Style

- Use type hints for function parameters (see `DataLoader.__init__` for reference)
- Follow existing docstring format with Args/Return sections
- Suppress warnings for InsecureRequestWarning and FutureWarning (already configured)
- Use pandas operations for data transformations
- Log important operations using the `logger` from `vnquant.log`
