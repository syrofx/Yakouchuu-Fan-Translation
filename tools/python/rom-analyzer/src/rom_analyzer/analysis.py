# orquestator for all the other backend modules
# Read ROM
# Determine its mapping.
# Read its header.
# Consolidate results.

from pathlib import Path
from rom_analyzer.header import print_info_text, read_header


def analyze_rom(path: str) -> None:
    rom = Path(path).read_bytes()
    header = read_header(rom, 0x7FC0)
    print_info_text(header)