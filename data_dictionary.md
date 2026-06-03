# 📖 Bluestock Mutual Fund Platform Data Dictionary

This document serves as the structural data dictionary for the automated Mutual Fund Analytics Platform, detailing the relational tables, constraints, and business telemetry rules established in the normalized SQLite database engine (`bluestock_mf.db`).

---

## 📦 1. dim_fund (Dimension Table)
Represents the structural master dataset for all 40 verified mutual fund schemas.

| Column Name | Data Type | Constraint | Business Definition / Constraints |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PRIMARY KEY | Unique Association Key registered via AMFI India. |
| `fund_house` | TEXT | NOT NULL | Asset Management Company holding company identity. |
| `scheme_name` | TEXT | NOT NULL | Full official operational fund identifier. |
| `category` | TEXT | - | Asset group classification (e.g., Equity, Debt, Hybrid). |
| `sub_category` | TEXT | - | Core strategic mandate (e.g., Large Cap, Mid Cap, Small Cap, Gilt). |
| `plan` | TEXT | - | Distribution channel format tier: Direct or Regular. |
| `launch_date` | TEXT | - | Fund initiation date stamp formatted as YYYY-MM-DD. |
| `benchmark` | TEXT | - | Official benchmark tracking index (e.g., NIFTY 100 TRI). |
| `expense_ratio_pct`| REAL | - | Annual operating cost ratio bounded dynamically (0.1% - 2.5%). |
| `exit_load_pct` | REAL | - | Exit contingent load percentage fee applied on early redemption. |
| `min_sip_amount` | INTEGER | - | Minimum transactional boundary for running systematic portfolios. |
| `min_lumpsum_amount`| INTEGER | - | Minimum initial capital boundary for single one-time actions. |
| `fund_manager` | TEXT | - | Primary professional manager overseeing asset distributions. |
| `risk_category` | TEXT | - | Qualitative SEBI risk assignment tier (Low to Very High). |
| `sebi_category_code`| TEXT | - | Internal regulatory matching identifier (e.g., EC01, EC03). |

---

## 📈 2. fact_nav (Fact Table)
Tracks the historical continuous time-series trajectories for calculating returns.

| Column Name | Data Type | Constraint | Business Definition / Constraints |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Internal system row sequencer surrogate key. |
| `amfi_code` | INTEGER | FOREIGN KEY | Relational reference tracking map connecting back to `dim_fund.amfi_code`. |
| `date` | TEXT | - | ISO-8601 standardized format trading day tracker (`YYYY-MM-DD`). |
| `nav` | REAL | - | Net Asset Value valuation pricing per unit base (Validated $> 0$, forward-filled). |

---

## 💼 3. fact_transactions (Fact Table)
Captures historical transactional volume logs across demographically segmented investor nodes.

| Column Name | Data Type | Constraint | Business Definition / Constraints |
| :--- | :--- | :--- | :--- |
| `investor_id` | TEXT | - | Unique alphanumeric tracking index identifying specific retail accounts. |
| `transaction_date` | TEXT | - | Log operational timestamp formatted cleanly as YYYY-MM-DD. |
| `amfi_code` | INTEGER | FOREIGN KEY | Relational reference mapping connecting into `dim_fund.amfi_code`. |
| `transaction_type` | TEXT | - | Core operational method enum types: SIP, Lumpsum, or Redemption. |
| `amount_inr` | INTEGER | - | Value scale metric of individual cash flow actions (Validated $> 0$). |
| `state` | TEXT | - | Territorial Indian state tracking vector identifying demographic source. |
| `city` | TEXT | - | Specific municipality urban locality identification string. |
| `city_tier` | TEXT | - | Geographic operational categorization tier: T30 or B30 markers. |
| `age_group` | TEXT | - | Cohort age bracket segment tracking tags (e.g., 18-25, 26-35). |
| `gender` | TEXT | - | Demography demographic indicator value sets (Male/Female). |
| `kyc_status` | TEXT | - | Compliance screening status enum evaluation: Verified or Pending. |

---

## 📊 4. fact_performance (Fact Table)
Houses analytical metric layers and derived risk snapshots computed from time-series aggregates.

| Column Name | Data Type | Constraint | Business Definition / Constraints |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PRIMARY KEY / FOREIGN KEY | Maps directly into `dim_fund.amfi_code` to preserve relational integrity. |
| `return_1yr_pct` | REAL | - | Absolute trailing performance return calculated across a 1-year timeline. |
| `return_3yr_pct` | REAL | - | Three-year compounded annual growth rate metric expression (3Yr CAGR %). |
| `return_5yr_pct` | REAL | - | Five-year compounded annual growth rate metric expression (5Yr CAGR %). |
| `alpha` | REAL | - | Structural active return outperformance calculation relative to benchmark indices. |
| `beta` | REAL | - | Systematic volatility risk multiplier measurement relative to broader markets. |
| `sharpe_ratio` | REAL | - | Risk-adjusted structural return efficiency score calculated vs risk-free proxies. |
| `sortino_ratio` | REAL | - | Refined risk efficiency metric penalizing downside financial volatility solely. |
| `max_drawdown_pct` | REAL | - | Worst peak-to-trough historical drop valuation percentage expression. |
| `risk_grade` | TEXT | - | Categorical quality index score evaluated using metric ranking arrays. |

---

## 🏢 5. fact_aum (Fact Table)
Monitors macro assets under management growth trends for top fund houses.

| Column Name | Data Type | Constraint | Business Definition / Constraints |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Internal auto-increment row sequence tracking index. |
| `date` | TEXT | - | Financial statement publication date tracker formatted as YYYY-MM-DD. |
| `fund_house` | TEXT | - | Name identifier string tracking specific Asset Management Companies. |
| `aum_crore` | INTEGER | - | Assets Under Management scale expressed in local denominations (INR Crore). |
| `num_schemes` | INTEGER | - | Structural count of distinct active schemas managed by the AMC node. |

---

## 🏛️ 6. fact_portfolio (Fact Table)
Tracks explicit underlying asset and equity sector weight concentrations.

| Column Name | Data Type | Constraint | Business Definition / Constraints |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Internal structural sequencer surrogate key field. |
| `amfi_code` | INTEGER | FOREIGN KEY | Core relationship relational map reference linked to `dim_fund.amfi_code`. |
| `stock_symbol` | TEXT | - | Standard market ticker assignment identifier (e.g., RELIANCE, HDFCBANK). |
| `stock_name` | TEXT | - | Full legal operating name of corporate equity asset elements. |
| `sector` | TEXT | - | Macro industrial category classification (e.g., Financial Services, IT). |
| `weight_pct` | REAL | - | Allocation density factor of individual positions inside the mutual fund asset mix. |
| `market_value_cr` | REAL | - | Absolute valuation capital holding layer scaled in INR Crore metrics. |