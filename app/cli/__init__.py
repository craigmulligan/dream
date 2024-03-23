import os
import subprocess
import shlex
import click
from app import alembic

def run_sh(cmd: str, env=None, popen=False):
    copied_env = os.environ.copy()

    if env:
        copied_env.update(env)

    args = shlex.split(cmd)

    if popen:
        return subprocess.Popen(args, env=copied_env)

    proc = subprocess.run(args, env=copied_env, shell=True)
    exit(proc.returncode)


@click.command("test")
@click.option("--watch", default=False, is_flag=True, help="watch mode")
@click.argument("pytest_options", nargs=-1, type=click.UNPROCESSED)
def test(watch: bool, pytest_options):
    pytest_flags = " ".join(pytest_options)

    if watch:
        run_sh(f"ptw -- --testmon {pytest_flags}")

    run_sh(f"pytest {pytest_flags}")

def run_tailwind_install():
    # install tailwind
    if not os.path.isfile('./tailwindcss'):
        print('Installing tailwindcss')
        run_sh("curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64 && chmod +x tailwindcss-macos-arm64 && mv tailwindcss-macos-arm64 tailwindcss")


def run_tailwind_dev(popen=False):
    return run_sh(
        "./tailwindcss -i ./app/static/input.css -o ./app/static/output.css --watch",
        popen=popen,
    )

def run_server_dev(popen=False):
    return run_sh(
        "flask run --host 0.0.0.0 --port 8080",
        env={"FLASK_DEBUG": "True"},
        popen=popen,
    )


def run_worker_dev(popen=False):
    return run_sh(
        "watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery --app run_app:celery worker --without-gossip",
        env={"FLASK_DEBUG": "True"},
        popen=popen,
    )

@click.command("server")
@click.option("--dev", default=False, is_flag=True, help="dev mode")
def run_server(dev: bool):
    if dev:
        alembic.upgrade()
        run_tailwind_install()

        procs = [run_server_dev(popen=True), run_tailwind_dev(popen=True)]
        for p in procs:
            p.wait()
    else:
        return run_sh(
            "gunicorn 'run_app:app' -b 0.0.0.0:8080",
        )

@click.command("worker")
@click.option("--dev", default=False, is_flag=True, help="dev mode")
def run_worker(dev: bool):
    if dev:
        alembic.upgrade()
        return run_worker_dev()
    else:
        return run_sh("celery --app 'run_app:celery' worker --without-gossip -B -c 1 --pool solo")

@click.command("run")
@click.option("--dev", default=False, is_flag=True, help="dev mode")
def run_all(dev: bool):
    """Run both the worker and dev server"""
    if dev:
        alembic.upgrade()
        run_tailwind_install()

        procs = [run_worker_dev(popen=True), run_server_dev(popen=True), run_tailwind_dev(popen=True)]
        for p in procs:
            p.wait()
    else:
        raise Exception("Cant run all in production mode.")


@click.command("fmt")
@click.argument("black_options", nargs=-1, type=click.UNPROCESSED)
def run_fmt(black_options):
    black_flags = " ".join(black_options)
    run_sh(f"black . {black_flags}")


@click.command("mypy")
def run_typecheck():
    run_sh("pyright .")


def init_app(app):
    app.cli.add_command(test, "test")
    app.cli.add_command(run_typecheck, "types")
    app.cli.add_command(run_fmt, "fmt")
    app.cli.add_command(run_worker, "worker")
    app.cli.add_command(run_server, "server")
    app.cli.add_command(run_all, "all")
