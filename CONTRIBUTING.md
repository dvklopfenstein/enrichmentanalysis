# Enrichment Analysis pull request guidelines

* [**When to confer**](#when-to-confer)
* [**Submitting a Pull Request**](#submitting-a-pull-request)

## When to confer
If you are adding tests, documentation, or bug fixes please open a pull request.

If you are adding new functionality, please email to strategize architectural changes.

## Submitting a Pull Request

When submitting a pull request, please:

1. Add unit tests which test new code
2. Properly comment all new code
3. Run `pylint` on all new code
4. Run `make pytest`: All existing tests must pass
5. Add new unit tests to the pytest makefile target
6. Check GitHub's [**About pull requests**](https://help.github.com/en/articles/about-pull-requests#initiating-the-pull-request) to submit a quality pull request
7. Ensure your commit messages [**are informative**](https://docs.scipy.org/doc/numpy/dev/gitwash/development_workflow.html#writing-the-commit-message)    

Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
