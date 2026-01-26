import argparse
from pathlib import Path


def parse_args():
    """
    CLI argument parsing
    """
    parser = argparse.ArgumentParser(
        description="Refine a clinical note using a consult transcript."
    )

    parser.add_argument(
        "--transcript",
        type=Path,
        required=True,
        help="Path to the consult transcript (.txt)",
    )

    parser.add_argument(
        "--note",
        type=Path,
        required=True,
        help="Path to the draft clinical note (.txt)",
    )

    parser.add_argument(
        "--codes",
        type=Path,
        required=True,
        help="Path to a clinical codes reference file (.txt)",
    )

    args = parser.parse_args()

    if not args.transcript.exists():
        parser.error(f"Transcript file not found: {args.transcript}")

    if not args.note.exists():
        parser.error(f"Note file not found: {args.note}")

    if not args.codes.exists():
        parser.error(f"Codes file not found: {args.codes}")

    return args




if __name__ == "__main__":
    parse_args()