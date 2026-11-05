# Contributing to WIMF

Thanks for taking the time to improve WIMF. This project is experimental, so
small, focused changes with tests are much easier to review than large ones.

By contributing you agree that your work is licensed under the project's
license, **GPL-3.0-or-later** (see `LICENSE`).

## Before you start

- Open an issue before starting a large feature, a new tile mode, or a
  bitstream change. Format decisions need to keep every existing WIM2 and
  WIM3 file decodable.
- Small fixes (typos, docs, test coverage, CLI ergonomics) can go straight to
  a pull request.
- Never commit generated output, build trees, `wimf.egg-info/`, wheel
  artifacts, or large binary fixtures. Use a small committed fixture if a
  regression needs one.

## Development setup

Python 3.10 or newer and a C++17 compiler are required for the native path;
the pure-Python fallback still works without a compiler.

```bash
git clone https://gitlab.com/ivanm12453/WorstImageFormat.git
cd WorstImageFormat
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .
```

`pip install -e .` builds the pybind11 extension in place. If you prefer to
build it explicitly:

```bash
python setup.py build_ext --inplace
```

## Checks before opening a pull request

```bash
python -m pip install ruff mypy pytest pybind11 numpy pillow zstandard
python -m ruff check wimf tests benchmarks examples setup.py
python -m ruff format wimf tests benchmarks examples setup.py --check
python -m mypy wimf --ignore-missing-imports --no-strict-optional --python-version 3.12
python -m pytest wimf tests -q
```

The full test names used by CI are listed in `.github/workflows/ci.yml` and
`.gitlab-ci.yml`. Running the whole `wimf` test directory is usually enough
locally.

### Native core

```bash
cmake -S . -B cmake-build -DBUILD_SHARED_LIBS=ON -DWIMF_BUILD_TESTS=ON -DCMAKE_BUILD_TYPE=Release
cmake --build cmake-build --config Release
ctest --test-dir cmake-build --build-config Release --output-on-failure
```

Native changes should also pass the standalone compiler checks and the
sanitizer job in CI. If you touch SIMD kernels, run
`tools/wimf_simd_bench.cpp` and report the hardware in the PR.

## Format and codec changes

- WIM2 and WIM3 decoders are permanent compatibility surfaces. A change must
  never make an existing file undecodable.
- Bitstream changes need: an updated specification in `docs/`, new vectors in
  `tests/conformance/`, a regression test, and a `CHANGELOG.md` entry.
- Keep the Python reference implementation and the C++ core in agreement;
  state which one is authoritative in the PR.
- Add corruption-rejection coverage when parsing new fields.

## Pull requests

- Keep one logical change per PR.
- Update `CHANGELOG.md` under an `Unreleased` heading for user-visible changes.
- Update the relevant document in `docs/` when behaviour or the bitstream
  changes.
- Make sure CI is green; required Linux checks must pass before merge.
- Do not include secrets, tokens, private keys, or proprietary binaries.

## Reporting bugs and security issues

- Functional bugs: open an issue with the OS, Python version,
  `wimf runtime --json` output, and a minimal sample file when possible.
- Security-sensitive issues (decoder crashes, out-of-bounds reads, memory
  exhaustion, unsafe preview paths): follow `SECURITY.md` instead of opening a
  public issue.
