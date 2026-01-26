from pathlib import Path
from cli import parse_args
from loaders import build_chunk_retriever
from chain import build_refinement_chain, build_code_retrieval_chain


def main():
    args = parse_args()

    # build the refined note and print results
    draft_note_text = args.note.read_text(encoding="utf-8")
    transcript_retriever = build_chunk_retriever(args.transcript)
    refinement_chain = build_refinement_chain(transcript_retriever)
    refined_note = refinement_chain.invoke(draft_note_text)


    print("\n=== *** PART 1 *** ===\n")
    print("\n=== REFINED NOTE ===\n")
    print(refined_note.refined_note)

    print("\n=== CHANGES MADE ===\n")
    for change in refined_note.changes_made:
        print(f"- {change}")

    print("\n=== MISSING INFORMATION ===\n")
    for item in refined_note.missing_info:
        print(f"- {item}")

    print("\n=== CITATIONS ===\n")
    for citation in refined_note.citations:
        print(f"- {citation}")



    # determine the relevant codes in the refined note and print results
    code_retriever = build_chunk_retriever(args.codes)
    code_retrieval_chain = build_code_retrieval_chain(code_retriever)
    codes = code_retrieval_chain.invoke(refined_note.refined_note)

    print("\n=== *** PART 2 *** ===\n")
    for i, code in enumerate(codes.suggested_codes):
        print(f"\n=== CODE {i + 1} ===\n")
        print(f"Code: {code.code}")
        print(f"Description: {code.description}")
        print(f"Rationale: {code.rationale}")



if __name__ == "__main__":
    main()