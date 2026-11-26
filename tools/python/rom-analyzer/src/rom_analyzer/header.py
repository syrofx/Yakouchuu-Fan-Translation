import sys
from dataclasses import dataclass
from enum import Enum, IntEnum

class Memory(Enum):
    ROM = 0,
    RAM = 1

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

class Region(Enum):
    JAPAN = 0x00,
    NORTH_AMERICA = 0x01,
    EUROPE = 0x02,
    SCANDINAVIA = 0x03,
    FINLAND = 0x04,
    DENMARK = 0x05,
    EUROPE_FRENCH_ONLY = 0x06,
    DUTCH = 0x07,
    SPANISH = 0x08,
    GERMAN = 0x08,
    ITALIAN = 0x0A,
    CHINESE = 0x0B,
    INDONESIA = 0x0C,
    SOUTH_KOREA = 0x0D,
    COMMON = 0x0E,
    CANADA = 0x0F,
    BRAZIL = 0x10,
    NINTENDO_GATEWAY_SYSTEM = 0x11, # to do: handle this special case by checking $FFB2 ascii game code
    AUSTRALIA = 0x12,
    OTHER_X = 0x13,
    OTHER_Y = 0x14,
    OTHER_Z = 0x15

REGION_NAMES = {
    Region.JAPAN : "Japan",
    Region.NORTH_AMERICA : "North America",
    Region.EUROPE : "Europe",
    Region.SCANDINAVIA : "Scandinavia",
    Region.FINLAND : "Finland",
    Region.DENMARK : "Denmark",
    Region.EUROPE_FRENCH_ONLY : "France",
    Region.DUTCH : "Dutchland",
    Region.SPANISH : "Spain",
    Region.GERMAN : "Germany",
    Region.ITALIAN : "Italy",
    Region.CHINESE : "Chine",
    Region.INDONESIA : "Indonesia",
    Region.SOUTH_KOREA : "South Korea",
    Region.COMMON : "Common",
    Region.CANADA : "Canada",
    Region.BRAZIL : "Brazil",
    Region.NINTENDO_GATEWAY_SYSTEM : "Nintendo Gateway System",
    Region.AUSTRALIA : "Australia",
    Region.OTHER_X : "Other variation x",
    Region.OTHER_Y : "Other variation y",
    Region.OTHER_Z : "Other variation z"
}

MAP_MODE_NAMES = {
    MapModes.LO_ROM: "LoROM",
    MapModes.HI_ROM: "HiROM",
    MapModes.S_DD1: "S-DD1",
    MapModes.SA_1: "SA-1",
    MapModes.EX_HI_ROM: "ExHiROM",
    MapModes.SPC_7110: "SPC7110"
}

SPEED_NAMES = {
    Speed.SLOW: "Low",
    Speed.FAST: "Fast"
}

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
        complement_checksum = rom_data[offset + 0x1C : offset + 0x1E],
        checksum            = rom_data[offset + 0x1E : offset + 0x20],
        interrupt_vectors   = rom_data[offset + 0x20]
    )

    return header_data

def print_info_text(header: RomHeader) -> None:
    title               = get_title_description(header.title)
    map_mode_speed      = get_map_mode_speed_description(header.map_mode)
    chipset             = get_cartridge_description(header.chipset)
    rom_size            = get_rom_ram_size_description(header.rom_size, Memory.ROM)
    ram_size            = get_rom_ram_size_description(header.ram_size, Memory.RAM)
    region              = get_region_description(header.country_code)
    developer_id        = get_developer_id_description(header.developer_id)
    rom_version         = get_rom_version_description(header.rom_version)
    checksum            = get_checksum_description(header.checksum, False)
    checksum_complement = get_checksum_description(header.complement_checksum, True)
    checksum_check      = get_checksum_check_description(int.from_bytes(header.checksum), int.from_bytes(header.complement_checksum))

    print(f"╔═════════ROM analysis═════════")
    print(f"║{title}")
    print(f"║{map_mode_speed}")
    print(f"║{chipset}")
    print(f"║{rom_size}")
    print(f"║{ram_size}")
    print(f"║{region}")
    print(f"║{developer_id}")
    print(f"║{rom_version}")
    print(f"║{checksum}")
    print(f"║{checksum_complement}")
    print(f"║{checksum_check}")

def get_title_description(value: int) -> str:
    title_decoded = value.decode("shift_jis", errors="replace").rstrip("\x00 ")
    return f"ROM Title: {title_decoded}"

def get_map_mode_speed_description(mode: MapModes) -> str:
    decoded_map_mode, decoded_speed = decode_map_mode(mode)
    return f"Map mode: {MAP_MODE_NAMES[decoded_map_mode]} \n║Speed: {SPEED_NAMES[decoded_speed]}"

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

def get_rom_ram_size_description(value: int, mem_flag: Memory) -> str:
    size = 1 << value
    if (mem_flag == Memory.ROM):
        return f"ROM size: {size}Kb"
    if (mem_flag == Memory.RAM):
        return f"RAM size: {size}Kb"

def get_region_description(value: int) -> str:
    decoded_country_code = decode_country_code(value)
    return f"Region: {REGION_NAMES[decoded_country_code]}"

def get_developer_id_description(value: int) -> str:
    return f"Developer id: \n║\tHex: {hex(value)} \n║\tDec: {value}"

def get_rom_version_description(value: int) -> str:
    if (value == 0x0):
        return f"ROM version: first"
    else:
        return f"ROM version: not first"

def get_checksum_description(value: bytes, is_complement) -> str:
    value = int.from_bytes(value, byteorder='big')

    if (is_complement):
        return f"Checksum complement: \n║\tHex: {hex(value)} \n║\tDec: {value}"
    else:
        return f"Checksum: \n║\tHex: {hex(value)} \n║\tDec:{value}"

def get_checksum_check_description(checksum: int, checksum_complement: int) -> str:
    result = checksum ^ checksum_complement
    if (result == 0xFFFF):
        return f"Checksum validation successful!"
    else:
        return f"Checksum validation failure!"

def decode_map_mode(value: int):
    map_mode_mask = 0x0F
    speed_mask =  1 << 6

    selected_mode = 0x0
    speed_mode    = 0x0

    if (value & map_mode_mask == 0x0):
        selected_mode = MapModes.LO_ROM
    if (value & map_mode_mask == 0x1):
        selected_mode = MapModes.HI_ROM
    if (value & map_mode_mask == 0x2):
        selected_mode = MapModes.S_DD1
    if (value & map_mode_mask == 0x3):
        selected_mode = MapModes.SA_1
    if (value & map_mode_mask == 0x5):
        selected_mode = MapModes.EX_HI_ROM
    if (value & map_mode_mask == 0xA):
        selected_mode = MapModes.SPC_7110

    if (value & speed_mask == 0):
        speed_mode = Speed.SLOW
    if (value & speed_mask == 1):
        speed_mode = Speed.FAST

    return selected_mode, speed_mode

def decode_cartridge_type(value: int):
    chipset = (value >> 4) & 0x0F
    coprocessor = value & 0x0F

    return Chipset(chipset), ChipsetCoprocessor(coprocessor)

def decode_custom_coprocessor(value: int):
    pass

def decode_country_code(value: int):
    if (value == 0x00):
        return Region.JAPAN
    if (value == 0x01):
        return Region.NORTH_AMERICA
    if (value == 0x02):
        return Region.EUROPE
    if (value == 0x03):
        return Region.SCANDINAVIA
    if (value == 0x04):
        return Region.FINLAND
    if (value == 0x05):
        return Region.DENMARK
    if (value == 0x06):
        return Region.EUROPE_FRENCH_ONLY
    if (value == 0x07):
        return Region.DUTCH
    if (value == 0x08):
        return Region.SPANISH
    if (value == 0x09):
        return Region.GERMAN
    if (value == 0x0A):
        return Region.ITALIAN
    if (value == 0x0B):
        return Region.CHINESE
    if (value == 0x0C):
        return Region.INDONESIA
    if (value == 0x0D):
        return Region.SOUTH_KOREA
    if (value == 0x0E):
        return Region.COMMON
    if (value == 0x0F):
        return Region.CANADA
    if (value == 0x10):
        return Region.BRAZIL # to do: handle special case for Nintendo Gateway System
    if (value == 0x11):
        return Region.AUSTRALIA
    if (value == 0x12):
        return Region.OTHER_X
    if (value == 0x13):
        return Region.OTHER_Y
    if (value == 0x14):
        return Region.OTHER_Z
