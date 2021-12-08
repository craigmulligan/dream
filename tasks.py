from invoke import task

@task
def db(c):
    c.run(f"docker-compose up -d", pty=True)

@task
def test(c, watch=False):
    db(c)
    if watch:
        c.run(f"ptw -- --testmon", pty=True)
        return
    
    
    c.run(f"pytest")



