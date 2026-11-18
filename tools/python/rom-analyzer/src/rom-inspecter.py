from pathlib import Path

rom_path = "../../../roms/yakouchuu.smc"

rom = Path(rom_path).read_bytes()

print(f"Size: {len(rom)} bytes")
print(f"Size: {len(rom) / 1024:.2f} KiB")
print(f"Size: {len(rom) / 1024 / 1024:.2f} MiB")

print(f"First 64 bytes:", rom[:64].hex(" "))
print(f"Last 64 bytes:", rom[-64:].hex(" "))

size = len(rom)

if size % 0x8000 == 512:
    print("Possible 512-byte copier header")
elif size % 0x8000 == 0:
    print("No apparent copier header")
else:
    print("Unusial ROM file")
