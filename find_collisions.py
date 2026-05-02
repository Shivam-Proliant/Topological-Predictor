import pandas as pd

meta = pd.read_parquet('upsc_metadata.parquet')
news_clusters = meta[meta['source_type'] == 'news']['cluster_id'].unique()

collision_data = []
for cid in news_clusters:
    if cid == -1:
        continue
    cluster = meta[meta['cluster_id'] == cid]
    if (cluster['source_type'] == 'pyq').any():
        collision_data.append({
            'cluster_id': cid,
            'news_count': len(cluster[cluster['source_type'] == 'news']),
            'pyq_count': len(cluster[cluster['source_type'] == 'pyq']),
            'themes': cluster['content'].iloc[0][:100] # preview
        })

df = pd.DataFrame(collision_data)
if not df.empty:
    df = df.sort_values('news_count', ascending=False)
    print(df[['cluster_id', 'news_count', 'pyq_count']].to_string(index=False))

else:
    print("No semantic collisions found between News and PYQ nodes.")
