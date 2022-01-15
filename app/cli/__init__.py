import os
import subprocess
import shlex
import click
from flask.cli import AppGroup
from flask_migrate import Migrate

dev = AppGroup("dev")
migrate = Migrate()


def run_sh(cmd: str, env=None, popen=False):
    copied_env = os.environ.copy()

    if env:
        copied_env.update(env)

    args = shlex.split(cmd)

    if popen:
        return subprocess.Popen(args, env=copied_env)

    ret = subprocess.call(args, env=copied_env)
    exit(ret)


@dev.command("test")
@click.option("--watch", default=False, is_flag=True, help="watch mode")
@click.argument("pytest_options", nargs=-1, type=click.UNPROCESSED)
def test(watch: bool, pytest_options):
    pytest_flags = " ".join(pytest_options)

    if watch:
        run_sh(f"ptw -- --testmon {pytest_flags}")

    run_sh(f"pytest {pytest_flags}")


@dev.command("db")
def run_db():
    run_sh("docker-compose up -d")


def run_server(popen=False):
    return run_sh(
        "flask run --host 0.0.0.0 --port 8080",
        env={"FLASK_ENV": "development"},
        popen=popen,
    )


def run_worker(popen=False):
    return run_sh(
        "watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery --app run_app:celery worker --without-gossip",
        env={"FLASK_ENV": "development"},
        popen=popen,
    )


@dev.command("server")
def run_server_command():
    return run_server()


@dev.command("worker")
def run_worker_command():
    return run_worker()


@dev.command("run")
def run_all():
    """Run both the worker and dev server"""
    procs = [run_worker(popen=True), run_server(popen=True)]
    for p in procs:
        p.wait()


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
