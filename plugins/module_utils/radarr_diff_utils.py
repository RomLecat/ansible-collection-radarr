# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import re

MASK = '********'
SECRET_NAME = re.compile(r'apikey|api_key|password|passkey|cookie|token|secret|pid|rsskey|username', re.IGNORECASE)
SORTED_LISTS = ('fields', 'specifications', 'format_items')
# computed by the server, never sent (supports_* too)
SERVER_KEYS = ('info_link', 'implementation_name', 'message', 'presets', 'capabilities', 'privacy', 'added', 'sort_name', 'min_refresh_interval')
# computed by the server for a movie
MOVIE_SERVER_KEYS = (
    'alternate_titles', 'certification', 'clean_title', 'collection', 'digital_release', 'folder_name', 'genres', 'has_file', 'images', 'imdb_id',
    'in_cinemas', 'is_available', 'keywords', 'last_search_time',
    'movie_file', 'movie_file_id', 'original_language', 'original_title', 'overview', 'physical_release',
    'popularity', 'ratings', 'release_date', 'runtime', 'secondary_year_source_id', 'size_on_disk', 'sort_title', 'statistics', 'status', 'studio',
    'title_slug', 'website', 'year', 'you_tube_trailer_id')


def _dump(resource, ignore=()):
    # model, dict or nothing -> plain dict without empty values
    if resource is None:
        return {}
    if hasattr(resource, 'model_dump'):
        resource = resource.model_dump(by_alias=False, mode='json')
    if isinstance(resource, dict):
        resource = dict((key, item) for key, item in resource.items() if key not in ignore)
    return _drop_none(resource)


def _drop_none(value):
    if isinstance(value, dict):
        return dict(
            (key, _drop_none(item)) for key, item in value.items()
            if item is not None and key not in SERVER_KEYS and not key.startswith('supports_')
        )
    if isinstance(value, list):
        return [_drop_none(item) for item in value]
    return value


def _named(items):
    return bool(items) and all(isinstance(item, dict) and 'name' in item for item in items)


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


def add_diff(module, result, before, after, ignore=()):
    """Set result['diff'] when the diff mode is on.

    before is the live resource and after the exact resource sent, as models, dicts or None. Server computed keys
    are dropped on both sides, and the top level keys of ignore too. Nothing sent to the API depends on this.
    """
    if not module._diff:
        return
    old = _dump(before, ignore)
    new = _dump(after, ignore)
    if not old and not new:
        return
    secrets = set()
    _field_names(old, secrets)
    _field_names(new, secrets)
    result['diff'] = dict(before=_clean(old, secrets), after=_clean(new, secrets))
