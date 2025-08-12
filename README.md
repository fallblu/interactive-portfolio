# Interactive Portfolio

A Streamlit app for an interactive personal portfolio with time-series retrieval and Plotly visualization.

## Quickstart

**Requirements:** Python 3.10+

```bash
# clone & enter
git clone <your-repo-url>
cd <your-repo>

# (recommended) create & activate a venv
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# install (dev extras optional)
python -m pip install -U pip
python -m pip install -e .[dev]

# run the app
streamlit run src/interactive_portfolio/app/portfolio.py```


## Configuration

Streamlit reads settings from `.streamlit/config.toml`.  
This repo includes two templates you can copy into place:

.streamlit/
├─ config.toml # active config (used by Streamlit)
├─ config.dev.toml # local dev template (opens browser automatically)
└─ config.prod.toml # prod template (headless server mode)


### Use the dev config (local development)

# Windows
```powershell
Copy-Item .streamlit\config.dev.toml .streamlit\config.toml -Force
streamlit run src\interactive_portfolio\app\portfolio.py```

# macOS/Linux
```bash
cp .streamlit/config.dev.toml .streamlit/config.toml
streamlit run src/interactive_portfolio/app/portfolio.py```


### Use the prod config (servers/containers/CI)

# Windows
```powershell
Copy-Item .streamlit\config.prod.toml .streamlit\config.toml -Force
streamlit run src\interactive_portfolio\app\portfolio.py```

# macOS/Linux
```bash
cp .streamlit/config.prod.toml .streamlit/config.toml
streamlit run src/interactive_portfolio/app/portfolio.py```