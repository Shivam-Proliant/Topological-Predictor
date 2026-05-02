import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

meta = pd.read_parquet('upsc_metadata.parquet')
clusters_only = meta[meta['cluster_id'] != -1]

# Top 100 clusters by total size
top_clusters = clusters_only['cluster_id'].value_counts().head(100).index

results = []
for cid in top_clusters:
    neighborhood = meta[meta['cluster_id'] == cid]
    
    # Calculate counts
    book_sources = neighborhood[neighborhood['source_type'] == 'book']['source'].nunique()
    pyq_count = len(neighborhood[neighborhood['source_type'] == 'pyq'])
    
    # Theme extraction
    content = neighborhood['content'].dropna().str.cat(sep=' ')
    clean_content = "".join(c for c in content if c.isprintable() or c in " ")
    
    theme = "Unknown"
    if len(clean_content) > 50:
        try:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=3)
            tfidf = vectorizer.fit_transform([clean_content])
            theme = ", ".join(vectorizer.get_feature_names_out())
        except:
            theme = "N/A"
            
    results.append({
        'Hub ID': cid,
        'Book Overlap': book_sources,
        'PYQ Count': pyq_count,
        'Theme': theme.title()
    })

df = pd.DataFrame(results)

# Calculate raw scores first
max_books_raw = df['Book Overlap'].max() if df['Book Overlap'].max() > 0 else 1
max_pyq_raw = df['PYQ Count'].max() if df['PYQ Count'].max() > 0 else 1
df['raw_score'] = ((df['Book Overlap'] / max_books_raw) * 40) + ((df['PYQ Count'] / max_pyq_raw) * 60)

# Apply Logarithmic Recalibration
df['log_score'] = np.log1p(df['raw_score'])
min_log = df['log_score'].min()
max_log = df['log_score'].max()

if max_log > min_log:
    df['Probability Score'] = ((df['log_score'] - min_log) / (max_log - min_log)) * 100
else:
    df['Probability Score'] = 100.0

df['Probability Score'] = df['Probability Score'].round(2)
df = df.sort_values('Probability Score', ascending=False)

with open('probability_matrix.md', 'w', encoding='utf-8-sig') as f:
    f.write("| Hub ID | Probability Score (Log-Scaled) | Theme | Book Overlap | PYQ Count |\n")
    f.write("|---|---|---|---|---|\n")
    for _, row in df[['Hub ID', 'Probability Score', 'Theme', 'Book Overlap', 'PYQ Count']].head(100).iterrows():
        f.write(f"| {row['Hub ID']} | {row['Probability Score']}% | {row['Theme']} | {row['Book Overlap']} | {row['PYQ Count']} |\n")

