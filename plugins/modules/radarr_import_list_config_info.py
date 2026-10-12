#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_import_list_config_info

short_description: Get information about Radarr import list config.

version_added: "1.3.0"

description: Get information about Radarr import list config.

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch import list config
- name: fetch import list config
  devopsarr.radarr.radarr_import_list_config_info:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Import list config ID.
    type: int
    returned: always
    sample: '1'
list_sync_level:
    description: Import list sync level, for example C(disabled), C(logOnly) or C(keepAndUnmonitor).
    returned: always
    type: str
    sample: 'disabled'
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


def get_import_list_config(result):
    try:
        return helper.get()
    except radarr.ApiException as e:
        module.fail_json('Error getting import list config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting import list config: {}'.format(to_native(e)), **result)


def run_module():
    global helper
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    helper = RadarrConfigHelper(module.api, '/api/v3/config/importlist', SECRETS)
    result = dict(
        changed=False,
    )

    # Get resource.
    result.update(helper.view(get_import_list_config(result)))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
