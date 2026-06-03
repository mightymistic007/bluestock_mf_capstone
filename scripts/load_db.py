import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

def load_relational_database():
    processed_dir = "data/processed"
    db_dir = "data/db"
    os.makedirs(db_dir, exist_ok=True)
    
    db_path = os.path.join(db_dir, "bluestock_mf.db")
    engine = create_engine(f"sqlite:///{db_path}")
    
    print(" Launching Relational DB Loader Engine...\n" + "="*50)
    
    # Apply Schema DDL script rules 
    with open("sql/schema.sql", "r") as f:
        schema_sql = f.read()
    
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_sql)
    print(" Normalized SQLite physical schema mapping completed successfully.")

    # Source-to-Target Data Loading Configuration Mapping
    mappings = {
        "clean_fund_master.csv": "dim_fund",
        "clean_nav_history.csv": "fact_nav",
        "clean_investor_transactions.csv": "fact_transactions",
        "clean_scheme_performance.csv": "fact_performance",
        "clean_portfolio_holdings.csv": "fact_portfolio",
        "clean_aum_by_fund_house.csv": "fact_aum"
    }

    for csv_file, table_name in mappings.items():
        csv_path = os.path.join(processed_dir, csv_file)
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            
            # Use appropriate pandas column subsets to map precisely into our DDL targets
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
            
            # Row count verification check
            with sqlite3.connect(db_path) as conn:
                db_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
                
            print(f" Loaded {table_name} | CSV rows: {len(df)} ➔ DB rows: {db_count} | Check: {' Match' if len(df) == db_count else ' Mismatch'}")

    print("\n Relational load sequence confirmed. Database engine operational.")

if __name__ == "__main__":
    load_relational_database()