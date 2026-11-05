# Security policy

WIMF parses untrusted image files, so decoder robustness is part of the
project's security surface.

## Supported versions

Security fixes are applied to the latest released 3.x line, and to 2.x while
it remains the compatibility container for existing files. Please reproduce
against the newest release before reporting.

## Reporting a vulnerability

Please **do not open a public issue** for a suspected vulnerability.

Use GitHub's private vulnerability reporting on the repository
(**Security → Report a vulnerability**) or email **ivanm12453@gmail.com**.

Include, when possible:

- WIMF version (`python -c "import wimf; print(wimf.__version__)"`),
  operating system, architecture, and Python version
- `wimf runtime --json` output
- a minimal file or byte sequence that triggers the problem
- whether the native extension was active or the pure-Python fallback was used

## Scope

In scope:

- out-of-bounds reads/writes, integer overflow, or memory exhaustion caused by
  a crafted WIM2/WIM3/WIMF v1/AWIF file
- crashes or unbounded allocation in `wimf.inspect`, `wimf.diagnose`, the CLI,
  or the Pillow plugin
- path traversal or unsafe file handling in CLI commands
- unsafe deserialization of container metadata

Out of scope:

- denial of service that requires an already-untrusted, extremely large file
  and only wastes expected amounts of memory
- issues that require the user to run the `--unsafe-preview` path on a file
  they already trust
- vulnerabilities in third-party dependencies that are fixed upstream; report
  those to the dependency instead

We will acknowledge a report as soon as possible and coordinate disclosure
with you before any public write-up.
