# syro - 16/11/2026
# see: https://snes.nesdev.org/wiki/ROM_header
from pathlib import Path
import sys

ROM_FILE_PATH = "../../../../data/original/yakouchuu.smc"
HEADER_SIZE = 0x40

LO_ROM_HEADER_BASE_ADDRESS = 0x7F00
HI_ROM_HEADER_BASE_ADDRESS = 0xFF00

# por ejemplo si es lorom, el cartridge title estara en 0x7FC0 y si es un hiron esta en 0xFFC0
MAP_MODES = {
    0x20: "LoROM",
    0x21: "HiROM",
    0x22: "LoROM + FastROM",
    0x25: "ExHiROM",
    0x30: "LoROM + FastROM",
    0x31: "HiROM + FastROM",
}

HEADER_OFFSETS = {
    "CartridgeTitle": 0xC0,
    "MemoryMap": 0xD5,
    "Chipset": 0xD6,
    "ROMSize": 0xD7,
    "RAMSize": 0xD8,
    "CountryCode": 0xD9,
    "DeveloperId": 0xDA,
    "ROMVersion": 0xDB,
    "ChecksumComplement": 0xDC,
    "Checksum": 0xDE,
    "InterruptVectors": 0xE0
}



# helper to merge 2 u8 into 1 u16
def u16(data, offset):
    return int.from_bytes(data[offset:offset+2], "little")

# first 21 bytes using jis x 0201 
def get_cartrige_tile(header):
    raw_title = header[0x00:0x15]

    title = raw_title.decode(
        "shift_jis", errors="replace"
    ).rstrip("\x00 ")

    return title

# xor the checksum and the complement
def checksum_matched(header):
    checksum_value = u16(header, 0x1E)
    checksum_complement_value = u16(header, 0x1C)

    return (checksum_value ^ checksum_complement_value) == 0xFFFF

def determine_memory_map(rom):
    return

def has_copier_header(rom):
    copier_header = len(rom) % 0x8000 == 512
    # print("Possible copier header:", copier_header)
    return copier_header

def read_header(rom, offset):
    header = rom[offset:offset + HEADER_SIZE]

    if len(header) != HEADER_SIZE:
        return

    return header


def get_full_address(rom, base, offset):
    return base | offset


def main():
    rom = Path(ROM_FILE_PATH).read_bytes()
    copier_header = has_copier_header(rom)
    base = 512 if copier_header else 0

    # header = read_header(rom, base + LO_ROM_HEADER_OFFSET) # find a way to determine if lo_rom or hi_rom
    # title = get_cartrige_tile(header)
    # checksum_match = checksum_matched(header)

    # print(f"Cartridge title: {title}")
    # print (f"Checksum matched: {checksum_match}")

    lo_rom_cartridge_title = get_full_address(LO_ROM_HEADER_BASE_ADDRESS, HEADER_OFFSETS["CartridgeTitle"])
    print(f"Title address {hex(lo_rom_cartridge_title)}")



if __name__ == "__main__":
    main()
