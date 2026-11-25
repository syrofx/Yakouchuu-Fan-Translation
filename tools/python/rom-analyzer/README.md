Python project in charge of analyzing the ROM provided, its job is to identify things like
- Header
- Mapping used
- Title
- Developer ID
- Size
- Checksum

Additionally the idea is to validate the checksums (xor with complement) and to provided offsets so the C++ project can extract the strings