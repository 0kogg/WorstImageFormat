# WIMF documentation

Start with the [project README](../README.md) for installation and a quick
tour. These pages go into detail on the container formats, the native core,
and the verification process.

## Format specifications

| Document | Contents |
|---|---|
| [WIM3 format specification](wim3-format.md) | Current default container (codename *oxygen*): quadtree tiles, Raw / Predictive-RC / embedded-wavelet modes, progressive truncation, lossy bitplane quantization. |
| [WIM2 format specification](wim2-format.md) | Stable hybrid container still used for existing files, anti-rot protection, and chrono history. |
| [Legacy migration](legacy-migration.md) | Reading and converting WIMF v1, `.wif`, `ROT!`, and AWIF files. |
| [Conformance vectors](conformance.md) | WIM2 conformance corpus and how to add cases. |
| [AWIF compatibility](awif-testing.md) | Legacy animation coverage and the test matrix. |

## Implementation

| Document | Contents |
|---|---|
| [Native C++ core](native-core.md) | C++17 backend, SIMD paths, and embedding WIMF in other programs. |
| [C ABI contract](c-api.md) | Version 1 C ABI surface and stability guarantees. |
| [SDK packaging](sdk-packaging.md) | Standalone archives, licensing, and development headers. |
| [Integrations](integrations.md) | Pillow plugin, ImageMagick/FFmpeg bridges, and desktop use. |
| [SIMD benchmarks](simd-benchmarks.md) | Kernel benchmarks and how to report hardware results. |

## Project process

| Document | Contents |
|---|---|
| [Known flaws](known-flaws.md) | Deliberate limitations and the audit that tracks them. |
| [Roadmap](roadmap.md) | What is planned, in progress, and explicitly out of scope. |
| [Release checklist](release-checklist.md) | Steps required to cut a release. |

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the development setup, required
local checks, and the rules for changing a bitstream. Security-sensitive
reports should follow [SECURITY.md](../SECURITY.md) instead of a public issue.

All documentation is licensed under the same terms as the project:
GPL-3.0-or-later.
