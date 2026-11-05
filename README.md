# WIMF - Worst IMage Format

[![PyPI](https://img.shields.io/pypi/v/wimf.svg)](https://pypi.org/project/wimf/)
[![Python](https://img.shields.io/pypi/pyversions/wimf.svg)](https://pypi.org/project/wimf/)
[![CI](https://github.com/ivanmj124/WorstImageFormat/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ivanmj124/WorstImageFormat/actions/workflows/ci.yml)
[![License](https://img.shields.io/pypi/l/wimf.svg)](https://gitlab.com/ivanm12453/WorstImageFormat/-/blob/main/LICENSE)

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://gitlab.com/ivanm12453/WorstImageFormat/-/raw/main/.github/assets/white.png">
    <source media="(prefers-color-scheme: light)" srcset="https://gitlab.com/ivanm12453/WorstImageFormat/-/raw/main/.github/assets/dark.png">
    <img alt="Worst Image Format" src="https://gitlab.com/ivanm12453/WorstImageFormat/-/raw/main/.github/assets/dark.png" width="500">
  </picture>
</p>

WIMF is an experimental, versioned image codec with a Python frontend and a
portable C++17 backend. New images use the **WIM3** container (codename
*oxygen*): a quadtree of independently checksummed tiles, each coded as Raw,
Predictive-RC, or embedded wavelet, with truncation-based progressive decoding
and optional lossy bitplane quantization. The stable **WIM2** container remains
fully decodable and is still selectable for existing workflows that rely on
anti-rot protection or chrono history.

## Highlights

- WIM3 by default, with quadtree tiles, embedded wavelet coding, and progressive truncation.
- Exact lossless coding and quality-controlled lossy quantization (`quality=1`–`10`).
- WIM2 per-tile hybrid selection over Raw, Predictive, Palette, and CDF Wavelet modes.
- `Fast`, `Balanced`, and `Extreme` search presets for WIM2 encoding.
- Independently decodable tiles for bounded ROI reads and checksum-isolated corruption.
- RGB, RGBA, grayscale, LA, depth channels, and 8/10/12/16-bit pipelines (WIM3).
- Zstandard-compressed structured symbols and per-tile CRC32 checksums (WIM2).
- Optional WIM2 anti-rot data capable of repairing up to two damaged shards.
- Indexed WIM2 chrono states with random state decoding.
- EXIF round-tripping for Pillow sources, including re-attachment on save.
- Portable C++17 kernels with NEON and AVX2 SIMD acceleration and a Python reference fallback.
- Pillow plugin, unified `wimf` CLI, and the headless-capable WIMF Studio.

## Known limitations

WIM3 is a draft format and its bitstream may still change between minor
releases; WIM2 and legacy files remain permanent decode surfaces. WIM3 does not
yet support anti-rot protection, chrono history, or animation, which stay
WIM2/legacy features. Chroma-from-luma, perceptual (CSF-weighted) quantization,
and the optional learned transform are future work.

WIM2 compression ratios are actively improving. WIMF 2.2 introduced
content-adaptive wavelet quantization, improved Zstandard compression levels,
and quadratic rate-distortion scoring. Further tuning is expected without
breaking decode compatibility.

Benchmarks and comparative metrics against PNG, WebP, AVIF, JPEG, and JPEG XL
are hardware-dependent and will be published separately once the codec reaches
a stable performance baseline.

## Installation

Install the published package with Python 3.10 or newer:

```bash
python -m pip install wimf
```

Precompiled wheels are published for Linux x86-64, Windows x86-64, macOS Intel, and macOS Apple Silicon across CPython 3.10–3.14. A matching wheel does not require a local compiler.

For development:

```bash
git clone https://gitlab.com/ivanm12453/WorstImageFormat.git
cd WorstImageFormat
python -m pip install -e .
```

Source installations require a C++17 compiler and pybind11; the Python fallback remains usable when the native extension is unavailable.

## Choose a configuration

| Goal | Recommended settings | Notes |
|---|---|---|
| General photographs | `quality=7, preset="Balanced", codec="auto"` | Default; lets every tile choose its best family. |
| Maximum compression search | `preset="Extreme", codec="auto"` | Evaluates every eligible tile mode and encodes more slowly. |
| Fast preview or batch work | `preset="Fast", codec="auto"` | Evaluates one classified mode plus Raw fallback. |
| Exact archival pixels | `lossless=True, codec="auto"` | Chooses the smallest exact candidate per tile. |
| Force photographic coding | `codec="wavelet"` | CDF 9/7 lossy or reversible CDF 5/3 lossless. |
| Flat graphics and icons | `codec="palette"` | Uses a local palette where eligible and Raw fallback otherwise. |
| Text and sharp edges | `codec="predictive"` | Reversible spatial prediction in lossless mode. |
| Diagnostic baseline | `codec="raw"` | Minimal codec logic; usually the largest output. |

Quality ranges from 1 through 10. Every quality is continuously tested under `Fast`, `Balanced`, and `Extreme`; the preset changes search effort, while quality controls lossy quantization.

`preset` and `codec` select WIM2 tile-mode search. Under the default WIM3 container the encoder validates both for API consistency but chooses Raw, Predictive-RC, or embedded-wavelet coding from its own quadtree analysis.

## Python API

```python
from PIL import Image
import wimf

image = Image.open("photo.png")

# WIM3 with quadtree selection is the default.
output = wimf.save("photo.wimf", image, quality=7)

# Exact reconstruction.
wimf.save("exact.wimf", image, lossless=True)

# Opt into the stable WIM2 container, or the legacy WIMF v1 format.
wimf.save("stable.wimf", image, lossless=True, format_version=2)
wimf.save("legacy.wimf", image, lossless=True, format_version=1)

decoded = wimf.open("photo.wimf")
decoded.pil.save("decoded.png")

# Memory-only applications can use bytes directly.
payload = wimf.encode(image, lossless=True, metadata={"author": "Arrow"})
decoded = wimf.decode(payload)
details = wimf.inspect(payload)
```

`codec` accepts `auto`, `wavelet`, `predictive`, `palette`, or `raw`. `preset` accepts `Fast`, `Balanced`, or `Extreme`.

### Complete save options

| Option | Values | Default | Meaning |
|---|---|---|---|
| `quality` | `1`–`10` | `7` | Lossy quality and rate-distortion target. |
| `lossless` | Boolean | `False` | Require exact pixel reconstruction. |
| `preset` | `Fast`, `Balanced`, `Extreme` | `Balanced` | Number of candidate modes evaluated per tile. |
| `codec` | `auto`, `wavelet`, `predictive`, `palette`, `raw` | `auto` | Automatic hybrid selection or forced family. |
| `format_version` | `1`, `2`, `3` | `3` | WIM3 default, stable WIM2, or explicit legacy WIMF v1 output. |
| `threads` | positive integer or `None` | `None` | Conservative automatic count or explicit tile workers. |
| `anti_rot` | Boolean | `False` | Append WIM2 protection capable of bounded recovery (`format_version=2`). |
| `metadata` | dictionary | `{}` | Application metadata stored in the container. |

### ROI decoding

```python
decoder = wimf.WIMFDecoder("large.wimf")
region = decoder.decode(roi=(1024, 768, 640, 480))
```

Only intersecting tile payloads are decompressed (WIM2 tiles; WIM3 quadtree leaves decode progressively).

### Anti-rot and chrono history

```python
encoder = wimf.WIMFEncoder(image).set_anti_rot()
encoder.add_chrono_state(edited_image)
payload = encoder.encode(lossless=True)

decoder = wimf.WIMFDecoder(payload)
original = decoder.decode_chrono_state(0)
edited = decoder.decode_chrono_state(1)
print(decoder.was_protected, decoder.was_repaired)
```

WIM2 extensions are appended after the base tile payload. Existing WIM2 files remain valid and older readers can still decode the primary image. Anti-rot and chrono history require `format_version=2`; WIM3 raises a clear error for both.

### Metadata without recompression

```python
updated = wimf.rewrite_metadata(payload, {"author": "Arrow", "license": "CC0"})
```

WIM2 tile payloads remain byte-for-byte identical. Tile offsets and checksums are recalculated, history is retained, and anti-rot protection is regenerated when present.

### Text transports

```python
text = wimf.to_base64(payload, wrap=76)
assert wimf.from_base64(text) == payload

assert wimf.from_base16(wimf.to_base16(payload)) == payload
assert wimf.from_base32(wimf.to_base32(payload)) == payload

url = wimf.to_data_url(payload)
assert wimf.from_data_url(url) == payload
```

These helpers use strict RFC 4648 parsing, bounded input sizes, and whitespace-tolerant decoding. Data URLs use Base64 and the `image/x-wimf` MIME type. Base16, Base32, and Base64 are transport encodings-not compression-and expand data by roughly 100%, 60%, and 33%, respectively.

### Runtime diagnostics

```python
print(wimf.runtime_info())
```

The result reports whether native kernels are active, architecture, SIMD path, hardware and effective thread counts, codec version, and Zstandard version.

### Mandelbrot example

The included generator renders a Mandelbrot set with NumPy and writes WIMF directly:

```bash
python examples/mandelbrot_wimf.py mandelbrot.wimf --width 1920 --height 1080 --quality 7
```

Use `--lossless`, force a tile mode with `--codec`, or zoom using `--center-x`, `--center-y`, and `--span`.

## Command-line tools

The unified command covers the normal workflow:

```bash
wimf encode photo.png photo.wimf --quality 7
wimf encode artwork.png artwork.wimf --lossless
wimf decode photo.wimf photo.png
wimf decode huge.wimf crop.png --roi 100 200 640 480
wimf info photo.wimf
wimf runtime
wimf view photo.wimf
wimf base16 encode photo.wimf photo.hex
wimf base32 encode photo.wimf photo.b32
wimf base64 encode photo.wimf photo.txt --data-url
wimf corrupt photo.wimf damaged.wimf --seed 42 --area payload
wimf diagnose damaged.wimf --unsafe-preview damaged-preview.png
```

Run `wimf <command> --help` for focused options. Metadata uses repeatable `--metadata KEY=VALUE` arguments. The original specialized commands remain available:

- `wimf-convert` and `wimf-meta` are deprecated compatibility tools in 2.2. Use the unified `wimf` CLI or WIMF Studio.
- AWIF authoring is deprecated. Existing animations remain readable, including historical timing metadata.
- `wimf-studio` opens the encoder, comparison viewer, tile inspector, protection/history tools, and codec lab.
- `wimf-view` is a compatibility alias that opens WIMF Studio.
- `wimf-cat` renders supported images in compatible terminals.
- `wimf-meta` inspects and edits legacy metadata.

Native C/C++ builds also provide `wimf-native`, a dependency-free process bridge for lossless PGM/PPM ↔ WIMF conversion.

## Project layout

| Path | Contents |
|---|---|
| `wimf/` | Python package: public API, WIM2 codec, WIM3 bindings, CLI, Studio, Pillow plugin |
| `src/` | Portable C++17 core, WIM3 codec, SIMD kernels, C ABI, and pybind11 bindings |
| `tools/` | Native PGM/PPM bridge, SIMD benchmark, and rate-distortion sweep |
| `tests/` | C++ tests, conformance vectors, standalone C/C++ build and consumer checks |
| `benchmarks/`, `examples/` | Benchmark drivers and runnable examples |
| `integrations/` | FFmpeg, ImageMagick, Linux, and Windows integration assets |
| `docs/` | Format specifications and project documentation ([index](docs/README.md)) |

## Tested feature matrix

| Feature | Status | Continuous verification |
|---|---|---|
| WIM3 default container | Implemented (draft) | Quadtree encode/decode, mixed tile modes, golden vectors, truncation |
| WIM3 Raw, Predictive-RC, and embedded wavelet | Implemented (draft) | Forced-mode and automatic selection, 8/10/12/16-bit parity |
| WIM3 progressive decode | Implemented | `target_planes` capped decode equals truncated-file decode |
| WIM2 Raw, Predictive, Palette, and Wavelet | Implemented | Forced modes, automatic mixed modes, exact/lossy reconstruction |
| Qualities and presets | Implemented | All qualities 1–10 × Fast/Balanced/Extreme |
| RGB, RGBA, grayscale, LA, depth channel | Implemented | Odd dimensions, edge tiles, alpha, five-channel depth access |
| 8-, 10-, and 16-bit pixels | Implemented | Exact high-bit-depth lossless round trips and native/reference parity |
| ROI and independent tiles | Implemented | Cross-tile crops and checksum-isolated corruption |
| Threading and cancellation | Implemented | Deterministic 1/2/4-thread output, progress contract, bounded cancellation |
| Metadata rewrite | Implemented | Tile payload identity, history retention, anti-rot regeneration |
| Anti-rot | Experimental | Two-shard repair, three-shard rejection, damaged parity, protected history |
| Chrono history | Experimental | Unchanged/changed states, ordering, random state access, protected history |
| Base16, Base32, Base64, and data URLs | Implemented | Strict alphabets, MIME validation, whitespace and safety bounds |
| EXIF round-trip | Implemented | Pillow EXIF tags preserved through encode/decode and re-attached on save |
| Corruption laboratory | Experimental | Header, metadata, index, payload, extension, and parity targeting |
| AWIF animation | Legacy decode compatibility | Committed fixtures and malformed-input safety |
| WIMF v1, `.wif`, and `ROT!` | Deprecated authoring; legacy decoding | Warning coverage, migration, and protected decode |
| WIMF Studio and headless CLI | Implemented | Headless state tests, command help, installed-wheel smoke tests |

The visual report separately exercises synthetic mixed content, a credited nature photograph, and a credited animal photograph. It publishes decoded outputs, amplified differences, exact configurations, tile-mode counts, timings, WIMF payloads, and JSON metrics as CI artifacts.

## Compatibility and status

| Capability | WIM3 (default) | WIM2 | Legacy decode |
|---|---|---|---|
| Hybrid still images | Raw / Predictive-RC / wavelet quadtree | Raw / Predictive / Palette / CDF wavelet tiles | WIMF v1 supported |
| Lossless and lossy coding | Implemented (bitplane quantization) | Implemented | Supported |
| ROI and independent tiles | Quadtree leaves | 128×128 tiles | Format-dependent |
| Progressive decode | Truncation-based (`target_planes`) | `layers` reserved, not embedded | No |
| 8/10/12/16-bit pixels | 8, 10, 12, 16 | 8, 10, 16 | 8-bit |
| Anti-rot | Not supported | Two-shard extension | `ROT!` supported |
| Chrono history | Not supported | Indexed extension | AWIF states supported |
| Animation creation | Not supported | Legacy-only | AWIF encode/decode with preserved timing |
| Wavelet watermark creation | Not supported | Planned | v1 only |

See the [WIM3 specification](docs/wim3-format.md), [WIM2 format overview](docs/wim2-format.md), [legacy migration guide](docs/legacy-migration.md), [native embedding guide](docs/native-core.md), [desktop/application integrations](docs/integrations.md), [adoption roadmap](docs/roadmap.md), and [release checklist](docs/release-checklist.md). The full index is in [docs/README.md](docs/README.md).

## Verification and roadmap

CI separates Python quality, cross-platform API/feature tests, legacy decode compatibility, WIM3 conformance, standalone C++, sanitizers, packaging, visual evidence, and non-blocking performance measurements. Python-versus-C++ benchmarks cover WIM2 still images on Windows, Linux, and macOS. The active roadmap is:

- Measure AVX2 and NEON SIMD acceleration across reference hardware (CRC-32 and predictive filter paths are implemented; wavelet lifting is scalar). Run `tools/wimf_simd_bench.cpp` locally or read CI job summaries - see `docs/simd-benchmarks.md`.
- Verify Linux ARM64 and Windows ARM64 wheels on dedicated native runners.
- Validate the memory-only synchronous core with Emscripten on the future web branch without changing the WIM3 bitstream.
- Publish signed standalone C/C++ development archives for the versioned ABI and conformance pack.
- Build on the Pillow plugin and native PGM/PPM bridge with ImageMagick, FFmpeg, and desktop thumbnailer integrations.
- Preserve legacy animation and watermark decoding without reviving their deprecated authoring paths.

Target performance is at least 10 MP/s Balanced encoding and 50 MP/s decoding on reference hardware; benchmark results are hardware-dependent and are not claimed until measured.

## Documentation

The [documentation index](docs/README.md) links every specification and process
page. Start with the [WIM3 specification](docs/wim3-format.md) for the current
container, or the [WIM2 specification](docs/wim2-format.md) if you need the
legacy format or its extensions.

## Contributing

Bug reports, documentation fixes, and focused pull requests are welcome. Read
[CONTRIBUTING.md](CONTRIBUTING.md) for the development setup, the local checks
CI requires, and the rules for bitstream changes. Format changes must keep every
existing WIM2, WIM3, and legacy file decodable.

## Security

WIMF parses untrusted files. Please report decoder crashes, out-of-bounds
access, or unsafe CLI behaviour privately as described in
[SECURITY.md](SECURITY.md), not in a public issue.

## License

WIMF is licensed under GPL-3.0-or-later. See [LICENSE](LICENSE).

## Reporting bugs

WIMF is experimental. If something breaks, please [open an issue](https://gitlab.com/ivanm12453/WorstImageFormat/-/issues) with your operating system, Python version, `wimf runtime --json` output, and a minimal sample file when possible. WIMF Studio's **Help → Report a Bug** command copies the relevant runtime diagnostics and opens the issue page.
