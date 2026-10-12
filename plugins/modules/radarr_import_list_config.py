#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_import_list_config

short_description: Manages Radarr import list config.

version_added: "1.3.0"

description:
    - Manages Radarr import list config.
    - Every option is optional. Only the options passed are changed, all the other settings are left untouched.

options:
    list_sync_level:
        description: Import list sync level, for example C(disabled), C(logOnly) or C(keepAndUnmonitor).
        type: str

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update import list config
- name: Update import list config
  devopsarr.radarr.radarr_import_list_config:
    list_sync_level: 'disabled'
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

OPTIONS = [
    'list_sync_level',
]

SECRETS = []


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        list_sync_level=dict(type='str'),
    )


def read_import_list_config(result):
    try:
        return helper.get()
    except radarr.ApiException as e:
        module.fail_json('Error getting import list config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting import list config: {}'.format(to_native(e)), **result)


def update_import_list_config(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = helper.update(want)
        except radarr.ApiException as e:
            module.fail_json('Error updating import list config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating import list config: {}'.format(to_native(e)), **result)
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
    helper = RadarrConfigHelper(module.api, '/api/v3/config/importlist', SECRETS)
    result = dict(
        changed=False,
        id=0,
    )

    # Get resource.
    state = read_import_list_config(result)
    result.update(helper.view(state))

    # Overlay only the options passed on the current resource.
    want, changed = helper.merge(state, module.params, OPTIONS)

    # Update an existing resource.
    if changed:
        update_import_list_config(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
