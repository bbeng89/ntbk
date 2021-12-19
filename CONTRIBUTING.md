# Contributing to NTBK

## Setting up the project

Clone the repository and cd into it. 

```console
foo@bar:~$ git clone git@github.com:bbeng89/ntbk.git
foo@bar:~$ cd ntbk
```

Create a virtualenv called "venv" and activate it

```console
foo@bar:~$ python3 -m venv venv
foo@bar:~$ source venv/bin/activate
```

Install the app for development

```console
foo@bar:~$ python setup.py develop
```

## Tests

Tests are written using [pytest](https://docs.pytest.org/en/6.2.x/), [pytest-mock](https://github.com/pytest-dev/pytest-mock/), and [freeze gun](https://github.com/spulec/freezegun).

Run all tests:

```console
foo@bar:~$ pytest
```