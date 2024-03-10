# Inky Pi

[![pypi](https://img.shields.io/pypi/v/inky-pi)](https://pypi.org/project/inky-pi/)
[![python](https://img.shields.io/pypi/pyversions/inky-pi.svg)](https://pypi.org/project/inky-pi/)
[![build](https://github.com/mickeykkim/inky_pi/actions/workflows/main.yml/badge.svg)](https://github.com/mickeykkim/inky_pi/actions/workflows/main.yml)
[![docs](https://readthedocs.org/projects/inky-pi/badge/?version=latest)](https://inky-pi.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/mickeykkim/inky_pi/branch/main/graph/badge.svg?token=0RT5PRPRTZ)](https://codecov.io/gh/mickeykkim/inky_pi)
[![Maintainability](https://api.codeclimate.com/v1/badges/b0f2104a75145d097108/maintainability)](https://codeclimate.com/github/mickeykkim/inky_pi/maintainability)

Inky_pi is a project to display train and weather data on an [Inky](https://github.com/pimoroni/inky) e-ink display
using a Raspberry Pi. It is modular and fetches data from a variety of
sources ([OpenLDBWS](http://lite.realtime.nationalrail.co.uk/openldbws/), [Huxley2](https://huxley2.azurewebsites.net/), [OpenWeatherMap](https://openweathermap.org/)).

![image 1](https://i.imgur.com/gkSz0xp.jpeg)

Example outputs (generated with `desktop` output option):

![weather_train](https://i.imgur.com/dkTOQPH.jpg)
![weather_only](https://i.imgur.com/4PohWbR.jpg)

Example terminal output (generated with `terminal` output option):

```bash
╭────────────── InkyPi Terminal Output ──────────────╮
│ Sun 10 Mar 2024                                    │
│ 16:03                                              │
│ 🌦                                                 │
│ Current Weather:                                   │
│ Temperature: 9.0°C                                 │
│ Condition: Rain                                    │
│ Today's Temperature Range: 7.5°C – 9.0°C           │
│ Today's Condition: moderate rain                   │
│ Tomorrow's Condition: overcast clouds              │
│ Train schedule from Kingston to London Waterloo:   │
│ 16:04 | P3 to London Waterloo - On time            │
│ 16:12 | P3 to London Waterloo - On time            │
│ 16:34 | P3 to London Waterloo - On time            │
╰────────────────────────────────────────────────────╯
```

Weather icon drawing code was adapted from [raspi-weather](https://github.com/DerekCaelin/raspi-weather).

Project setup was aided using [Sam Brigg](https://github.com/briggySmalls)'s [cookiecutter template](https://github.com/briggySmalls/cookiecutter-pypackage) fork.

## Installation

Use the [Poetry](https://python-poetry.org/) package manager to install Inky_pi.

```bash
poetry install
```

## Usage

```bash
poetry shell
inky_pi display --help
```

Alternatively, the program can be called via its main function.

```bash
poetry shell
python -m inky_pi --help
```

The program can be configured by
running `python -m inky_web` to launch the configuration editor web interface. The web interface creates/edits the
local `.env` file which holds application configuration.

![image 2](https://i.imgur.com/MOLEZBl.png)

API keys for configuration are needed for train data using OpenLDBWS and for weather data using OpenWeatherMap.
Alternatively, train data can be fetched using Huxley2 without an API key (though the maintainer contends that the
Huxley2 server goes down often without notice). A module for Weather Underground could be easily written as a
contribution/exercise.

The program runs once per invocation. For automated scheduling, [cron](https://www.mankier.com/8/cron) is recommended using the `python main.py` invocation as described above.

## Development Tools

Development tools can be run using [Invoke](http://www.pyinvoke.org/).

#### Virtual Environment: [Poetry](https://python-poetry.org/)

A Poetry virtual environment must be created before running any dev tools:

```bash
poetry shell
```

#### Linting and Type Analysis: [Pylint](https://www.pylint.org/), [Flake8](https://flake8.pycqa.org/en/latest/), [ruff](https://pypi.org/project/ruff/), and [mypy](http://mypy-lang.org/)

```bash
invoke lint
```

#### Formatting: [Black](https://pypi.org/project/black/), [isort](https://pycqa.github.io/isort/), and [ssort](https://pypi.org/project/ssort/).

```bash
invoke format
```

#### Testing: [Pytest](https://docs.pytest.org/)

```bash
invoke test
invoke coverage
```

#### Docs Generation: [Sphinx](https://www.sphinx-doc.org/en/master/)

```bash
invoke docs
```

#### CI Workflow: [Tox](https://tox.readthedocs.io/en/latest/)

```bash
tox
```

CI/CD is [configured](https://github.com/mickeykkim/inky_pi/blob/main/.github/workflows/main.yml) and run
using [GitHub Actions](https://docs.github.com/en/actions/reference).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to add/update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
