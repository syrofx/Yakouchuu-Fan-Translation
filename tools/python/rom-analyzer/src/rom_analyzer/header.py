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
from enum import Enum, IntEnum

class MapModes(Enum):
    LO_ROM    = 0,
    HI_ROM    = 1,
    S_DD1     = 2,
    SA_1      = 3,
    EX_HI_ROM = 4,
    SPC_7110  = 5

class Speed(Enum):
    SLOW = 0,
    FAST = 1

class Chipset(Enum):
    ROM_ONLY                    = 0x0,
    ROM_RAM                     = 0x1,
    ROM_RAM_BATTERY             = 0x2,
    ROM_COPROCESSOR             = 0x3,
    ROM_COPROCESSOR_RAM         = 0x4,
    ROM_COPROCESSOR_RAM_BATTERY = 0x5,
    ROM_COPROCESSOR_BATTERY     = 0x6,

class ChipsetCoprocessor(IntEnum):
    COPROCESSOR_DSP             = 0x0,
    COPROCESSOR_GSU             = 0x1,
    COPROCESSOR_OBC1            = 0x2,
    COPROCESSOR_SA1             = 0x3,
    COPROCESSOR_SDD1            = 0x4,
    COPROCESSOR_SRTC            = 0x5,
    COPROCESSOR_OTHER           = 0xE,
    COPROCESSOR_CUSTOM          = 0xF

class CustomCoprocessor(Enum):
    SPC_7110    = 0,
    ST010_ST011 = 1,
    ST018       = 2,
    CX4         = 3,
    NA          = 4

CHIPSET_NAMES = {
    Chipset.ROM_ONLY: "ROM only",
    Chipset.ROM_RAM: "ROM + RAM",
    Chipset.ROM_RAM_BATTERY: "ROM + RAM + battery",
    Chipset.ROM_COPROCESSOR: "ROM + coprocessor",
    Chipset.ROM_COPROCESSOR_RAM: "ROM + coprocessor + RAM",
    Chipset.ROM_COPROCESSOR_RAM_BATTERY: "ROM + coprocessor + RAM + battery",
    Chipset.ROM_COPROCESSOR_BATTERY: "ROM + coprocessor + RAM",
}

COPROCESSOR_NAMES = {
    ChipsetCoprocessor.COPROCESSOR_DSP: "DSP",
    ChipsetCoprocessor.COPROCESSOR_GSU: "GSU (SuperFX)",
    ChipsetCoprocessor.COPROCESSOR_OBC1: "OBC1",
    ChipsetCoprocessor.COPROCESSOR_SA1: "SA-1",
    ChipsetCoprocessor.COPROCESSOR_SDD1: "S-DD1",
    ChipsetCoprocessor.COPROCESSOR_SRTC: "S-RTC",
    ChipsetCoprocessor.COPROCESSOR_OTHER: "Other",
    ChipsetCoprocessor.COPROCESSOR_CUSTOM: "Custom"
}

CUSTOM_COPROCESSOR_NAMES = {
    CustomCoprocessor.SPC_7110: "SPC7110",
    CustomCoprocessor.ST010_ST011: "ST010/ST011",
    CustomCoprocessor.ST018: "ST018",
    CustomCoprocessor.CX4: "CX4",
    CustomCoprocessor.NA: "NA",
}

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
    header_data = RomHeader(
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

    return header_data

def get_info_text(header: RomHeader) -> None:
    # make this 3 to follow the same pattern as chipset, rom_size, ram_size
    title = header.title.decode("shift_jis", errors="replace").rstrip("\x00 ")
    map_mode = header.map_mode
    mode, speed = parse_map_mode(map_mode)


    chipset  = get_cartridge_description(header.chipset)
    rom_size = get_rom_ram_size_description(header.rom_size)
    ram_size = get_rom_ram_size_description(header.ram_size)

    print(f"ROM Title: {title}")
    print(f"Map mode: {mode.name}")
    print(f"Speed: {speed.name}")
    print(f"{chipset}")
    print(f"{rom_size}")
    print(f"{ram_size}")

def parse_map_mode(raw_map_mode):
    map_mode_mask = 0x0F
    speed_mask =  1 << 6

    selected_mode = 0x0
    speed_mode    = 0x0

    if (raw_map_mode & map_mode_mask == 0x0):
        selected_mode = MapModes.LO_ROM
    if (raw_map_mode & map_mode_mask == 0x1):
        selected_mode = MapModes.HI_ROM
    if (raw_map_mode & map_mode_mask == 0x2):
        selected_mode = MapModes.S_DD1
    if (raw_map_mode & map_mode_mask == 0x3):
        selected_mode = MapModes.SA_1
    if (raw_map_mode & map_mode_mask == 0x5):
        selected_mode = MapModes.EX_HI_ROM
    if (raw_map_mode & map_mode_mask == 0xA):
        selected_mode = MapModes.SPC_7110

    if (raw_map_mode & speed_mask == 0):
        speed_mode = Speed.SLOW
    if (raw_map_mode & speed_mask == 1):
        speed_mode = Speed.FAST

    return selected_mode, speed_mode

def decode_cartridge_type(value: int):
    chipset = (value >> 4) & 0x0F
    coprocessor = value & 0x0F

    return Chipset(chipset), ChipsetCoprocessor(coprocessor)

def decode_custom_coprocessor():
    pass

def get_cartridge_description(value: int) -> str:
        if (value == 0x00):
            return (f"Chipset: {CHIPSET_NAMES[Chipset.ROM_ONLY]}")
        elif (value == 0x01):
            return (f"Chipset: {CHIPSET_NAMES[Chipset.ROM_RAM]}")
        elif (value == 0x02):
            return (f"Chipset: {CHIPSET_NAMES[Chipset.ROM_RAM_BATTERY]}")
        else:
            chipset, chipset_coprocessor = decode_coprocessor_cartridge_type(value)
            if (chipset_coprocessor == ChipsetCoprocessor.COPROCESSOR_CUSTOM):
                # todo - handle the custom coprocessor decoding
                print("Not yet supported")
            return (f"Chipset: {CHIPSET_NAMES[chipset]}, Coprocessor: {COPROCESSOR_NAMES[chipset_coprocessor]}")

def get_rom_ram_size_description(value: int) -> str:
    size = 1 << value
    return f"Size: {size}Kb"

def get_country_code_description(value: int) -> str:
    # todo implement this, very similiar to the chipset one, using a table for names and an enum
    pass