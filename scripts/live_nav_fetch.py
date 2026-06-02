import os
import requests
import pandas as pd

def fetch_and_save_nav(scheme_code, scheme_name):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"🌐 Contacting API for: {scheme_name} ({scheme_code})...")
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            meta = data.get('meta', {})
            nav_history = data.get('data', [])
            
            if not nav_history:
                print(f" No data array found for {scheme_name}.")
                return
                
            df = pd.DataFrame(nav_history)
            df['scheme_code'] = scheme_code
            df['scheme_name'] = meta.get('scheme_name', scheme_name)
            df['fund_house'] = meta.get('fund_house', 'Unknown')
            
            output_filename = f"data/raw/nav_{scheme_code}.csv"
            df.to_csv(output_filename, index=False)
            print(f" Saved: {output_filename} ({len(df)} rows)")
        else:
            print(f" Failed. HTTP Status: {response.status_code}")
    except Exception as e:
        print(f" Connection error for {scheme_code}: {e}")

if __name__ == "__main__":
    schemes = {
        "125497": "HDFC Top 100 Direct",
        "119551": "SBI Bluechip",
        "120503": "ICICI Bluechip",
        "118632": "Nippon Large Cap",
        "119092": "Axis Bluechip",
        "120841": "Kotak Bluechip"
    }
    for code, name in schemes.items():
        fetch_and_save_nav(code, name)