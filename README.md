# devkit-toolbox-cli

A personal CLI toolbox — a growing collection of automation commands for
everyday tasks (files, system info, crypto utilities, productivity notes).
Built as an ongoing learning project and portfolio piece; it never really
"finishes", it grows over time.

## Status

🚧 Early development (MVP / v0.1). The `hash` command is implemented; the
rest of the planned commands are not built yet.

## Requirements

- Python 3.10+
- No third-party dependencies (the v0.1 MVP uses only the Python standard
  library)

## Installation

```bash
git clone git@github.com:decriptcypher/devkit-toolbox-cli.git
cd devkit-toolbox-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

The `-e` (editable) install links the `devkit` command straight to the
source code, so changes take effect immediately without reinstalling.

## Usage

```bash
devkit --help
```

### `hash` — generate a hash for a file or text

```bash
devkit hash <path>                 # hash a file's contents (default algorithm: sha256)
devkit hash "some text" --text     # hash literal text instead of a file
devkit hash <path> --algo md5      # choose the algorithm: md5, sha1, or sha256
```

Example:
```bash
$ devkit hash "hello" --text
2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b982
```

## Project structure

```
src/devkit/
├── cli.py             # entry point: argument parsing and command routing
└── crypto/
    └── hash.py         # `hash` command logic
```

Each command category lives in its own subpackage under `src/devkit/`.
Adding a new command means adding one file to the right subpackage plus one
registration line in `cli.py` — no need to touch anything else.

## Roadmap

- **v0.2** — automated tests (pytest), GitHub Actions CI
- **v0.3** — migrate from `argparse` to Typer + Rich for nicer output
- **v0.4** — publish to PyPI
- **v0.5+** — web3/crypto utility commands (gas price checks, download
  checksums, etc.), always avoiding any handling of real private
  keys/seed phrases

## Versioning

This project follows [SemVer](https://semver.org/) (`MAJOR.MINOR.PATCH`),
tracked in `pyproject.toml`. While in initial development, `MAJOR` stays at
`0` (e.g. `0.1.0`, `0.2.0`, ...).

## License

MIT — see [LICENSE](LICENSE).
