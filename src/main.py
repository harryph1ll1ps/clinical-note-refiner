from pathlib import Path
from cli import parse_args
from loaders import build_chunk_retriever
from chain import build_refinement_chain, build_code_retrieval_chain
import json


def main():
    args = parse_args()

    # build the refined note
    draft_note_text = args.note.read_text(encoding="utf-8")
    transcript_retriever = build_chunk_retriever(args.transcript)
    refinement_chain = build_refinement_chain(transcript_retriever)
    refined_note = refinement_chain.invoke(draft_note_text)

    # determine the relevant codes in the refined note
    code_retriever = build_chunk_retriever(args.codes)
    code_retrieval_chain = build_code_retrieval_chain(code_retriever)
    codes = code_retrieval_chain.invoke(refined_note.refined_note)

    # return a JSON object with the results
    result = {
        "refined_note": {
            "note": refined_note.refined_note,
            "changes_made": refined_note.changes_made,
            "missing_info": refined_note.missing_info,
            "citations": refined_note.citations,
        },

        "codes": [
            {
                "code": c.code,
                "description": c.description,
                "rationale": c.rationale,
            }
            for c in codes.suggested_codes
        ],
    }

    print(json.dumps(result,indent=2))



if __name__ == "__main__":
    main()