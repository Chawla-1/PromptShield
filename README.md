# PromptShield 🛡️
> Automated Red-Teaming and Defence Iteration for LLM RAG Applications

PromptShield is a security evaluation framework and defensive hardening system built for Large Language Model (LLM) applications connected to Retrieval-Augmented Generation (RAG) pipelines. It empirically benchmarks prompt vulnerability across:
- **Direct Prompt Injections (DI)**: Instruction overrides, debug impersonations, and developer mode prompts.
- **Prompt & Canary Extraction (PE)**: Secret canary token extraction (`CANARY-7F3K9`) and internal instruction leaks.
- **Indirect Injections (II)**: Poisoned policy documents containing hidden exfiltration payloads (`VISIT-EVIL-123`).

---

## 📌 Submission Information (SCSE4041 - Milestone 2)
* **Team ID**: `PE-B-65-15`
* **Team Name**: `The Hidden Variable`
* **Batch**: `61`
* **Faculty Mentor**: `Dr. Ankit Vijay Bansal`
* **Team Members**:
  * `S24CSEU2034` - Aaryan Chawla (Team Leader)
  * `S24CSEU2598` - Vinayak Mishra
  * `S24CSEU0634` - Anmol Tyagi
  * `S24CSEU0251` - Yasharth Nagda
  * `S24CSEU2017` - Raj Kumar
* **Prototype Link**: `[Insert Streamlit Cloud URL or Colab Link]`
* **GitHub Repository**: [https://github.com/Chawla-1/PromptShield](https://github.com/Chawla-1/PromptShield)
* **Reel Link**: `[Insert Unlisted YouTube or Google Drive Link]` *(Length: 90-150s)*

---

## 📂 Repository Structure

```text
promptshield/
├── README.md               # Overview, setup guide, team details, and links
├── CHANGELOG.md            # Chronological changelog since Milestone 1
├── requirements.txt        # Python package dependencies
├── .env.example            # Environment configuration template
│
├── prompts/                # Prompt iteration repository
│   ├── v1/                 # Version 1 (Baseline prompt + user template)
│   ├── v2/                 # Version 2 (Hardened confidentiality prompt)
│   ├── v3/                 # Version 3 (Spotlighting delimiters)
│   └── final/              # Production prompt sheet & templates
│
├── code/                   # Application & evaluation source code
│   ├── app.py              # Streamlit interactive attack & defense UI
│   ├── backend.py          # Gemini API backend interface with retries
│   ├── defences.py         # Prompt engineering defense definitions (v0-v2)
│   ├── target_bot.py       # RAG bot implementation over policy docs
│   ├── judge.py            # Rule-based deterministic evaluation judge
│   ├── run_eval.py         # Batch evaluation harness
│   ├── combine.py          # Results aggregator
│   └── clean_runs.py       # Data sanitization utility
│
├── test-data/              # Test inputs and saved outputs
│   ├── attacks.json        # 30 red-team attack test cases
│   ├── benign.json         # 10 benign policy validation queries
│   └── saved_eval_outputs.csv # Evaluated results across versions
│
├── docs/                   # Diagrams, reports, and documentation
│   ├── architecture_and_diagrams.md     # Mermaid system & RAG diagrams
│   ├── milestone_2_report_draft.md      # 7-section Milestone 2 report draft
│   └── PromptShield_Technical_Report.md # Supporting Technical Report
│
├── data/policy_docs/       # Synthetic university knowledge base
│   ├── exams.txt
│   ├── fees.txt
│   ├── hostel.txt
│   └── library.txt
│
└── results/                # Evaluation run CSV logs
    └── all_runs.csv        # Comprehensive 360-trial benchmark results
```

---

## 📊 Empirical Defense Benchmark Results

Tested across 30 attack vectors $\times$ 3 stochastic runs (90 attack trials per version) using `gemini-3.1-flash-lite`:

| Defence Version | Direct Injection ASR | Indirect Injection ASR | Prompt Extraction ASR | Overall ASR (Lower is better) | Benign Accuracy (Higher is better) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **v0 (Baseline Concatenation)** | 56.7% | 80.0% | 76.7% | **71.1%** | **100.0%** |
| **v1 (Instruction Hardening)** | 10.0% | 6.7% | 0.0% | **5.6%** | **100.0%** |
| **v2 (Delimited Spotlighting)** | **0.0%** | **0.0%** | **0.0%** | **0.0%** | **100.0%** |

---

## 🚀 Quickstart & Setup

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/<your-username>/promptshield.git
cd promptshield
pip install -r requirements.txt
```

### 2. Configure Environment Secrets
Create a `.env` file in the root directory (never commit this file to git):
```bash
cp .env.example .env
```
Add your Google Gemini API Key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
PS_BACKEND=gemini
PS_GEMINI_MODEL=gemini-3.1-flash-lite
```

### 3. Run the Evaluation Benchmark
```bash
python run_eval.py --versions v0 v1 v2 --runs 3 --delay 1.0
```

### 4. Launch the Interactive Web App
```bash
streamlit run app.py
```
