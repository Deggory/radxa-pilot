# Documentation for the Radxa port

This checkout targets **Ubuntu ARM64 on Radxa Dragon Q8B**. Start with the
project-specific guides below. The other pages in this folder are inherited
openpilot/Sunnypilot references; their comma-device setup instructions and
supported-car claims do not establish support for this Radxa/Chimera port.

| What you need | Read |
| --- | --- |
| Install dependencies and build | [install.md](../install.md) |
| Radxa implementation status | [RADXA_PORT.md](../RADXA_PORT.md) |
| Changes made in this checkout | [readme_wat_we_did.md](../readme_wat_we_did.md) |
| Resume the current work | [AI handoff](../Ai/HANDOFF.md) |
| BeamNG optical camera + CAN loop | [BeamNG guide](../openpilot/tools/sim/beamng/README.md) |

## Which inherited documents matter here?

- **Useful porting references:** [car interfaces](how-to/car-port.md),
  [logs](concepts/logs.md), [replay](how-to/replay-a-drive.md),
  [safety](SAFETY.md), [limitations](LIMITATIONS.md) and
  [integration concepts](INTEGRATION.md). Device-specific sections still need
  adaptation; they are not evidence of a tested Radxa implementation.
- **Development policy:** [AI policy](AI_POLICY.md) and
  [contributing](CONTRIBUTING.md). These are documentation, not runtime settings.
- **Upstream reference:** [CARS.md](CARS.md) is a generated vehicle catalogue.
  It neither loads car support nor qualifies our custom actuator or Chimera.
- **Comma-device instructions:** [connect-to-comma](how-to/connect-to-comma.md)
  describes comma hardware, not Q8B login, wiring or installation. Use our
  project-specific installation guide instead.

## Does Radxa need this folder to run?

The driving pipeline does not use this folder as its hardware implementation.
The documentation website is optional for an on-board deployment. During
development, preserve the reference pages and existing tooling links: the
`op docs` command uses `serve.py`, the website uses `template.html` and assets,
and the car-documentation generator/maintenance job writes `CARS.md`.

Removing these files from the development checkout also requires adapting
their consumers and links. No documentation files or comma hardware code were
deleted in this review. A separate dependency-checked deployment package can
omit development documentation without removing it from the source repository.

## Optional upstream documentation website

The `docs/` tree is the source for [docs.comma.ai](https://docs.comma.ai).
The site is updated on pushes to master by this [workflow](../.github/workflows/docs.yaml).

**1. Build the site**
``` bash
op docs --build
```

**2. Run the site locally** (rebuilds on change)
``` bash
op docs
```
