from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'ntbk',
    version = '0.0.1',
    author = 'Blake Bengtson',
    author_email = 'blake@962.dev',
    license = 'MIT',
    description = 'A simple, opinionated terminal notebook inspired by bullet journaling.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/bbeng89/ntbk',
    py_modules = ['main', 'ntbk'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Productivity",
    ],
    entry_points = '''
        [console_scripts]
        ntbk=main:main
    '''
)