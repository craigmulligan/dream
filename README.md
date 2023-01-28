A boring but dreamy setup. 

Tools:

* poetry
* flask
* sqlalchemy
* celery
* black
* mypy
* hotwire / htmx
* fly.io

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
flask test 
```

# Run test suite in watch mode.
```
flask test --watch
```

# Run dev server and worker

```
flask all 
```

# Run dev server 
```
flask server --dev
```

# Run dev worker 
```
flask worker --dev
```

# Format code
```
flask fmt 
```

# Type-check code
```
flask mypy
```

# Create a new migration
```
flask db revision "new table" 
```
