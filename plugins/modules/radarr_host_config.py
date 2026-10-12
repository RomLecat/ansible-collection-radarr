#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_host_config

short_description: Manages Radarr host config.

version_added: "1.3.0"

description:
    - Manages Radarr host config.
    - Every option is optional. Only the options passed are changed, all the other settings are left untouched.

options:
    bind_address:
        description: Address Radarr binds to.
        type: str
    port:
        description: HTTP port.
        type: int
    ssl_port:
        description: HTTPS port.
        type: int
    enable_ssl:
        description: Enable SSL.
        type: bool
    launch_browser:
        description: Launch the browser on startup.
        type: bool
    authentication_method:
        description: Authentication method.
        type: str
        choices: ["none", "basic", "forms", "external"]
    authentication_required:
        description: Authentication requirement.
        type: str
        choices: ["enabled", "disabledForLocalAddresses"]
    analytics_enabled:
        description: Send anonymous usage and error information.
        type: bool
    username:
        description: Username.
        type: str
    password:
        description: Password.
        type: str
    password_confirmation:
        description: Password confirmation, to be passed with I(password).
        type: str
    log_level:
        description: Log level.
        type: str
    log_size_limit:
        description: Log size limit in MB.
        type: int
    console_log_level:
        description: Console log level.
        type: str
    branch:
        description: Update branch.
        type: str
    api_key:
        description: API key of the Radarr instance.
        type: str
    ssl_cert_path:
        description: Path of the SSL certificate.
        type: str
    ssl_cert_password:
        description: Password of the SSL certificate.
        type: str
    url_base:
        description: URL base.
        type: str
    instance_name:
        description: Instance name.
        type: str
    application_url:
        description: Application URL.
        type: str
    update_automatically:
        description: Install updates automatically.
        type: bool
    update_mechanism:
        description: Update mechanism.
        type: str
        choices: ["builtIn", "script", "external", "apt", "docker"]
    update_script_path:
        description: Path of the update script.
        type: str
    proxy_enabled:
        description: Use a proxy.
        type: bool
    proxy_type:
        description: Proxy type.
        type: str
        choices: ["http", "socks4", "socks5"]
    proxy_hostname:
        description: Proxy hostname.
        type: str
    proxy_port:
        description: Proxy port.
        type: int
    proxy_username:
        description: Proxy username.
        type: str
    proxy_password:
        description: Proxy password.
        type: str
    proxy_bypass_filter:
        description: Comma separated list of addresses that bypass the proxy.
        type: str
    proxy_bypass_local_addresses:
        description: Bypass the proxy for local addresses.
        type: bool
    certificate_validation:
        description: Certificate validation.
        type: str
        choices: ["enabled", "disabledForLocalAddresses", "disabled"]
    backup_folder:
        description: Backup folder.
        type: str
    backup_interval:
        description: Backup interval in days.
        type: int
    backup_retention:
        description: Backup retention in days.
        type: int

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update host config
- name: Update host config
  devopsarr.radarr.radarr_host_config:
    bind_address: '*'
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Host config ID.
    type: int
    returned: always
    sample: '1'
bind_address:
    description: Address Radarr binds to.
    returned: always
    type: str
    sample: '*'
port:
    description: HTTP port.
    returned: always
    type: int
    sample: 7878
ssl_port:
    description: HTTPS port.
    returned: always
    type: int
    sample: 9898
enable_ssl:
    description: Enable SSL.
    returned: always
    type: bool
    sample: false
launch_browser:
    description: Launch the browser on startup.
    returned: always
    type: bool
    sample: true
authentication_method:
    description: Authentication method.
    returned: always
    type: str
    sample: 'external'
authentication_required:
    description: Authentication requirement.
    returned: always
    type: str
    sample: 'enabled'
analytics_enabled:
    description: Send anonymous usage and error information.
    returned: always
    type: bool
    sample: true
username:
    description: Username.
    returned: always
    type: str
    sample: 'radarr'
log_level:
    description: Log level.
    returned: always
    type: str
    sample: 'info'
log_size_limit:
    description: Log size limit in MB.
    returned: always
    type: int
    sample: 1
console_log_level:
    description: Console log level.
    returned: always
    type: str
    sample: ''
branch:
    description: Update branch.
    returned: always
    type: str
    sample: 'master'
ssl_cert_path:
    description: Path of the SSL certificate.
    returned: always
    type: str
    sample: ''
url_base:
    description: URL base.
    returned: always
    type: str
    sample: ''
instance_name:
    description: Instance name.
    returned: always
    type: str
    sample: 'Radarr'
application_url:
    description: Application URL.
    returned: always
    type: str
    sample: ''
update_automatically:
    description: Install updates automatically.
    returned: always
    type: bool
    sample: true
update_mechanism:
    description: Update mechanism.
    returned: always
    type: str
    sample: 'docker'
update_script_path:
    description: Path of the update script.
    returned: always
    type: str
    sample: ''
proxy_enabled:
    description: Use a proxy.
    returned: always
    type: bool
    sample: false
proxy_type:
    description: Proxy type.
    returned: always
    type: str
    sample: 'http'
proxy_hostname:
    description: Proxy hostname.
    returned: always
    type: str
    sample: ''
proxy_port:
    description: Proxy port.
    returned: always
    type: int
    sample: 8080
proxy_username:
    description: Proxy username.
    returned: always
    type: str
    sample: ''
proxy_bypass_filter:
    description: Comma separated list of addresses that bypass the proxy.
    returned: always
    type: str
    sample: ''
proxy_bypass_local_addresses:
    description: Bypass the proxy for local addresses.
    returned: always
    type: bool
    sample: true
certificate_validation:
    description: Certificate validation.
    returned: always
    type: str
    sample: 'enabled'
backup_folder:
    description: Backup folder.
    returned: always
    type: str
    sample: 'Backups'
backup_interval:
    description: Backup interval in days.
    returned: always
    type: int
    sample: 7
backup_retention:
    description: Backup retention in days.
    returned: always
    type: int
    sample: 28
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
    'bind_address',
    'port',
    'ssl_port',
    'enable_ssl',
    'launch_browser',
    'authentication_method',
    'authentication_required',
    'analytics_enabled',
    'username',
    'password',
    'password_confirmation',
    'log_level',
    'log_size_limit',
    'console_log_level',
    'branch',
    'api_key',
    'ssl_cert_path',
    'ssl_cert_password',
    'url_base',
    'instance_name',
    'application_url',
    'update_automatically',
    'update_mechanism',
    'update_script_path',
    'proxy_enabled',
    'proxy_type',
    'proxy_hostname',
    'proxy_port',
    'proxy_username',
    'proxy_password',
    'proxy_bypass_filter',
    'proxy_bypass_local_addresses',
    'certificate_validation',
    'backup_folder',
    'backup_interval',
    'backup_retention',
]

SECRETS = ['password', 'password_confirmation', 'api_key', 'ssl_cert_password', 'proxy_password']


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        bind_address=dict(type='str'),
        port=dict(type='int'),
        ssl_port=dict(type='int'),
        enable_ssl=dict(type='bool'),
        launch_browser=dict(type='bool'),
        authentication_method=dict(type='str', choices=["none", "basic", "forms", "external"]),
        authentication_required=dict(type='str', choices=["enabled", "disabledForLocalAddresses"]),
        analytics_enabled=dict(type='bool'),
        username=dict(type='str'),
        password=dict(type='str', no_log=True),
        password_confirmation=dict(type='str', no_log=True),
        log_level=dict(type='str'),
        log_size_limit=dict(type='int'),
        console_log_level=dict(type='str'),
        branch=dict(type='str'),
        api_key=dict(type='str', no_log=True),
        ssl_cert_path=dict(type='str'),
        ssl_cert_password=dict(type='str', no_log=True),
        url_base=dict(type='str'),
        instance_name=dict(type='str'),
        application_url=dict(type='str'),
        update_automatically=dict(type='bool'),
        update_mechanism=dict(type='str', choices=["builtIn", "script", "external", "apt", "docker"]),
        update_script_path=dict(type='str'),
        proxy_enabled=dict(type='bool'),
        proxy_type=dict(type='str', choices=["http", "socks4", "socks5"]),
        proxy_hostname=dict(type='str'),
        proxy_port=dict(type='int'),
        proxy_username=dict(type='str'),
        proxy_password=dict(type='str', no_log=True),
        proxy_bypass_filter=dict(type='str', no_log=False),
        proxy_bypass_local_addresses=dict(type='bool'),
        certificate_validation=dict(type='str', choices=["enabled", "disabledForLocalAddresses", "disabled"]),
        backup_folder=dict(type='str'),
        backup_interval=dict(type='int'),
        backup_retention=dict(type='int'),
    )


def read_host_config(result):
    try:
        return helper.get()
    except radarr.ApiException as e:
        module.fail_json('Error getting host config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting host config: {}'.format(to_native(e)), **result)


def update_host_config(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = helper.update(want)
        except radarr.ApiException as e:
            module.fail_json('Error updating host config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating host config: {}'.format(to_native(e)), **result)
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
    helper = RadarrConfigHelper(module.api, '/api/v3/config/host', SECRETS)
    result = dict(
        changed=False,
        id=0,
    )

    # Get resource.
    state = read_host_config(result)
    result.update(helper.view(state))

    # Overlay only the options passed on the current resource.
    want, changed = helper.merge(state, module.params, OPTIONS)

    # Update an existing resource.
    if changed:
        update_host_config(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
