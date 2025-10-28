Developer setup and testing
===========================

This project uses a few optional system-level libraries (audio, rpi hardware) that
you may not have installed on your development machine. On Debian/Ubuntu environments
the system Python may be "externally managed" (PEP 668), which prevents installing
packages system-wide with pip. To avoid that, use a virtual environment.

Quickstart (recommended)
-------------------------

1. Create and populate a virtualenv:

```bash
./scripts/setup_dev.sh python3
```

2. Activate it:

```bash
source .venv/bin/activate
```

3. Run tests and linters:

```bash
./scripts/run_tests.sh
```

Notes about the PEP 668 error
-----------------------------
If you see "externally-managed-environment" when running `pip install`, that means
your OS (or Python distribution) prevents pip from changing system-wide packages.
The `setup_dev.sh` script above creates a local venv to avoid that issue.

CI

The repository contains a GitHub Actions workflow at `.github/workflows/ci.yml` that
installs runtime + dev dependencies and runs tests + flake8 on pushes and PRs.

Secrets & CI
-----------

Do not store API keys or other secrets in `config/` files or commit them to the repo.
Use environment variables locally and GitHub Actions secrets in CI. The reasoning
engine and interface will prefer environment variables if present:

- `OPEN_WEBUI_API_KEY` — API key for Open Web UI (sent as `Authorization: Bearer <key>` by default)
- `OPEN_WEBUI_API_KEY_STYLE` — optional; set to `x-api-key` to send the key as `X-API-Key` header
- `OLLAMA_API_KEY` — API key for Ollama (if your Ollama deployment requires auth)
- `OLLAMA_API_KEY_STYLE` — optional style for Ollama (defaults to `bearer`)

To add a secret to GitHub Actions, go to your repository Settings → Secrets → Actions and add a new secret
named `OPEN_WEBUI_API_KEY` (or `OLLAMA_API_KEY`). Then reference it in your workflow as `secrets.OPEN_WEBUI_API_KEY`.

Locally you can export the variable in your shell for testing (don't commit):

```bash
export OPEN_WEBUI_API_KEY='sk_live_...'
export OPEN_WEBUI_API_KEY_STYLE='bearer'
```

CI guidance: in your workflow set the env for the job or step:

```yaml
env:
	OPEN_WEBUI_API_KEY: ${{ secrets.OPEN_WEBUI_API_KEY }}
```

This keeps secrets out of the code and avoids accidental commits.

Run secret-enabled CI job manually
-------------------------------

The workflow now supports manual runs from the Actions UI. This is useful when you
have added `OPEN_WEBUI_API_KEY` (and optionally `OPEN_WEBUI_API_KEY_STYLE`) to your
repository secrets and want to run the tests that validate secret-dependent behavior.

Steps:

1. In GitHub go to Settings → Secrets → Actions and add `OPEN_WEBUI_API_KEY` (and
	`OPEN_WEBUI_API_KEY_STYLE` if needed).
2. Open the Actions tab in the repository, select the `CI` workflow, and click
	"Run workflow". Choose the branch and run. The optional job "Tests (with secrets)"
	will run if the `OPEN_WEBUI_API_KEY` secret is present.

Local equivalent
----------------

You can also run the secret-enabled tests locally by exporting the variables and
running the specific tests. Example:

```bash
export OPEN_WEBUI_API_KEY='sk_live_...'
export OPEN_WEBUI_API_KEY_STYLE='bearer'
python -m unittest -v test_interface_ui.py
```

Remember to `unset` the env vars when done, or run tests in a disposable shell.

Secret-only workflow
--------------------

There's also a dedicated manual workflow in `.github/workflows/secret-tests.yml` that
you can run from the Actions UI (Run workflow). It is intended for maintainers to run
secret-enabled tests in isolation and reads API keys from repository secrets. Use this
if you want to validate integrations that require API keys without affecting the
default CI matrix.
