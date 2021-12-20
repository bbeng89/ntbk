import argparse
from datetime import date

import pytest
from freezegun import freeze_time

from ntbk import helpers


def test_parse_key_val_var():
    assert helpers.parse_key_val_var('key=val') == ('key', 'val')

def test_convert_key_value_vars_to_dict():
    kvps = ['key1=val1', 'key2=val2']
    dct = helpers.convert_key_value_vars_to_dict(kvps)
    assert dct == { 'key1': 'val1', 'key2': 'val2' }

@freeze_time('2022-01-01')
def test_get_today_alias():
    assert helpers.get_date_object_for_alias('today') == date(2022, 1, 1)

@freeze_time('2022-01-01')
def test_get_today_alias():
    assert helpers.get_date_object_for_alias('tomorrow') == date(2022, 1, 2)

@freeze_time('2022-01-01')
def test_get_today_alias():
    assert helpers.get_date_object_for_alias('yesterday') == date(2021, 12, 31)

def test_passing_date_returns_same_date():
    dt = date(2020, 1, 1)
    assert helpers.get_date_object_for_alias(dt) == dt

def test_passing_invalid_alias_returns_none():
    assert helpers.get_date_object_for_alias('two days ago') == None

def test_argparse_valid_iso_date():
    assert helpers.argparse_valid_iso_date('2021-01-01') == date(2021, 1, 1)

def test_arparse_valid_iso_date_fails():
    with pytest.raises(argparse.ArgumentTypeError):
        helpers.argparse_valid_iso_date('01/01/2021')