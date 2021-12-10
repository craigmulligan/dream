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
flask dev db 
```

# Run test suite. 
```
flask dev test 
```

# Run test suite in watch mode.
```
flask dev test --watch
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

My dream app setup:

Tools:

* docker
* python
* hotwire
* sqlalchemy
* marshmallow (Anything better?)
* jinja
* black formatter
* mypy
* fly
