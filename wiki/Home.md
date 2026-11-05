<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://gitlab.com/ivanm12453/WorstImageFormat/-/raw/main/.github/assets/white.png">
    <source media="(prefers-color-scheme: light)" srcset="https://gitlab.com/ivanm12453/WorstImageFormat/-/raw/main/.github/assets/dark.png">
    <img alt="Worst Image Format" src="https://gitlab.com/ivanm12453/WorstImageFormat/-/raw/main/.github/assets/dark.png" width="500">
  </picture>
</p>

WIMF is an experimental image codec with a Python frontend and a portable C++17 backend. New files use the **WIM3** container and the canonical `.wimf` extension. WIM2 and legacy files remain fully decodable.

WIM3 stores a quadtree of independently checksummed tiles and codes each leaf as Raw, Predictive-RC, or embedded wavelet, with truncation-based progressive decoding and optional lossy bitplane quantization. WIM2 remains available with its Raw, Predictive, Palette, and Wavelet tile modes, plus anti-rot recovery and indexed history states.

## Start here

- [[Installation]] — install wheels and verify native acceleration.
- [[Python-API]] — encode, decode, inspect, ROI, metadata, and history.
- [[Command-line tools]] — headless workflows and diagnostics.
- [[WIMF-Studio]] — desktop encoder, inspector, and corruption lab.
- [[WIM3-Format]] — current default container and coding modes.
- [[WIM2-Format]] — stable hybrid container and tile-mode overview.
- [[Conformance-Vectors]] — portable decoder expectations and hashes.
- [[Native-Integration]] — embed the codec without Python.
- [[Corruption-and-Recovery]] — strict decoding, diagnostic previews, and anti-rot.
- [[Legacy-Migration]] — move WIMF v1, `.wif`, AWIF, and `ROT!` content forward.
- [[Roadmap]] — interoperability and adoption work.

## Project status

WIM3 is the default authoring container and is still a draft: its bitstream may change between minor releases. WIM2 is the stable container and is required for anti-rot protection and chrono history. Deprecated legacy writers warn on use while read-only compatibility is retained indefinitely.

The authoritative specifications live in the repository: [`docs/wim3-format.md`](https://gitlab.com/ivanm12453/WorstImageFormat/-/blob/main/docs/wim3-format.md) and [`docs/wim2-format.md`](https://gitlab.com/ivanm12453/WorstImageFormat/-/blob/main/docs/wim2-format.md).

WIMF is experimental. Please report reproducible bugs at <https://gitlab.com/ivanm12453/WorstImageFormat/-/issues> with your OS, Python version, `wimf runtime --json` output, and a minimal sample when possible. Security-sensitive reports should follow [`SECURITY.md`](https://gitlab.com/ivanm12453/WorstImageFormat/-/blob/main/SECURITY.md).

> WIMF compresses data; it does not encrypt it. Never store secrets in metadata.
