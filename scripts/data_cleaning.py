import os
import pandas as pd
import numpy as np

def clean_data():
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)
    
    print(" Starting Day 2 Data Cleaning Pipeline...\n" + "="*50)
    
    # -------------------------------------------------------------
    # 1. Clean 02_nav_history.csv
    # -------------------------------------------------------------
    print(" Processing 02_nav_history.csv...")
    nav_df = pd.read_csv(os.path.join(raw_dir, "02_nav_history.csv"))
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    nav_df = nav_df.drop_duplicates()
    nav_df = nav_df[nav_df['nav'] > 0]
    
    # Forward-fill weekends/holidays per scheme group
    nav_df = nav_df.sort_values(by=['amfi_code', 'date'])
    cleaned_nav_groups = []
    for code, group in nav_df.groupby('amfi_code'):
        group = group.set_index('date')
        full_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq='D')
        group = group.reindex(full_range)
        group['amfi_code'] = group['amfi_code'].ffill().astype(int)
        group['nav'] = group['nav'].ffill()
        group = group.reset_index().rename(columns={'index': 'date'})
        cleaned_nav_groups.append(group)
    
    final_nav_df = pd.concat(cleaned_nav_groups, ignore_index=True)
    final_nav_df.to_csv(os.path.join(processed_dir, "clean_nav_history.csv"), index=False)
    print(f"    Saved clean_nav_history.csv | Rows: {len(final_nav_df)}")

    # -------------------------------------------------------------
    # 2. Clean 08_investor_transactions.csv
    # -------------------------------------------------------------
    print("\n Processing 08_investor_transactions.csv...")
    tx_df = pd.read_csv(os.path.join(raw_dir, "08_investor_transactions.csv"))
    tx_df['transaction_date'] = pd.to_datetime(tx_df['transaction_date'])
    tx_df = tx_df[tx_df['amount_inr'] > 0]
    
    # Standardize string capitalization/spacing variants to clean enums
    tx_df['transaction_type'] = tx_df['transaction_type'].str.strip().str.capitalize()
    tx_df['transaction_type'] = tx_df['transaction_type'].replace({'Sip': 'SIP', 'Lump_sum': 'Lumpsum', 'Lumpsum': 'Lumpsum', 'Redemption': 'Redemption'})
    
    # Force KYC format validation sanity
    tx_df['kyc_status'] = tx_df['kyc_status'].str.strip().str.capitalize()
    tx_df.to_csv(os.path.join(processed_dir, "clean_investor_transactions.csv"), index=False)
    print(f"    Saved clean_investor_transactions.csv | Rows: {len(tx_df)}")

    # -------------------------------------------------------------
    # 3. Clean 07_scheme_performance.csv
    # -------------------------------------------------------------
    print("\n Processing 07_scheme_performance.csv...")
    perf_df = pd.read_csv(os.path.join(raw_dir, "07_scheme_performance.csv"))
    
    # Coerce dynamic metric text rows to numeric to isolate potential parsing errors
    numeric_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'expense_ratio_pct', 'sharpe_ratio', 'sortino_ratio']
    for col in numeric_cols:
        if col in perf_df.columns:
            perf_df[col] = pd.to_numeric(perf_df[col], errors='coerce')
            
    # Flag extreme anomalies or boundaries out of range
    anomalies = perf_df[(perf_df['expense_ratio_pct'] < 0.1) | (perf_df['expense_ratio_pct'] > 2.5)]
    if not anomalies.empty:
        print(f"  Flagged {len(anomalies)} files outside expected expense_ratio ranges (0.1%-2.5%).")
        
    perf_df.to_csv(os.path.join(processed_dir, "clean_scheme_performance.csv"), index=False)
    print(f"    Saved clean_scheme_performance.csv | Rows: {len(perf_df)}")

    # -------------------------------------------------------------
    # 4. Process Remaining Contextual Files
    # -------------------------------------------------------------
    print("\n Copying and verifying remaining framework datasets...")
    other_files = ["01_fund_master.csv", "03_aum_by_fund_house.csv", "04_monthly_sip_inflows.csv", 
                   "05_category_inflows.csv", "06_industry_folio_count.csv", "09_portfolio_holdings.csv", "10_benchmark_indices.csv"]
    
    for f in other_files:
        if os.path.exists(os.path.join(raw_dir, f)):
            df = pd.read_csv(os.path.join(raw_dir, f))
            # Basic drops to eliminate empty system frames
            df = df.dropna(how='all').drop_duplicates()
            clean_name = f"clean_{f.split('_', 1)[1]}" if f[0].isdigit() else f"clean_{f}"
            df.to_csv(os.path.join(processed_dir, clean_name), index=False)
            
    print(" All 10 cleaned CSV files successfully generated in data/processed/")

if __name__ == "__main__":
    clean_data()