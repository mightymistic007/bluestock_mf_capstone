# Bluestock Mutual Fund Analytics Platform 

An institutional-grade, end-to-end data engineering pipeline and business intelligence system built to ingest, clean, evaluate, and visualize historical and live mutual fund schemes. This framework automates core risk management metrics, monitors portfolio concentrations, tracks investor churn risk, and generates parameterized fund allocations.

##  Key Platform Features
- **Automated Data Pipelines:** Multi-source ingestion scripts updating system SQLite architectures with live market NAV feeds via the `mfapi.in` REST API.
- **Quantitative Performance Trackers:** System computing CAGR, OLS Alpha/Beta regressions against the Nifty 100, Sharpe, Sortino, Maximum Drawdowns, and tracking errors vs major indexes[cite: 1].
- **Advanced Tail-Risk Engines:** Automated extraction of 95% Historical Value at Risk (VaR) and Conditional Value at Risk (CVaR)[cite: 1].
- **Portfolio Audits (HHI Index):** Herfindahl-Hirschman index calculations analyzing sector concentration risks over equity blocks[cite: 1].
- **Behavioral Cohort Tracking:** Behavioral grouping maps measuring recurring transactional continuity and flagging accounts at risk (>35-day gaps)[cite: 1].
- **Interactive BI Infrastructure:** 4-page responsive Power BI application rendering demographic distributions, performance tiers, and asset trends[cite: 1].

---

##  Tech Stack & Prerequisites
- **Language:** Python 3.10+[cite: 1]
- **Core Processing:** Pandas, NumPy, SciPy (OLS Regressions)[cite: 1]
- **Database Engine:** SQLite3 via SQLAlchemy ORM[cite: 1]
- **Visualizations:** Matplotlib, Seaborn, Plotly[cite: 1]
- **Business Intelligence:** Power BI Desktop[cite: 1]

To install all platform dependencies locally, run:
```bash
pip install pandas numpy matplotlib seaborn plotly sqlalchemy scipy requests jupyter