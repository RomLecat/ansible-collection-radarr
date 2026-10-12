#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_ui_config

short_description: Manages Radarr UI config.

version_added: "1.3.0"

description:
    - Manages Radarr UI config.
    - Every option is optional. Only the options passed are changed, all the other settings are left untouched.

options:
    first_day_of_week:
        description: First day of the week, 0 is Sunday.
        type: int
    calendar_week_column_header:
        description: Calendar week column header format.
        type: str
    movie_runtime_format:
        description: Movie runtime format.
        type: str
        choices: ["hoursMinutes", "minutes"]
    short_date_format:
        description: Short date format.
        type: str
    long_date_format:
        description: Long date format.
        type: str
    time_format:
        description: Time format.
        type: str
    show_relative_dates:
        description: Show relative dates.
        type: bool
    enable_color_impaired_mode:
        description: Enable color impaired mode.
        type: bool
    movie_info_language:
        description: Movie info language ID.
        type: int
    ui_language:
        description: UI language ID.
        type: int
    theme:
        description: Theme, for example C(auto), C(light) or C(dark).
        type: str

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update UI config
- name: Update UI config
  devopsarr.radarr.radarr_ui_config:
    first_day_of_week: 0
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: UI config ID.
    type: int
    returned: always
    sample: '1'
first_day_of_week:
    description: First day of the week, 0 is Sunday.
    returned: always
    type: int
    sample: 0
calendar_week_column_header:
    description: Calendar week column header format.
    returned: always
    type: str
    sample: 'ddd M/D'
movie_runtime_format:
    description: Movie runtime format.
    returned: always
    type: str
    sample: 'hoursMinutes'
short_date_format:
    description: Short date format.
    returned: always
    type: str
    sample: 'MMM D YYYY'
long_date_format:
    description: Long date format.
    returned: always
    type: str
    sample: 'dddd, MMMM D YYYY'
time_format:
    description: Time format.
    returned: always
    type: str
    sample: 'h(:mm)a'
show_relative_dates:
    description: Show relative dates.
    returned: always
    type: bool
    sample: true
enable_color_impaired_mode:
    description: Enable color impaired mode.
    returned: always
    type: bool
    sample: false
movie_info_language:
    description: Movie info language ID.
    returned: always
    type: int
    sample: 1
ui_language:
    description: UI language ID.
    returned: always
    type: int
    sample: 1
theme:
    description: Theme, for example C(auto), C(light) or C(dark).
    returned: always
    type: str
    sample: 'auto'
'''

from ansible_collections.devopsarr.radarr.plugins.module_utils.radarr_module import RadarrModule
from ansible_collections.devopsarr.radarr.plugins.module_utils.radarr_config_utils import RadarrConfigHelper
from ansible.module_utils.common.text.converters import to_native

try:
    import radarr
    HAS_RADARR_LIBRARY = True
except ImportError:
    HAS_RADARR_LIBRARY = False

OPTIONS = [
    'first_day_of_week',
    'calendar_week_column_header',
    'movie_runtime_format',
    'short_date_format',
    'long_date_format',
    'time_format',
    'show_relative_dates',
    'enable_color_impaired_mode',
    'movie_info_language',
    'ui_language',
    'theme',
]

SECRETS = []


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        first_day_of_week=dict(type='int'),
        calendar_week_column_header=dict(type='str'),
        movie_runtime_format=dict(type='str', choices=["hoursMinutes", "minutes"]),
        short_date_format=dict(type='str'),
        long_date_format=dict(type='str'),
        time_format=dict(type='str'),
        show_relative_dates=dict(type='bool'),
        enable_color_impaired_mode=dict(type='bool'),
        movie_info_language=dict(type='int'),
        ui_language=dict(type='int'),
        theme=dict(type='str'),
    )


def read_ui_config(result):
    try:
        return helper.get()
    except radarr.ApiException as e:
        module.fail_json('Error getting UI config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting UI config: {}'.format(to_native(e)), **result)


def update_ui_config(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = helper.update(want)
        except radarr.ApiException as e:
            module.fail_json('Error updating UI config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating UI config: {}'.format(to_native(e)), **result)
        result.update(helper.view(response))
    else:
        result.update(helper.view(want))
    # No need to exit module since it will exit by default either way


def run_module():
    global helper
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )

    # Init client and result.
    helper = RadarrConfigHelper(module.api, '/api/v3/config/ui', SECRETS)
    result = dict(
        changed=False,
        id=0,
    )

    # Get resource.
    state = read_ui_config(result)
    result.update(helper.view(state))

    # Overlay only the options passed on the current resource.
    want, changed = helper.merge(state, module.params, OPTIONS)

    # Update an existing resource.
    if changed:
        update_ui_config(want, result)
        if module._diff:
            result['diff'] = dict(before=helper.view(state), after=helper.view(want))

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
