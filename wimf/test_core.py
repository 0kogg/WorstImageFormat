from pathlib import Path

import numpy as np
from PIL import Image

import wimf
from wimf.extensions import parse_extensions


def test_lossless_roundtrip(tmp_path):
    """Verify bit-perfect lossless encoding and decoding."""
    arr = np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    out = str(tmp_path / "test_ll.wimf")
    wimf.save(out, img, lossless=True)

    loaded = wimf.open(out)
    assert np.array_equal(arr, loaded.to_numpy())


def test_lossy_dimensions(tmp_path):
    """Verify lossy encoding preserves image structure."""
    arr = np.random.randint(0, 256, (128, 128, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    out = str(tmp_path / "test_lossy.wimf")
    wimf.save(out, img, quality=5)

    loaded = wimf.open(out)
    assert loaded.size == (128, 128)


def test_metadata_persistence(tmp_path):
    """Verify metadata is saved and loaded correctly."""
    arr = np.random.randint(0, 256, (16, 16, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    out = str(tmp_path / "test_meta.wimf")
    wimf.save(out, img, quality=5, author="CI_Tester", custom="Data")

    info = wimf.info(out)
    assert info["author"] == "CI_Tester"
    assert info["custom"] == "Data"


def test_parity_protection(tmp_path):
    """Verify anti_rot encoding creates a protected WIM2 file."""
    arr = np.random.randint(0, 256, (16, 16, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    out = str(tmp_path / "test_parity.wimf")
    wimf.save(out, img, lossless=True, anti_rot=True, format_version=2)

    with open(out, "rb") as f:
        magic = f.read(4)
    assert magic in (b"WIM2", b"WIM3")
    assert b"AROT" in parse_extensions(Path(out).read_bytes())


def test_cpp_extension_loaded():
    """Ensure the C++ backend is the active processing engine."""
    from wimf import core

    assert core.HAS_CPP is True, "C++ extension failed to load in CI environment."


def test_tiled_mode_10(tmp_path):
    """Verify large images trigger and survive Mode 10 tiling."""
    arr = np.random.randint(0, 256, (600, 600, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    out = str(tmp_path / "test_tiled.wimf")
    wimf.save(out, img, quality=3)

    loaded = wimf.open(out)
    assert loaded.size == (600, 600)


def test_native_short_buffer_kernels_stay_in_bounds():
    """Regression: sizes below one SIMD vector must not underflow loop bounds.

    block_xor_raw and calculate_checksum_raw compared ``i <= size - 32``,
    which wraps to a huge value for size < 32 and let the AVX2 loop run one
    32-byte access past the end of the buffer. That crashed the Ubuntu 26.04
    CI job on a 24-byte parity chunk.
    """
    from wimf import wimf_cpp

    rng = np.random.default_rng(1234)
    for size in range(1, 65):
        target = rng.integers(0, 256, size, dtype=np.uint8)
        source = rng.integers(0, 256, size, dtype=np.uint8)
        expected = target ^ source
        wimf_cpp.block_xor(target, source)
        assert np.array_equal(target, expected), f"block_xor mismatch at size {size}"
        checksum = wimf_cpp.calculate_checksum(expected)
        assert checksum == int(expected.astype(np.uint64).sum() % 4294967295), f"checksum mismatch at size {size}"


def test_parity_protection_short_payloads():
    """Parity blocks smaller than a SIMD vector round-trip and repair safely."""
    from wimf.parity import protect, verify_and_repair

    for size in range(1, 65):
        payload = bytes((i * 37 + size) & 0xFF for i in range(size))
        protected = protect(payload, num_chunks=4)
        clean, protected_flag, repaired = verify_and_repair(protected)
        assert clean == payload
        assert protected_flag is True
        assert repaired is False

        header = 4 + 4 + 4 + 4 * 4
        corrupted = bytearray(protected)
        corrupted[header] ^= 0xFF
        recovered, protected_flag, repaired = verify_and_repair(bytes(corrupted))
        assert recovered == payload, f"failed to repair size {size}"
        assert protected_flag is True
        assert repaired is True
