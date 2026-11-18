
from pathlib import Path
import sys

HEADER_SIZE = 0x40

CANDIDATES = {
    "LoROM": 0x7FC0,
    "HiROM": 0xFFC0,
    "ExHiROM": 0x40FFC0,
}

MAP_MODES = {
    0x20: "LoROM",
    0x21: "HiROM",
    0x22: "LoROM + FastROM",
    0x25: "ExHiROM",
    0x30: "LoROM + FastROM",
    0x31: "HiROM + FastROM",
}

def u16(data, offset):
    return int.from_bytes(data[offset:offset+2], "little")

def inspect_header(rom, offset, name):
    header = rom[offset:offset + HEADER_SIZE]

    if len(header) != HEADER_SIZE:
        return

    raw_title = header[0x00:0x15]

    print("Title bytes:", raw_title.hex(" "))

    title = raw_title.decode(
        "shift_jis", errors="replace"
    ).rstrip("\x00 ")

    print(f"Title: {title}")

    map_mode = header[0x15]
    cartridge = header[0x16]
    rom_size = header[0x17]
    ram_size = header[0x18]
    region = header[0x19]
    version = header[0x1B]

    complement = u16(header, 0x1C)
    checksum = u16(header, 0x1E)
    reset_vector = u16(header, 0x3C)

    print(f"\n--- {name} ---")
    print(f"Header offset: 0x{offset:X}")
    print(f"Title: {title}")
    print(f"Map mode: 0x{map_mode:02X}")
    print(f"Mapping: {MAP_MODES.get(map_mode, 'Unknown')}")
    print(f"Cartridge type: 0x{cartridge:02X}")
    print(f"ROM size code: 0x{rom_size:02X}")
    print(f"RAM size code: 0x{ram_size:02X}")
    print(f"Region: {region}")
    print(f"Version: {version}")
    print(f"Complement: 0x{complement:04X}")
    print(f"Checksum: 0x{checksum:04X}")
    print(f"Reset vector: 0x{reset_vector:04X}")

    print(
        "Checksum pair valid:",
        (complement ^ checksum) == 0xFFFF
    )

def main():
    if len(sys.argv) != 2:
        print("Usage: python snes_header.py <game>.sfc")
        return

    path = Path(sys.argv[1])
    rom = path.read_bytes()

    print(f"File: {path}")
    print(f"Size: {len(rom)} bytes")
    print(f"Size: {len(rom) / 1024 / 1024:.3f} MiB")

    copier_header = len(rom) % 0x8000 == 512

    print("Possible copier header:", copier_header)

    base = 512 if copier_header else 0

    # for name, offset in CANDIDATES.items():
    inspect_header(rom, base + 0x7FC0, "LoRom")

if __name__ == "__main__":
    main()
