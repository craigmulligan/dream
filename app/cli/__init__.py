import os
import subprocess
import shlex
import click
from flask.cli import AppGroup
from flask_migrate import Migrate

dev = AppGroup("dev")
migrate = Migrate()

def run_sh(cmd: str, env=None):
    copied_env = os.environ.copy()

    if env:
        copied_env.update(env)
    subprocess.call(shlex.split(cmd), env=copied_env)

@dev.command("test")
@click.option("--watch", default=False, is_flag=True)
def test_watch(watch: bool):
    if watch:
        run_sh(f"ptw -- --testmon")
        return

    run_sh(f"pytest")


@dev.command("db")
def run_db():
    run_sh('docker-compose up -d')

@dev.command("server")
def run_server():
    run_sh("flask run --host 0.0.0.0 --port 8080", env={"FLASK_ENV": "development"})

@dev.command("worker")
def run_worker():
    run_sh("celery --app run_app:celery worker")

def register_cli(app, db):
    app.cli.add_command(dev)
    migrate.init_app(app, db)
