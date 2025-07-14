"""
Convert synthetic_queries.json to a simple CSV with only the query field
For comparison with requests.csv
"""

import json
import pandas as pd
import os

def json_to_csv():
    """Convert synthetic queries JSON to simple CSV format"""
    
    print("🔄 Converting synthetic_queries.json to CSV...")
    
    # Read the JSON file
    json_path = "synthetic_queries.json"
    csv_path = "synthetic_queries.csv"
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract just the queries
        queries = []
        for item in data['synthetic_queries']:
            queries.append({'query': item['query']})
        
        # Create DataFrame and save as CSV
        df = pd.DataFrame(queries)
        df.to_csv(csv_path, index=False)
        
        print(f"✅ Successfully converted {len(queries)} queries to CSV")
        print(f"📄 Saved to: {csv_path}")
        
        # Show preview
        print("\n🎯 Preview of generated CSV:")
        print("-" * 50)
        for i, query in enumerate(queries[:5], 1):
            print(f"{i}. {query['query']}")
        
        if len(queries) > 5:
            print(f"... and {len(queries) - 5} more queries")
            
        return csv_path
        
    except Exception as e:
        print(f"❌ Error converting to CSV: {e}")
        return None

if __name__ == "__main__":
    json_to_csv()
