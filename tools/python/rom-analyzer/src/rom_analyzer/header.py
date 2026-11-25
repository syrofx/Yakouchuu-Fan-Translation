# this module exclusively handles the information inside a rom header for the SNES, given a known offset it gives you thinks like:
# Internal ROM title
# ROM size
# SRAM size
# Cartridge type.
# ROM version.
# Checksum.
# Complement checksum.
# Reset vector.

# this module does not search for a header it only interprets a header give a known offset or return an error if no header can be interpreted from there.


# tl;dr 
# 1.-read corresponding bytes to the header
# 2.- Present that in a legible way

## read about this in python doc
from dataclasses import dataclass
from enum import Enum

class MapModes(Enum):
    LO_ROM    = 0,
    HI_ROM    = 1,
    S_DD1     = 2,
    SA_1      = 3,
    EX_HI_ROM = 4,
    SPC_7110  = 5

class Speed(Enums)
    Slow = 0,
    Fast = 1

@dataclass
class RomHeader:
    title: int
    map_mode: int
    chipset: int
    rom_size: int
    ram_size: int
    country_code: int
    developer_id: int
    rom_version: int
    complement_checksum: int
    checksum: int
    interrupt_vectors: int

def read_header(rom_data: bytes, offset: int) -> RomHeader:
    entry = RomHeader(
        title               = rom_data[offset + 0x0 : offset + 0x15],
        map_mode            = rom_data[offset + 0x15],
        chipset             = rom_data[offset + 0x16],
        rom_size            = rom_data[offset + 0x17],
        ram_size            = rom_data[offset + 0x18],
        country_code        = rom_data[offset + 0x19],
        developer_id        = rom_data[offset + 0x1A],
        rom_version         = rom_data[offset + 0x1B],
        complement_checksum = rom_data[offset + 0x1C : offset + 0x1D],
        checksum            = rom_data[offset + 0x1E : offset + 0x1F],
        interrupt_vectors   = rom_data[offset + 0x20]
    )

    return entry

def get_info_text(header: RomHeader) -> None:
    title = header.title.decode("shift_jis", errors="replace").rstrip("\x00 ")
    map_mode = header.map_mode


    print(f"ROM Title: {title}")
    parse_map_mode(map_mode)
    #print(f"Map mode: {bin(header.map_mode)}")


def parse_map_mode(raw_map_mode):
    map_mode_mask = 0x0F
    if (raw_map_mode & map_mode_mask = 0x0)


