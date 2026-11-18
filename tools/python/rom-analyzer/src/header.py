# this module exclusively handles the information inside a rom header for the SNES, thinks like:
# Internal ROM title
# ROM size
# SRAM size
# Cartridge type.
# ROM version.
# Checksum.
# Complement checksum.
# Reset vector.

## read about this in python doc
from dataclasses import dataclass

@dataclass
class RomHeader:
    title: str
    rom_size: int
    sram_size: int
    cartridge_type: int
    rom_version: int
    checksum: int
    complement_checksum: int
    reset_vector: int

def read_header(rom_data: bytes, offset: int) -> RomHeader:
    pass