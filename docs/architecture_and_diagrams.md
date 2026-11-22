# PromptShield - System Architecture & Solution Diagrams

## 1. End-to-End System Architecture

```mermaid
flowchart TD
    User["Student / Attacker"] --> UI["Streamlit Web UI / CLI Harness"]
    UI --> TargetBot["Target Bot (RagBot)"]
    TargetBot --> Retriever["Keyword Retriever"]
    Retriever --> PolicyDocs[("Policy Docs Corpus (txt)")]
    Retriever --> PromptBuilder["Defence Prompt Builder (v0, v1, v2)"]
    PromptBuilder --> LLM["LLM Backend (Gemini 3.1 Flash-Lite)"]
    LLM --> TargetBot
    TargetBot --> UI
    UI --> Judge["Rule-Based Judge"]
    Judge --> CSV[("Results Logger (runs.csv)")]
```

## 2. RAG Pipeline Diagram

```mermaid
flowchart LR
    Q["Student Query"] --> Tokenize["Tokenize Query"]
    Tokenize --> Overlap["Word Overlap Scorer"]
    Docs[("Policy Chunks")] --> Overlap
    Overlap --> TopK["Select Top-2 Chunks"]
    TopK --> Delimiters["Wrap in <untrusted> Tags"]
    Q --> Delimiters
    Delimiters --> FinalPrompt["Spotlighted Prompt Assembly"]
    FinalPrompt --> GeminiAPI["Gemini API"]
    GeminiAPI --> Answer["Policy Answer"]
```

## 3. Prompt Evaluation & Red-Teaming Workflow

```mermaid
flowchart TD
    AttackDataset["Attack Dataset (30 attacks: DI, PE, II)"] --> Harness["run_eval.py"]
    BenignDataset["Benign Dataset (10 queries)"] --> Harness
    Harness --> Iteration["For each defence version (v0, v1, v2) x 3 runs"]
    Iteration --> RAG["Execute Prompt on Target Bot"]
    RAG --> Judge["Judge Checks: Canary / Marker / Fragment"]
    Judge --> Metrics["Compute Attack Success Rate (ASR) & Benign %"]
    Metrics --> Export["results/all_runs.csv"]
```

## 4. Input-Output Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Attacker
    participant Bot as Target Bot (RagBot)
    participant KB as Policy Knowledge Base
    participant Backend as Gemini Backend
    participant Judge as Evaluation Judge

    User->>Bot: Submit Query / Attack Prompt
    Bot->>KB: Retrieve Top Policy Chunks
    KB-->>Bot: Context Chunks
    Bot->>Backend: Send System Prompt + Delimited Context & Question
    Backend-->>Bot: Generated Completion
    Bot->>User: Display Bot Response
    Bot->>Judge: Pass Output + Attack Metadata
    Judge-->>User: Classification (BLOCKED / ATTACK SUCCEEDED)
```
