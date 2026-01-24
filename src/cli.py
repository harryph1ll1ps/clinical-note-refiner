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

    return parser.parse_args()


if __name__ == "__main__":
    parse_args()