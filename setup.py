from distutils.core import setup

from alabama import __version__

with open('requirements/requirements-deploy.txt', 'r') as f:
    requirements = [line.strip().split()[0] for line in f
                    if not (line.startswith('#') or line.startswith('\n'))]

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='alabama',
    version=__version__,
    packages=['alabama'],
    license='MIT',
    description='Election map of Alabama',
    long_description=long_description,
    author='Don B. Fox',
    url='https://github.com/xofbd/alabama_election_map',
    install_requires=requirements
)
