# Python Continuous Performance Tests
Command line interface based on [typer](https://typer.tiangolo.com/)

## Installation
- Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- `conda config --add channels conda-forge`
- `conda config --add channels anaconda` (pytest)
- install required modules by `conda env create --file=conda_env.yaml`
- note that module `psycopg2` requires `pg_config` i.e. postgres client tools 

- [Download poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer)
  -- `curl -sSL https://install.python-poetry.org | python3 -`
- 
- in this directory call `poetry install` (expects poetry on the PATH)
- `poetry shell`

## Commands
Commands expect working directory (i.e. directory where they are started) equal to CPT root. `--help` list
available options. Works equally from (git) bash and Windows. General
`python bin/pycpt/{command}.py --help`

- [child_pipeline](child_pipeline.py) runs frontend and GQL API test
- [compare_cmd](compare_cmd.py) compares 2 measurements
- [job_stats](job_stats.py) extract job stats from mmm and dpm database
- [redeploy_paas](redeploy_paas.py) manage kustomize based PaaS deployments
  `python bin/pycpt/redeploy_paas.py --test-env paas_ci --step show_steps` shows all available steps with
  step description
- [process_fe_log](process_fe_log.py) process request-response fe log
- [post_elk_events](post_elk_events.py) post off-line events to ELK (no check for `elk.sent.events` property )
