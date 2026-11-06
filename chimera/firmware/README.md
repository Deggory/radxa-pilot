# Chimera firmware

This is the destination for the modern STM32F413 board target. No firmware source
or executable build target has been added in the folder-setup increment.

Start from the [existing implementation map](../docs/FIRMWARE_SOURCE_MAP.md).
T01 will document the flash/config boundaries and known reset GPIO behavior;
T02 will define identity and communication contracts. T03 then adds reviewed
F413 support, an appropriately licensed linker and an offline build/size check.

The legacy Ocelot build helper/toolchain already exist in the workspace. Their
availability is established evidence; modern-image reproducibility and physical
qualification are separate work. Do not introduce a flash step into a build.
