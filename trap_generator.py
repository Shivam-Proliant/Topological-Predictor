import pandas as pd
import numpy as np

# Load recalibrated data
meta = pd.read_parquet('upsc_metadata.parquet')
clusters_only = meta[meta['cluster_id'] != -1]

# Get Top 100 Hubs
top_hubs_ids = clusters_only['cluster_id'].value_counts().head(100).index

# Prepare output
mock_test_data = []

for cid in top_hubs_ids:
    hub_data = meta[meta['cluster_id'] == cid]
    # Sample 10 snippets per hub
    samples = hub_data.sample(min(10, len(hub_data)), random_state=42)
    
    for _, row in samples.iterrows():
        mock_test_data.append({
            "hub_id": int(cid),
            "source": row['source'],
            "content": row['content'][:1000] # Limit content length
        })

# Save for processing
import json
with open('hub_snippets.json', 'w', encoding='utf-8') as f:
    json.dump(mock_test_data, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(mock_test_data)} snippets from {len(top_hubs_ids)} hubs.")
