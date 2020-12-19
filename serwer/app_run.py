import click
from app.services.app import app as flask_app
from app import init_app

@click.group()
def cli():
    pass


@cli.command()
def run():
    flask_app.app_context().push()
    init_app()
    flask_app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    cli()
