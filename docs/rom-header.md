Extacted from: https://snes.nesdev.org/wiki/ROM_header
# Rom header overview
Nintendo required SNES developers to include a header in the game's data that describes what hardware the game cartridge contains. This is not needed by the SNES hardware, though the game software can access it as ROM data. The header is located at the CPU address range $00FFC0-$00FFDF, right before the interrupt vectors, with an optional second header at $00FFB0-$00FFBF. This means that the location of the header within the actual ROM file will change based on the cartridge's memory map mode - with LoROM games placing it at $007Fxx, HiROM games placing it at $00FFxx, and ExHiROM games placing it at $40FFxx. Therefore, if it's correctly filled out, an emulator will have a higher chance of being able to figure out where the header is

# ROM header table of contents
## Table for Hi-Rom
| First address | Length |                                                Contents                                                |
|:-------------:|:------:|:------------------------------------------------------------------------------------------------------:|
| $FFC0         | 21     | Cartridge title (21 bytes ASCII range $20-7E, or possibly JIS X 0201. Unused bytes should be spaces.)  |
| $FFD5         | 1      | ROM speed and memory map mode (LoROM/HiROM/ExHiROM)                                                    |
| $FFD6         | 1      | Chipset (Indicates if a cartridge contains extra RAM, a battery, and/or a coprocessor)                 |
| $FFD7         | 1      | ROM size: 1<<N kilobytes, rounded up (so 8=256KB, 12=4096KB and so on)                                 |
| $FFD8         | 1      | RAM size: 1<<N kilobytes (so 1=2KB, 5=32KB, and so on)                                                 |
| $FFD9         | 1      | Country code (implies NTSC/PAL)                                                                        |
| $FFDA         | 1      | Developer ID                                                                                           |
| $FFDB         | 1      | ROM version (0 = first)                                                                                |
| $FFDC         | 2      | Checksum complement (Checksum ^ $FFFF)                                                                 |
| $FFDE         | 2      | Checksum                                                                                               |
| $FFE0         | 32     | Interrupt vectors                                                                                      |

## Table for Lo-Rom
| First address | Length |                                                Contents                                                |   |   |
|:-------------:|:------:|:------------------------------------------------------------------------------------------------------:|---|---|
| $7FC0         | 21     | Cartridge title (21 bytes ASCII range $20-7E, or possibly JIS X 0201. Unused bytes should be spaces.)  |   |   |
| $7FD5         | 1      | ROM speed and memory map mode (LoROM/HiROM/ExHiROM)                                                    |   |   |
| $7FD6         | 1      | Chipset (Indicates if a cartridge contains extra RAM, a battery, and/or a coprocessor)                 |   |   |
| $7FD7         | 1      | ROM size: 1<<N kilobytes, rounded up (so 8=256KB, 12=4096KB and so on)                                 |   |   |
| $7FD8         | 1      | RAM size: 1<<N kilobytes (so 1=2KB, 5=32KB, and so on)                                                 |   |   |
| $7FD9         | 1      | Country code (implies NTSC/PAL)                                                                        |   |   |
| $7FDA         | 1      | Developer ID                                                                                           |   |   |
| $7FDB         | 1      | ROM version (0 = first)                                                                                |   |   |
| $7FDC         | 2      | Checksum complement (Checksum ^ $FFFF)                                                                 |   |   |
| $7FDE         | 2      | Checksum                                                                                               |   |   |
| $7FE0         | 32     | Interrupt vectors                                                                                      |   |   |


Take for instance the rom of yakuchuu, a Lo-ROM cartige:

$7FC0 | d4 ba b3 c1 ad b3 20 20 20 20 20 20 20 20 20 20
         +--+--+--+--+--+
         |  |  |  |  |  |
         ﾔ  ｺ  ｳ  ﾁ  ｭ  ｳ  

