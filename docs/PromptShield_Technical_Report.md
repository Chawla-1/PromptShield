# PromptShield: Empirical Evaluation and Hardening of LLM RAG Applications Against Prompt Injection and Extraction

**Document Type**: Technical Report (Milestone 2 Supporting Document)  
**Team ID**: PE-B-65-15  
**Team Name**: The Hidden Variable  
**Batch**: 61 | **Faculty Mentor**: Dr. Ankit Vijay Bansal  
**Authors**: Aaryan Chawla (S24CSEU2034), Vinayak Mishra (S24CSEU2598), Anmol Tyagi (S24CSEU0634), Yasharth Nagda (S24CSEU0251), Raj Kumar (S24CSEU2017)  

---

### Abstract
Large Language Model (LLM) applications connected to Retrieval-Augmented Generation (RAG) pipelines are acutely vulnerable to prompt injection, system prompt extraction, and indirect injection via untrusted retrieved documents. In this work, we present **PromptShield**, an automated red-teaming evaluation framework and defence benchmarking harness applied to an academic university policy assistant (*HelpBot*). We rigorously iterate across three architectural defence strategies: (1) baseline instructions with secret canary tokens, (2) hardened adversarial boundary instructions, and (3) XML delimiter spotlighting that partitions untrusted data from instruction streams. Across a benchmark suite of 30 distinct attack vectors tested across 3 stochastic runs (90 attack evaluations per version) using `gemini-3.1-flash-lite`, the overall Attack Success Rate (ASR) plunged from **71.1% (baseline)** to **5.6% (hardened)**, reaching **0.0% (spotlighting)**, while retaining **100% utility and accuracy** on benign policy queries.

---

### 1. Introduction & Threat Model
As academic institutions and enterprises deploy LLM-powered RAG systems, adversaries exploit the lack of structural separation between trusted instructions and untrusted data. In PromptShield, we evaluate three critical threat vectors:
1. **Direct Injection (DI)**: The user attempts to override the system instructions using authority impersonation, debug modes, or instruction reset commands.
2. **Prompt Extraction (PE)**: The adversary attempts to reconstruct confidential system instructions or extract an embedded secret canary token (`CANARY-7F3K9`).
3. **Indirect Injection (II)**: A retrieved policy document contains an injected malicious payload designed to hijack the model's objective and output an exfiltration marker (`VISIT-EVIL-123`).

---

### 2. Architectural Design & Methodology

PromptShield implements an automated red-teaming harness comprised of:
* **Retrieval Subsystem**: Token-overlap chunk ranker pulling policies across academic tuition, hostel regulations, examination procedures, and library policies from `data/policy_docs/`.
* **Multi-Tier Defence Pipeline**:
  * **v0 (Baseline)**: Permissive context concatenation.
  * **v1 (Instruction Hardening)**: Strict confidentiality boundaries and a designated safe refusal response.
  * **v2 (Delimited Spotlighting)**: Structural framing enclosing both retrieved context chunks and user questions inside explicit `<untrusted>` tags, coupled with instruction priors telling the model to treat all text within tags as purely informational data.
* **Automated Rule-Based Judge**: Deterministic detection checking for canary extraction, system prompt fragment leaks, or evil payload markers.

---

### 3. Empirical Results & Findings

| Version | Defence Approach | Direct Injection ASR | Indirect Injection ASR | Prompt Extraction ASR | Overall ASR (Lower is better) | Benign Accuracy (Higher is better) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **v0** | Baseline Concatenation | 56.7% | 80.0% | 76.7% | **71.1%** | **100.0%** |
| **v1** | Hardened Instructions | 10.0% | 6.7% | 0.0% | **5.6%** | **100.0%** |
| **v2** | XML Spotlighting | **0.0%** | **0.0%** | **0.0%** | **0.0%** | **100.0%** |

#### Key Insights:
1. **Hardened instructions alone** eliminated prompt extraction (0.0% ASR) and reduced direct injection, but occasionally succumbed to complex roleplays or nested indirect injections (5.6% overall).
2. **Spotlighting via `<untrusted>` tags** created an impermeable syntactic separation between instructions and data, completely neutralizing all 30 attack vectors without any degradation of legitimate question answering (100% benign accuracy).

---

### 4. Known Limitations & Future Work
* **Token Overhead**: Enclosing retrieved chunks in structural tags consumes additional prompt tokens.
* **Adversarial Tag Escapes**: While effective against standard delimiters, attackers may attempt to craft closing `</untrusted>` tags within their inputs; future iterations will implement server-side tag sanitization and multi-agent supervisory auditing.
