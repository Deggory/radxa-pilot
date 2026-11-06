# Panda Docker Flash Workspace

This workspace was reduced to only what is needed to build and flash the `panda` firmware to STM32 through Docker.

## Required files at repository root

- `Dockerfile`
- `build_container.sh`
- `build_project.sh`
- `flash_docker.sh`
- `recover.sh`
- `firmware/` (shared firmware code + `panda` project)

## Flash panda with Docker

1. Build Docker image:
   ```bash
   ./build_container.sh
   ```
2. Build and flash panda firmware:
   ```bash
   ./flash_docker.sh panda
   ```

If no project is passed, scripts now default to `panda`.

## Notes

- Device flashing uses `dfu-util` in `recover.sh`.
- Build output is generated under `firmware/obj/`.
