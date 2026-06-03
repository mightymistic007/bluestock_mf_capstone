-- Day 2 Assignment: 10 Analytical Strategic Queries

-- Query 1: Top 5 Funds by aggregate AUM values
SELECT amfi_code, scheme_name, aum_crore 
FROM fact_performance
JOIN dim_fund USING (amfi_code)
ORDER BY aum_crore DESC 
LIMIT 5;

-- Query 2: Average net asset value (NAV) computed month-by-month
SELECT STRFTIME('%Y-%m', date) as month_period, AVG(nav) as average_nav
FROM fact_nav
GROUP BY month_period
ORDER BY month_period ASC;

-- Query 3: Structural check on funds carrying an expense ratio beneath 1%
SELECT amfi_code, scheme_name, expense_ratio_pct 
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- Query 4: Transaction density grouped by territorial Indian state metrics
SELECT state, COUNT(*) as transaction_volume, SUM(amount_inr) as total_invested_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_invested_inr DESC;

-- Query 5: Identifying Top 3 sectors held across active portfolios
SELECT sector, ROUND(SUM(weight_pct), 2) as aggregated_weight_pct
FROM fact_portfolio
GROUP BY sector
ORDER BY aggregated_weight_pct DESC
LIMIT 3;

-- Query 6: High-Risk high-return options (Sharpe Ratio > 1.2 sorted by alpha)
SELECT amfi_code, scheme_name, sharpe_ratio, alpha
FROM fact_performance
JOIN dim_fund USING (amfi_code)
WHERE sharpe_ratio > 1.2
ORDER BY alpha DESC;

-- Query 7: Distribution breakdown of transaction payment channels
SELECT transaction_type, COUNT(*) as volume, SUM(amount_inr) as absolute_inr
FROM fact_transactions
GROUP BY transaction_type;

-- Query 8: Average asset size of Top fund houses
SELECT fund_house, AVG(aum_crore) as baseline_amc_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY baseline_amc_aum DESC;

-- Query 9: Core underperforming tracking systems (Negative Alpha metrics)
SELECT amfi_code, scheme_name, alpha, risk_grade
FROM fact_performance
JOIN dim_fund USING (amfi_code)
WHERE alpha < 0
ORDER BY alpha ASC;

-- Query 10: Structural KYC onboarding compliance ratios
SELECT kyc_status, COUNT(*) as total_investors, 
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM fact_transactions), 2) as ratio_pct
FROM fact_transactions
GROUP BY kyc_status;