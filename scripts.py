"""
Project lifecycle scripts defined in pyproject.toml
"""
import subprocess

def tests():
    """ Run all unit tests and report test coverage """
    subprocess.run(
        ['coverage', 'run', '--omit', '*/site-packages/*,tests/*', '-m', 'pytest', 'tests/']
    )
    subprocess.run(
        ['coverage', 'report']
    )
