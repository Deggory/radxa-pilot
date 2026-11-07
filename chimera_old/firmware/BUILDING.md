# Build Ocelot board firmware from source

The folders under `firmware/` contain **source code**, not firmware ready to
upload. `SConscript` chooses one board's `main.c`, compiles it with the ARM
toolchain, converts its ELF to a raw `.bin`, then adds a version and RSA
signature to produce `.bin.signed`. It also builds a separate `bootstub.bin`.
The firmware-folder [`build_local.sh`](build_local.sh) runs this build without
connecting to USB or flashing a board.

| Physical board | Build project | Main source | Signed output |
| --- | --- | --- | --- |
| Chimera | `chimera` | `chimera/main.c` | `obj/chimera.bin.signed` |
| Interceptor Core | `interceptor_core` | `RetroPilot_Cores/interceptor_core/main.c` | `obj/interceptor_core.bin.signed` |
| Actuator Core | `actuator_core` | `RetroPilot_Cores/actuator_core/main.c` | `obj/actuator_core.bin.signed` |
| Relay Core | `relay_core` | `RetroPilot_Cores/relay_core/main.c` | `obj/relay_core.bin.signed` |
| iBooster | `ibst` | `ibst/main.c` | `obj/ibst.bin.signed` |

From `~/comma` (the directory shown in your terminal prompt):

```bash
./build_local.sh chimera
./build_local.sh interceptor_core
```

The workspace launcher calls the builder in `ocelot/firmware/`. If you first
change into `~/comma/ocelot/firmware`, use these commands instead:

```bash
./build_local.sh chimera
./build_local.sh interceptor_core
./build_local.sh ALL
```

You can also run `./ocelot/firmware/build_local.sh chimera` directly from
`~/comma`.

`ALL` builds the 11 projects listed in `firmware/SConscript`. For one
project, the raw file is `firmware/obj/<project>/<project>.bin`; the signed
application is `firmware/obj/<project>.bin.signed`. `firmware/obj/bootstub.bin`
is the separate bootloader. `obj/` is ignored by Git and can be regenerated.

On this Radxa, SCons 4.5.2, ARM GCC 13.2.1, binutils 2.42, newlib headers and
Python `pycryptodome` are available under
`~/.local/ocelot-build-tools/`; the wrapper adds them to its own environment.
Other machines need `scons`, `arm-none-eabi-gcc`, `arm-none-eabi-objcopy`, ARM
C headers (newlib) and the Python package that provides `Crypto.PublicKey`.
The repository's Dockerfile and `build_container.sh` provide another build
environment where Docker is installed. `build_container.sh` creates the
image only. The legacy `flash_docker.sh` builds inside that image and then
calls host-side `recover.sh`, which writes **both** the signed application
and `bootstub.bin` to the board. With no project argument, its lack of a guard
can let it reach `recover.sh`; it does not safely list projects. Use `build_local.sh` or
`build_project.sh` when you only want to create files.

The default build uses the repository's **debug signing key** in
`firmware/certs/debug`. The bootstub verifies the signature before starting
an application; a release-only bootstub will reject a debug-signed file.
The private release key is not in this checkout. The saved 2026-09-21 nightly
Chimera image was independently checked against the included debug public
key, but that does not prove every board's bootstub accepts local builds.

For the desktop DFU app, choose **Choose .bin.signed** and select the signed
application for the physical board; do not select the raw `.bin` or
`bootstub.bin` as an application. A build does not update the saved nightly
ZIP automatically. This checkout is at source commit `94efc673`, while the
downloaded nightly ZIP identifies commit `de19321`, so a new local build is
not the same firmware as that ZIP. Compilation and signing do not prove the
board will boot or operate correctly; test a build on an isolated bench before
any further use.

The [downloaded-versus-local comparison](BUILD_COMPARISON.md) records sizes,
hashes, embedded version strings and signing-key checks for all files that
exist in both sets.

Two later config-flash watchdog repair **candidates** were built on
2026-10-04: one from this local `main` source under
[`inspection/chimera-config-write-fix-20261004/`](inspection/chimera-config-write-fix-20261004/README.md),
and one from public `origin/json_api` float-layout source under
[`inspection/chimera-jsonapi-configfix-20261004/`](inspection/chimera-jsonapi-configfix-20261004/README.md).
The `json_api` candidate was later flashed application-only to the isolated
Chimera and read back exactly, but did not boot after a full USB power cycle.
The saved `de193215` nightly was restored and verified. The `main` candidate
remains unflashed. A firmware version change alone does not lift the native
app's board-serial write quarantine. See the
[bench outcome](../Core%20Config/FLASH_WRITE_INCIDENT.md#isolated-bench-outcome-later-on-2026-10-04).

To inspect instructions inside a signed file, see
[INSPECTING_SIGNED_BIN.md](INSPECTING_SIGNED_BIN.md). It explains the limits
of recovering source code from a binary.
