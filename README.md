# Clinical Note Refiner

A minimal, end-to-end **LangChain RAG pipeline** that refines draft clinical notes using evidence from consult transcripts and suggests relevant clinical codes (e.g., ICD-10). Returns structured JSON output suitable for downstream systems or APIs.

The project focuses on **clarity, safety, and composable LLM pipelines**.

---

## How It Works

### 1. Note Refinement

- **Input:** Draft note + consult transcript
- **Process:** Retrieves relevant transcript excerpts using FAISS vector store
- **Output:** Refined note with:
  - Changes made
  - Missing information
  - Supporting citations

### 2. Code Suggestion

- **Input:** Refined note + clinical code reference file
- **Process:** Retrieves relevant code descriptions
- **Output:** Suggested codes with brief rationale

---

## Project Structure
```
src/
├── main.py         # Orchestrates the full pipeline
├── cli.py          # CLI parsing and validation
├── loaders.py      # Document loading, chunking, retrieval
├── chain.py        # LangChain pipelines
├── prompts.py      # Prompt templates
└── schemas.py      # Pydantic output schemas

data/
├── transcripts/
├── notes/
└── codes/
```

---

## Requirements

- **Python:** 3.10+
- **Ollama:** Local installation
- **Models:**
  - `llama3.2:3b`
  - `nomic-embed-text`

---

## Usage
```bash
python src/main.py \
  --transcript data/transcripts/consult_01.txt \
  --note data/notes/draft_note_01.txt \
  --codes data/codes/icd10.txt
```

---

## Output

The program prints a single JSON object:
```json
{
  "refined_note": {
    "note": "...",
    "changes_made": [],
    "missing_info": [],
    "citations": []
  },
  "codes": [
    {
      "code": "G44.2",
      "description": "Tension-type headache",
      "rationale": "..."
    }
  ]
}
```

---

## Design Principles

- **Selective retrieval (RAG)** over full-context injection
- **Structured outputs** validated with Pydantic
- **Composable, multi-stage chains**
- **No hallucinated clinical facts or codes**