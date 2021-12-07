from invoke import task

@task
def test(c, watch=False):
    if watch:
        c.run(f"ptw -- --testmon", pty=True)
        return
    
    
    c.run(f"pytest")
