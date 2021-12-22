import os
import subprocess
import shlex
import click
from flask.cli import AppGroup
from flask_migrate import Migrate

dev = AppGroup("dev")
migrate = Migrate()


def flags_to_str(**kwargs) -> str:
    flag_str = ""
    for key, value in kwargs.items():
        if value:
            if isinstance(value, bool):
                flag_str = flag_str + f" -{key}"
            else:
                flag_str = flag_str + f" -{key}={value}"

    return flag_str


def run_sh(cmd: str, env=None):
    copied_env = os.environ.copy()

    if env:
        copied_env.update(env)
    ret = subprocess.call(shlex.split(cmd), env=copied_env)
    exit(ret)


@dev.command("test")
@click.option("--watch", default=False, is_flag=True, help="watch mode")
@click.argument("pytest_options", nargs=-1, type=click.UNPROCESSED)
def test(watch: bool, rest):
    pytest_flags = " ".join(rest)

    if watch:
        run_sh(f"ptw -- --testmon {pytest_flags}")

    run_sh(f"pytest {pytest_flags}")


@dev.command("db")
def run_db():
    run_sh("docker-compose up -d")


@dev.command("server")
def run_server():
    run_sh("flask run --host 0.0.0.0 --port 8080", env={"FLASK_ENV": "development"})


@dev.command("worker")
def run_worker():
    run_sh(
        "watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery --app run_app:celery worker --without-gossip"
    )


@dev.command("fmt")
@click.argument("black_options", nargs=-1, type=click.UNPROCESSED)
def run_fmt(black_options):
    black_flags = " ".join(black_options)
    run_sh(f"black . {black_flags}")


@dev.command("mypy")
def run_mypy():
    run_sh("mypy .")


def register_cli(app, db):
    app.cli.add_command(dev)
    migrate.init_app(app, db)
