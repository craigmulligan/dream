> A boring but dreamy setup.

This setup is optimized for simplicity & development speed. This means minimal dependencies & infrastructure.

# Tools

* flask
* celery
* sqlite
* poetry
* black
* mypy

Getting started

# Init virtual-env.

```
poetry shell
```

# Install dependencies 

```
poetry install
```

# Run test suite. 
```
flask dev test 
```

# Run test suite in watch mode.
```
flask dev test --watch
```

# Run dev server and worker

```
flask dev run
```

# Run dev server 
```
flask dev server
```

# Run dev worker 
```
flask dev worker 
```

# Format code
```
flask dev fmt 
```

# Type-check code
```
flask dev mypy
```
