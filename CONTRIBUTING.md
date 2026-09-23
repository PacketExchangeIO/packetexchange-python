# Contributing

Thank you for helping improve the PacketExchange Python SDK. Bug reports, fixes and
documentation improvements are welcome.

## Before you start

- For a bug, open an issue with a minimal reproduction. Remove API keys, webhook secrets,
  phone numbers and other personal data first.
- For a new feature or a change to the public API, open an issue to discuss it before
  sending a pull request.
- Report security vulnerabilities privately as described in [SECURITY.md](SECURITY.md).
- Questions about your account, billing or the API itself go to [support@packetexchange.io](mailto:support@packetexchange.io).

## Development setup

You need Python 3.9 or later; the pinned toolchain in `requirements-dev.txt` targets
Python 3.12.

```bash
git clone https://github.com/PacketExchangeIO/packetexchange-python.git
cd packetexchange-python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt -e .
pytest
mypy
python -m build
```

The tests use `httpx.MockTransport`. They must never call the live API: it costs money
and sends real messages.

## Project layout

| Path | Contents |
| --- | --- |
| `src/packetexchange/_client.py` | The `PacketExchange` client and its resources |
| `src/packetexchange/_errors.py` | `PacketExchangeError` |
| `src/packetexchange/_webhooks.py` | `verify_webhook_signature` |
| `src/packetexchange/_generated/` | Models and the operation table generated from `openapi.json` (do not edit by hand) |
| `scripts/generate.py` | The generator |
| `tests/` | Tests (pytest) |

## Making a change

1. Create a branch from `main`.
2. Make your change, following the existing style: small typed methods, one per endpoint,
   each with a short docstring naming the method and path. Python argument names are
   snake_case and map to the API's camelCase fields.
3. Add or update tests in `tests/`.
4. If `openapi.json` changed, run `python scripts/generate.py`. CI fails if the generated
   files are out of date.
5. Run `pytest`, `mypy` and `python -m build`.
6. Add an entry under **Unreleased** in `CHANGELOG.md`.
7. Open a pull request and fill in the template.

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE) and that you will follow the [Code of Conduct](CODE_OF_CONDUCT.md).
