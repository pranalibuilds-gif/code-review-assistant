import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "demo"))

from sample_data.generator import DemoDataGenerator


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed the local database with a realistic enterprise demo dataset."
    )
    parser.add_argument(
        "--profile",
        choices=["small", "medium", "enterprise", "six_year_history"],
        default="enterprise",
        help="Select a demo profile size and timeline.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Remove existing seeded demo data before generating a fresh dataset.",
    )
    args = parser.parse_args()

    generator = DemoDataGenerator(profile_name=args.profile)
    generator.run(reset=args.reset)


if __name__ == "__main__":
    main()
