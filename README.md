mdgt
====
**mdgt** (spoken: "midget") is a microservice which parses microdata.  mdgt is still
in the initial design and development phase.

Quick Instructions
------------------
**Command Line Output:** `python -m mdgt [options] [provider] [query]`

* `[provider]` The name of the provider, must be in `/providers/`
* `[query]` The query the provider will use to obtain output

Options:
* `--console`, `-c`: Output to stdout in a readable format (default)
* `--json`, `-j`: Output to stdout as json
* `--providers`, `-p`: Output to stdout a list of available providers

**RESTful Web Server**: `python -m mdgt -w [port(optional)]`

This starts a WSGI-compliant web server at the specified port (default `8181`).  The
api is invoked with `http://domain:port/provider/query`, or `http://domain:port/providers`
(for a list of available providers).

Development instructions
------------------------
**Windows:** Use the handy win_init.ps1 script to set up the virtual
environment and install dependencies to it. PyPI doesn't have 64-bit binaries
for lxml, so the whl file is included and installed from the script.

**Linux/Mac users:** Set up a virtual environment with `python -m venv venv`, activate it,
then install the dependencies with `pip install requirements.txt`.
