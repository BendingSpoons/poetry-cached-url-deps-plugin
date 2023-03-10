# poetry-cached-url-deps-plugin

This [Poetry](https://python-poetry.org/) plugin implements a hackish way of solving https://github.com/python-poetry/poetry/issues/2415, i.e. `url` dependencies not being cached by Poetry dependency resolution.

## Installation

Until the plugin is published on PyPI, you can install it as:
```bash
poetry self add git+https://github.com/BendingSpoons/poetry-cached-url-deps-plugin.git#1.0.0
```

## How does it work

The plugin is really an hack over the Poetry codebase and not a perfect one, for which more intrusive changes would need to be performed.

The hack consists of creating a fake `_url` cache repository (you'll see it when running `poetry cache list` as soon as an object got cached) and using that when downloading url dependencies. As a consequence, you'll still see `Downloading...` your url dependencies every time although they will be read from the filesystem - it's an extra filesystem operation that will be avoided with a better solution.

Since the plugin mocks Poetry internals, we pin the version of Poetry with which this plugin is compatible to an exact version. Future releases of Poetry may possibly require a rework of this plugin or render the hack impossible to achieve. As we are supporting the Poetry community with contributions to the main repo, we hope they will be integrated in future releases, making this plugin ideally useless.
