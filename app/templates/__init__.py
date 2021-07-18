from jinja2 import Environment, PackageLoader, select_autoescape

templates = Environment(
    loader=PackageLoader(__name__, "."), autoescape=select_autoescape()
)
