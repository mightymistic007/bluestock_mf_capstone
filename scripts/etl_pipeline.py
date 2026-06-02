import os
import pandas as pd

def profile_datasets():
    raw_dir = "data/raw"
    if not os.path.exists(raw_dir):
        print(f" Error: '{raw_dir}' folder doesn't exist.")
        return

    # Target the original datasets while ignoring the dynamic API outputs
    csv_files = [f for f in os.listdir(raw_dir) if f.endswith('.csv') and not f.startswith('nav_')]
    
    if not csv_files:
        print(" No base CSV files found in data/raw/. Please add your 10 datasets!")
        return
        
    print(f" Found {len(csv_files)} datasets to profile.\n" + "="*60)

    for file in csv_files:
        path = os.path.join(raw_dir, file)
        print(f"\n File: {file}")
        try:
            df = pd.read_csv(path)
            print(f" Shape: {df.shape}")
            print("\n Column Data Types:")
            print(df.dtypes)
            print("\n Top Rows Preview:")
            print(df.head(2))
            
            missing = df.isnull().sum().sum()
            dupes = df.duplicated().sum()
            print(f"\n Integrity Check: Missing Values: {missing} | Duplicates: {dupes}")
        except Exception as e:
            print(f" Error parsing {file}: {e}")
        print("-" * 60)

    print("\n Running AMFI Quality Integrity Validation...")
    try:
        # Standardize file lookups regardless of prefixes
        master_file = next((f for f in csv_files if "fund_master" in f), None)
        history_file = next((f for f in csv_files if "nav_history" in f), None)
        
        if master_file and history_file:
            master_df = pd.read_csv(os.path.join(raw_dir, master_file))
            history_df = pd.read_csv(os.path.join(raw_dir, history_file))
            
            print("\n Fund Master Exploration Overview:")
            for col in ['fund_house', 'category', 'sub_category', 'risk_grade', 'risk_category']:
                if col in master_df.columns:
                    print(f"   ▫️ Unique {col.replace('_', ' ').title()}s: {master_df[col].nunique()}")

            # Confirm columns match your scheme configurations
            code_col = 'amfi_code' if 'amfi_code' in master_df.columns else 'scheme_code'
            hist_code_col = 'amfi_code' if 'amfi_code' in history_df.columns else 'scheme_code'
            
            missing_codes = ~master_df[code_col].isin(history_df[hist_code_col])
            missing_count = missing_codes.sum()
            
            print("\n Data Quality Summary Report:")
            if missing_count == 0:
                print("    SUCCESS: Integrity check passed. Every master scheme code maps into nav_history.")
            else:
                print(f"    WARNING: {missing_count} master codes are completely missing from the history records.")
        else:
            print("   ℹ Validation skipped: Ensure fund_master and nav_history files are present in data/raw.")
    except Exception as e:
        print(f"    System Validation Interrupted: {e}")

if __name__ == "__main__":
    profile_datasets()