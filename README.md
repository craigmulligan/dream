My dream app setup:

Tools:

* poetry
* flask
* sqlalchemy
* celery
* black
* mypy
* hotwire / htmx
* fly

Getting started

# Init virtual-env.

```
poetry shell
```

# Install dependencies 

```
poetry install
```

# Run db.

```
flask dev db && flask db upgrade
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

# Create a new migration
```
flask db migrate
```
