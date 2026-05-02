import pandas as pd
import faiss
import os
import numpy as np
from sklearn.cluster import DBSCAN

# Load assets
index_path = "upsc_faiss_index.bin"
meta_path = "upsc_metadata.parquet"

if not os.path.exists(index_path):
    print(f"Error: {index_path} not found.")
    exit(1)
if not os.path.exists(meta_path):
    print(f"Error: {meta_path} not found.")
    exit(1)

print("Loading index and metadata...")
index = faiss.read_index(index_path)
meta = pd.read_parquet(meta_path)

# --- NEW: Source Categorization ---
def categorize_source(file_path):
    # Ensure lowercase for consistent matching
    path = str(file_path).lower()
    
    # 1. Actual Previous Year Questions (The Ground Truth)
    if any(k in path for k in ['pyq', 'official', '201', '202']) and 'test' not in path:
        return 'pyq'
    
    # 2. Current Affairs & Magazines (The Dynamic Signal)
    elif any(k in path for k in ['ca ', 'aug20', 'sep20', 'news', 'monthly', 'pt365']):
        return 'news'
    
    # 3. Mock Tests (The Proxy Signal)
    elif any(k in path for k in ['test', 'mock', 'csp', 'vision', 'insight', 'flt']):
        return 'mock'
    
    # 4. Everything else is Static Theory
    else:
        return 'book'

print("Categorizing sources...")
meta['source_type'] = meta['source'].apply(categorize_source)
print("Source type distribution:")
print(meta['source_type'].value_counts())

# --- Clustering Logic ---
if 'cluster_id' not in meta.columns:
    print("Performing DBSCAN clustering to generate 'cluster_id'...")
    vectors = index.reconstruct_n(0, index.ntotal)
    # DBSCAN on cosine distance
    clustering = DBSCAN(eps=0.15, min_samples=5, metric='cosine', n_jobs=-1).fit(vectors)
    meta['cluster_id'] = clustering.labels_
    print("Clustering complete.")

# Save updated metadata with cluster_id and source_type
meta.to_parquet(meta_path)
print("Metadata updated and saved.")


# 2. Identify dense 'Hubs'
print("Identifying top clusters...")
clusters_only = meta[meta['cluster_id'] != -1]
top_clusters = clusters_only['cluster_id'].value_counts().head(100).index

# 3. Extract a 'Knowledge Packet' for each Hub
output_file = "probability_packets.txt"
print(f"Writing packets to {output_file}...")
with open(output_file, "w", encoding='utf-8-sig') as f:
    for cid in top_clusters:
        neighborhood = meta[meta['cluster_id'] == cid]
        if neighborhood.empty:
            continue
        
        f.write(f"=== HUB ID: {cid} ===\n")
        # Metadata info
        source = neighborhood['source'].iloc[0] if 'source' in neighborhood.columns else "N/A"
        stype = neighborhood['source_type'].iloc[0] if 'source_type' in neighborhood.columns else "N/A"
        
        f.write(f"METADATA: {source} (Type: {stype})\n")
        # Combine content
        if 'content' in neighborhood.columns:
            clean_content = neighborhood['content'].str.cat(sep=' ')
            clean_content = "".join(c for c in clean_content if c.isprintable() or c in "\n\r\t")
        else:
            clean_content = "N/A"
            
        f.write(f"CORE CONTENT: {clean_content}\n\n")

print(f"Successfully processed {len(top_clusters)} clusters.")
print(f"Packets saved to {output_file}")
print("Done!")
