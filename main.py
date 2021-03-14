import os
import click
from app import create_app
from app.libs.templating import create_info_template

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
create_info_template()


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names != ('', ):
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
