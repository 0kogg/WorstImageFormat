# WIM3 format

WIM3 (codename *oxygen*) is the default WIMF container. It replaces WIM2's
fixed 128×128 tile grid with a quadtree of independently checksummed leaves,
and each leaf is coded as Raw, Predictive-RC, or embedded wavelet. Embedded
wavelet payloads truncate at plane boundaries, which makes
progressive-by-quality decoding real rather than a reserved counter.

The authoritative specification, including the container header, tile
descriptor, split tree, coding modes, progressive truncation, lossy bitplane
quantization, and sample-depth rules, lives in the repository:

- [`docs/wim3-format.md`](https://gitlab.com/ivanm12453/WorstImageFormat/-/blob/main/docs/wim3-format.md)

Related pages:

- [[WIM2-Format]] — the stable container that still backs anti-rot and chrono history.
- [[Conformance-Vectors]] — decoder expectations and hashes.
- [[Native-Integration]] — the C++ core and C ABI.

## Status

Phases 1–3 are implemented: container, split tree, Raw / Predictive-RC /
embedded-wavelet modes, 8–16-bit sample depths, truncation-based progressive
decode, EXIF round-tripping, and quantized-bitplane lossy coding. Chroma-from-
luma, perceptual (CSF-weighted) quantization, and the optional learned
transform remain future work.

WIM3 does not support anti-rot protection, chrono history, or animation.
Encode those with `format_version=2` or the legacy paths.
