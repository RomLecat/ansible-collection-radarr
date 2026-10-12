#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_ui_config_info

short_description: Get information about Radarr UI config.

version_added: "1.3.0"

description: Get information about Radarr UI config.

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch UI config
- name: fetch UI config
  devopsarr.radarr.radarr_ui_config_info:
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

SECRETS = []


def get_ui_config(result):
    try:
        return helper.get()
    except radarr.ApiException as e:
        module.fail_json('Error getting UI config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting UI config: {}'.format(to_native(e)), **result)


def run_module():
    global helper
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    helper = RadarrConfigHelper(module.api, '/api/v3/config/ui', SECRETS)
    result = dict(
        changed=False,
    )

    # Get resource.
    result.update(helper.view(get_ui_config(result)))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
