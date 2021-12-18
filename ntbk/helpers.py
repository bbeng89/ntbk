# system imports
from datetime import date, timedelta
from argparse import ArgumentTypeError


def parse_key_val_var(var_str):
    """Helper: Takes a string in the format foo=bar and converts it to a tuple ('foo', 'bar')"""
    items = var_str.split('=')
    return (items[0].strip(), items[1].strip())


def convert_key_value_vars_to_dict(var_list):
    """Helper: Takes a list like ['foo=bar', 'bar=baz'] and converts it to {'foo': 'bar', 'bar': 'baz'} """
    vars = {}
    for var in var_list:
        key, value = parse_key_val_var(var)
        vars[key] = value
    return vars


def get_date_object_for_alias(alias):
    """Helper: get a datetime object for a given alias"""
    if isinstance(alias, date):
        return alias # it's already a date
    elif alias == 'today':
        return date.today()
    elif alias == 'yesterday':
        return date.today() - timedelta(days=1)
    elif alias == 'tomorrow':
        return date.today() + timedelta(days=1)
    return None

def argparse_valid_iso_date(self, s):
    """Helper: Validator used by argparse to make sure given dates are in ISO format"""
    try:
        return date.fromisoformat(s)
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise ArgumentTypeError(msg)
