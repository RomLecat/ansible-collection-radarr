#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_metadata_config

short_description: Manages Radarr metadata config.

version_added: "1.3.0"

description:
    - Manages Radarr metadata config.
    - Every option is optional. Only the options passed are changed, all the other settings are left untouched.

options:
    certification_country:
        description: Certification country, as a lowercase TMDb country code.
        type: str
        choices: ["au", "br", "ca", "fr", "de", "gb", "ie", "it", "es", "us", "nz"]

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update metadata config
- name: Update metadata config
  devopsarr.radarr.radarr_metadata_config:
    certification_country: 'us'
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Metadata config ID.
    type: int
    returned: always
    sample: '1'
certification_country:
    description: Certification country, as a lowercase TMDb country code.
    returned: always
    type: str
    sample: 'us'
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
    'certification_country',
]

SECRETS = []


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        certification_country=dict(type='str', choices=["au", "br", "ca", "fr", "de", "gb", "ie", "it", "es", "us", "nz"]),
    )


def read_metadata_config(result):
    try:
        return helper.get()
    except radarr.ApiException as e:
        module.fail_json('Error getting metadata config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting metadata config: {}'.format(to_native(e)), **result)


def update_metadata_config(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = helper.update(want)
        except radarr.ApiException as e:
            module.fail_json('Error updating metadata config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating metadata config: {}'.format(to_native(e)), **result)
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
    helper = RadarrConfigHelper(module.api, '/api/v3/config/metadata', SECRETS)
    result = dict(
        changed=False,
        id=0,
    )

    # Get resource.
    state = read_metadata_config(result)
    result.update(helper.view(state))

    # Overlay only the options passed on the current resource.
    want, changed = helper.merge(state, module.params, OPTIONS)

    # Update an existing resource.
    if changed:
        update_metadata_config(want, result)
        if module._diff:
            result['diff'] = dict(before=helper.view(state), after=helper.view(want))

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
