# Project  Topological Prediction Engine

Project y is an advanced, CPU-optimized predictive engine designed to forecast high-probability questions for the Objective Examinations. 

Rather than relying on simple keyword matching or standard LLM generation, this architecture maps 15 years of static syllabus data (Textbooks) and dynamic data (Current Affairs, PYQs) onto a **Non-Euclidean Toroidal Manifold**. By calculating the semantic gravity between these data points, the engine identifies dense "Question Hubs" to generate an adversarial mock test.

##  The Mathematics \

1. **Dimensionless Relational Space:** Instead of standard Euclidean vectors, the engine relies on the relative topological distance between text chunks using `FAISS` (HNSW graphs), allowing infinite hierarchical depth.
2. **Toroidal Geometry:** The UPSC syllabus is cyclical (themes repeat over years). The data is mapped to a 3D Torus, where the inner ring represents the static core syllabus and the outer ring represents dynamic current affairs.
3. **Statistical Hub Extraction:** The engine utilizes **DBSCAN** (Density-Based Spatial Clustering) to locate "Semantic Hotspots" where Historical Patterns (PYQs) physically collide with Current Events (News).
4. **Logarithmic Probability Matrix:** To prevent the "Giant Component" of generic syllabus topics from skewing the results, a Logarithmic Min-Max scaling is applied, elevating high-yield, specific "Signal Centers" (e.g., Quantum Tech, Constitutional Articles) to a 90%+ probability threshold.

##  System Architecture

This project is specifically optimized for a **high-core, zero-GPU server environment** (e.g., 48 vCPUs, 58 GB RAM).

*   **Ingestion:** `PyMuPDF4LLM` + `Ray` (Multiprocessing for semantic header chunking).
*   **Vectorization:** `Nomic-Embed-Text-v1.5` running via `ONNX Runtime` for bare-metal AVX2 CPU acceleration.
*   **Manifold Mapping:** `FAISS` and `UMAP`.
*   **Adversarial Generation:** Local `Gemma 27B` via `llama.cpp` using Contrastive Prompting to generate multi-statement "Trap" questions.

##  Quick Start (Server Deployment)

### 1. Prerequisites
Ensure you are running a Debian/Ubuntu server with Python 3.10+.
```bash
pip install pandas numpy scikit-learn faiss-cpu llama-cpp-python
```

### 2. Required Assets
Place the following compiled files in the root directory:
*   `upsc_faiss_index.bin` (The Semantic Graph)
*   `upsc_metadata.parquet` (The Data Chunks)
*   `gemma-2-2b-it-Q4_K_M.gguf` (The Local Examiner Model)

### 3. Execution
Run the master script to extract the topological hubs, calculate the probability matrix, and generate the 1,000-question test batch.
```bash
python3 antigravity_engine.py --run
```

##  Output
The engine generates `adversarial_mock_test.jsonl`. Each entry contains:
*   The Question, Options, and Answer.
*   The "Trap" Justification (Why the AI designed a specific misleading statement based on UPSC trends).
*   The Deterministic Probability Score (The mathematical chance of appearance in the upcoming cycle).

##  License
MIT License.
