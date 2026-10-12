# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import re

MASK = '********'
SECRET_NAME = re.compile(r'apikey|api_key|password|passkey|cookie|token|secret|pid|rsskey|username', re.IGNORECASE)
SORTED_LISTS = ('fields', 'specifications', 'format_items')


def _dump(resource):
    # model, dict or nothing -> plain dict without empty values
    if resource is None:
        return {}
    if hasattr(resource, 'model_dump'):
        resource = resource.model_dump(by_alias=False, mode='json')
    return _drop_none(resource)


def _drop_none(value):
    if isinstance(value, dict):
        return dict((key, _drop_none(item)) for key, item in value.items() if item is not None)
    if isinstance(value, list):
        return [_drop_none(item) for item in value]
    return value


def _named(items):
    return bool(items) and all(isinstance(item, dict) and 'name' in item for item in items)


def _restrict(before, after):
    # Keep of the current resource only what the wanted one sets: the compared document.
    if isinstance(before, dict) and isinstance(after, dict):
        return dict((key, _restrict(before[key], value)) for key, value in after.items() if key in before)
    if isinstance(before, list) and isinstance(after, list):
        if _named(before) and _named(after):
            by_name = dict((item['name'], item) for item in before)
            return [_restrict(by_name[item['name']], item) for item in after if item['name'] in by_name]
        if len(before) == len(after):
            return [_restrict(old, new) for old, new in zip(before, after)]
    return before


def _field_names(value, secrets):
    # names of the fields to mask: secret looking ones and the ones masked by the server
    if isinstance(value, dict):
        for key, item in value.items():
            if key == 'fields' and isinstance(item, list):
                for field in item:
                    if isinstance(field, dict) and 'name' in field:
                        if SECRET_NAME.search(str(field['name'])) or field.get('value') == MASK:
                            secrets.add(field['name'])
            _field_names(item, secrets)
    elif isinstance(value, list):
        for item in value:
            _field_names(item, secrets)


def _clean(value, secrets):
    # mask the secret fields and sort the lists in a stable order
    if isinstance(value, dict):
        cleaned = {}
        for key, item in value.items():
            if key == 'fields' and isinstance(item, list):
                fields = [dict(name=field.get('name'), value=MASK if field.get('name') in secrets else field.get('value')) for field in item]
                cleaned[key] = sorted(fields, key=lambda field: str(field['name']))
            elif key in SORTED_LISTS and _named(item):
                cleaned[key] = sorted((_clean(entry, secrets) for entry in item), key=lambda entry: str(entry['name']))
            else:
                cleaned[key] = _clean(item, secrets)
        return cleaned
    if isinstance(value, list):
        return [_clean(item, secrets) for item in value]
    return value


def add_diff(module, result, before, after):
    """Set result['diff'] when the diff mode is on.

    before and after are models, dicts or None. Nothing sent to the API depends on this.
    """
    if not module._diff:
        return
    old = _dump(before)
    new = _dump(after)
    if not old and not new:
        return
    if old and new:
        old = _restrict(old, new)
    secrets = set()
    _field_names(old, secrets)
    _field_names(new, secrets)
    result['diff'] = dict(before=_clean(old, secrets), after=_clean(new, secrets))
