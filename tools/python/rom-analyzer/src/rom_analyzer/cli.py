# Entry point of the application the rasponsability is:
# interpret user arguments
# validate arguments
# invoke corresponding functions
# presents results

# something like
# $ rom-analyzer analyze game.sfc
# $ rom-analyzer header game.sfc
# $ rom-analyzer mapping game.sfc

import argparse

from rom_analyzer.analysis import analyze_rom


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rom-analyzer",
        description="SNES ROM analysis utility"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a SNES ROM"
    )

    analyze_parser.add_argument(
        "rom",
        help="Path to the ROM file"
    )

    return parser

def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        analyze_rom(args.rom)


if __name__ == "__main__":
    main()