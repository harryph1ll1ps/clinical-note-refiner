from pathlib import Path
from cli import parse_args
from loaders import build_chunk_retriever
from chain import build_refinement_chain


def main():
    args = parse_args()

    draft_note_text = args.note.read_text(encoding="utf-8")

    retriever = build_chunk_retriever(args.transcript)
    chain = build_refinement_chain(retriever)

    result = chain.invoke(draft_note_text)

    print("\n=== REFINED NOTE ===\n")
    print(result.refined_note)

    print("\n=== CHANGES MADE ===\n")
    for change in result.changes_made:
        print(f"- {change}")

    print("\n=== MISSING INFORMATION ===\n")
    for item in result.missing_info:
        print(f"- {item}")

    print("\n=== CITATIONS ===\n")
    for citation in result.citations:
        print(f"- {citation}")


if __name__ == "__main__":
    main()