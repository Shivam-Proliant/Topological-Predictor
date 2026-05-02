import os
import json
import numpy as np
import pandas as pd
import faiss
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from llama_cpp import Llama
import argparse

# --- CONFIGURATION ---
INDEX_FILE = "upsc_faiss_index.bin"
METADATA_FILE = "upsc_metadata.parquet"
OUTPUT_QUESTIONS = "adversarial_mock_test.jsonl"
MODEL_PATH = "gemma-2-2b-it-Q4_K_M.gguf"
CPU_CORES = 48
TARGET_QUESTIONS = 1000

class AntigravityEngine:
    def __init__(self):
        print("[INIT] Booting Project Antigravity Engine...")
        self.index = self._load_index()
        self.metadata = self._load_metadata()
        self.llm = self._init_llm()

    def _load_index(self):
        if not os.path.exists(INDEX_FILE):
            raise FileNotFoundError(f"Missing {INDEX_FILE}")
        return faiss.read_index(INDEX_FILE)

    def _load_metadata(self):
        if not os.path.exists(METADATA_FILE):
            raise FileNotFoundError(f"Missing {METADATA_FILE}")
        meta = pd.read_parquet(METADATA_FILE)
        
        # Categorize Source Type on-the-fly
        meta['source_type'] = meta['source'].apply(self._categorize_source)
        return meta

    def _categorize_source(self, file_path):
        path = str(file_path).lower()
        if any(k in path for k in ['pyq', 'official', '201', '202']) and 'test' not in path:
            return 'pyq'
        elif any(k in path for k in ['ca ', 'aug20', 'sep20', 'news', 'monthly', 'pt365']):
            return 'news'
        elif any(k in path for k in ['test', 'mock', 'csp', 'vision', 'insight', 'flt']):
            return 'mock'
        else:
            return 'book'

    def _init_llm(self):
        if not os.path.exists(MODEL_PATH):
            print(f"[WARNING] Local LLM not found at {MODEL_PATH}. Generation will be skipped.")
            return None
        return Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=CPU_CORES)

    def phase4_extract_hubs(self):
        """Extracts Toroidal coordinates from FAISS and clusters them."""
        print("[PHASE 4] Extracting Spatial Clusters via DBSCAN...")
        
        # Extract raw vectors to act as our spatial coordinates
        total_vectors = self.index.ntotal
        vectors = self.index.reconstruct_n(0, total_vectors)
        
        # We use the raw vectors for high-dimensional clustering
        scaler = StandardScaler()
        coords_scaled = scaler.fit_transform(vectors)
        
        dbscan = DBSCAN(eps=0.15, min_samples=15)
        self.metadata['cluster_id'] = dbscan.fit_predict(coords_scaled)
        
        # Filter Noise
        hubs = self.metadata[self.metadata['cluster_id'] != -1]
        print(f"[PHASE 4] Detected {hubs['cluster_id'].nunique()} semantic hubs.")
        return hubs

    def _calculate_probability(self, group):
        news_count = len(group[group['source_type'] == 'news'])
        pyq_count = len(group[group['source_type'] == 'pyq'])
        book_count = len(group[group['source_type'] == 'book'])
        
        # Density formula (weighted towards PYQ and News overlap)
        base_score = (news_count * 1.5) + (pyq_count * 2.0) + (book_count * 0.5)
        return pd.Series({'raw_score': base_score})

    def phase5_recalibrate_scores(self, hubs):
        """Applies Logarithmic scaling to identify Strategic Signal Centers."""
        print("[PHASE 5] Recalibrating Probability Matrix (Log-Scale)...")
        
        cluster_stats = hubs.groupby('cluster_id').apply(self._calculate_probability)
        
        # Log-transformation to handle the 'Giant Component'
        cluster_stats['log_score'] = np.log1p(cluster_stats['raw_score'])
        min_s = cluster_stats['log_score'].min()
        max_s = cluster_stats['log_score'].max()
        cluster_stats['p_log'] = ((cluster_stats['log_score'] - min_s) / (max_s - min_s)) * 100
        
        # Sort and return top hubs
        top_hubs = cluster_stats.sort_values(by='p_log', ascending=False).reset_index()
        print(f"[PHASE 5] Recalibration complete. Highest Hub Score: {top_hubs['p_log'].max():.2f}%")
        return top_hubs

    def phase6_generate_test(self, top_hubs):
        """Uses the local LLM to generate Adversarial 'Trap' questions."""
        if not self.llm:
            return
            
        print(f"[PHASE 6] Generating {TARGET_QUESTIONS} Adversarial Questions...")
        
        with open(OUTPUT_QUESTIONS, "w", encoding="utf-8") as f:
            q_count = 0
            
            # Iterate through Top 100 Hubs
            for _, hub in top_hubs.head(100).iterrows():
                hub_id = hub['cluster_id']
                p_score = hub['p_log']
                hub_data = self.metadata[self.metadata['cluster_id'] == hub_id]
                
                # Sample 10 unique contexts from this hub
                snippets = hub_data.sample(min(10, len(hub_data)))
                
                for _, snippet in snippets.iterrows():
                    if q_count >= TARGET_QUESTIONS:
                        break
                        
                    prompt = f"""<start_of_turn>user
You are a senior UPSC examiner.
Source Material: {snippet['content']}
TASK: Generate ONE multi-statement UPSC Prelims question based on this material. Include a 'Trap' statement. Provide the Answer and Explanation.
<end_of_turn>
<start_of_turn>model
"""
                    response = self.llm(prompt, max_tokens=300, stop=["<end_of_turn>"])
                    output_text = response['choices'][0]['text'].strip()
                    
                    q_data = {
                        "q_number": q_count + 1,
                        "hub_id": int(hub_id),
                        "probability_score": f"{p_score:.2f}%",
                        "content": output_text
                    }
                    f.write(json.dumps(q_data) + "\n")
                    q_count += 1
                    print(f"Generated Q.{q_count} [Hub {hub_id}]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project Antigravity: UPSC Prediction Engine")
    parser.add_argument('--run', action='store_true', help="Run the full pipeline")
    args = parser.parse_args()

    if args.run:
        engine = AntigravityEngine()
        hubs = engine.phase4_extract_hubs()
        scored_hubs = engine.phase5_recalibrate_scores(hubs)
        engine.phase6_generate_test(scored_hubs)
        print("\n[SUCCESS] Pipeline Execution Complete.")
    else:
        print("Use --run to execute the pipeline.")
