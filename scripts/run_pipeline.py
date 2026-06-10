"""
Bluestock Mutual Fund Analytics Platform — Master Pipeline Orchestrator
Author: Ganjikunta Mohan Krishna
Date: June 10, 2026

This script serves as the centralized automation hub that sequentially executes:
1. Live NAV Data Extraction & Ingestion
2. Quantitative Risk Engines (VaR, CVaR, HHI Indexes)
3. Portfolio Recommendation Filters
"""

import os
import subprocess
import sys

def execute_script(script_path):
    """Safely executes standard Python sub-pipeline modules via system shells."""
    print(f"\n Executing Script: {script_path}...")
    try:
        subprocess.run([sys.executable, script_path], check=True)
        print(f" Successfully finished: {script_path}")
    except subprocess.CalledProcessError as e:
        print(f" Execution failed at {script_path}. Error: {e}")
        sys.exit(1)

def execute_notebook_natively(notebook_path):
    """Executes a Jupyter notebook natively using the Python API to bypass CLI path bugs."""
    print(f"\n Executing Notebook Natively: {notebook_path}...")
    try:
        import nbformat
        from nbconvert.preprocessors import ExecutePreprocessor
        
        # Read the notebook file safely
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
            
        # Configure the execution preprocessor (10-minute timeout per cell)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        
        # Run the notebook cells sequentially in its local directory context
        notebook_dir = os.path.dirname(notebook_path) or '.'
        ep.preprocess(nb, {'metadata': {'path': notebook_dir}})
        
        # Save the executed notebook back to disk so output cells display live results
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
            
        print(f" Successfully executed and updated notebook cells: {notebook_path}")
    except Exception as e:
        print(f" Notebook Execution Failed.\nDetails: {str(e)}")
        sys.exit(1)

def main():
    print("======================================================================")
    print("  STARTING BLUESTOCK MUTUAL FUND ANALYTICS MASTER PIPELINE ")
    print("======================================================================")
    
    # 1. Live NAV Data Extraction & Ingestion
    step_1 = "scripts/live_nav_fetch.py"
    if os.path.exists(step_1):
        execute_script(step_1)
    else:
        print(f" Warning: Target file {step_1} not found in workspace. Skipping.")

    # 2. Quantitative Risk Engines (Executed Natively to bypass nbconvert path errors)
    step_2 = "notebooks/Advanced_Analytics.ipynb"
    if os.path.exists(step_2):
        execute_notebook_natively(step_2)
    else:
        print(f" Warning: Target file {step_2} not found in workspace. Skipping.")

    # 3. Portfolio Recommendation Filters
    step_3 = "scripts/recommender.py"
    if os.path.exists(step_3):
        execute_script(step_3)
    else:
        print(f" Warning: Target file {step_3} not found in workspace. Skipping.")

    print("\n======================================================================")
    print("  ALL DATA ENGINEERING AND QUANT PIPELINES EXECUTED SUCCESSFULLY!")
    print("======================================================================")

if __name__ == "__main__":
    main()