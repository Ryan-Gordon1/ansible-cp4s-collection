
# Copyright: (c) 2021, Ryan Gordon
# The MIT License
#  
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from __future__ import (absolute_import, division, print_function)
from resilient_lib import close_incident
from ansible.module_utils.basic import AnsibleModule

# Additional import of common code
# from cp4s_common import create_authenticated_client

__metaclass__ = type

DOCUMENTATION = r'''
---
module: cases_privacy_data_types

short_description: A Module used to get applicable privacy data types in CP4S or Resilient

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This module is an example of how you can choose to use a module or a role to achieve a similar outcome. An almost identical piece of functionality exists in the CP4S role but this gives a programmatic way to do it.

author:
    - Ryan Gordon (@Ryan-Gordon)
'''

EXAMPLES = r'''
- name: Use DNS to get privacy details
  ryan_gordon1.cloud_pak_for_security.case_privacy_regulator_types:
    host: mydns.aws.com
    api_key_id: supersecret
    api_key_secret: evenmoresecret

- name: Use IP to get privacy details
  ryan_gordon1.cloud_pak_for_security.case_privacy_regulator_types:
    host: 9.9.9.9
    api_key_id: supersecret
    api_key_secret: evenmoresecret
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''
# TODO: Review the encapsulation of common logic in module utils
# So far i have not gotten it to work.
# When working according to the docs this statement should work
# from ansible_collections.ryan_gordon1.cloud_pak_for_security.plugins.module_utils.cp4s_common_logic import create_authenticated_client


def run_module():
    # define available arguments/parameters a user can pass to the module
    # ansible module_args cannot accept a dict for custom modules so use a json str for input
    module_args = dict(
        host=dict(type='str', required=True),
        api_key_id=dict(type='str', required=True),
        api_key_secret=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        response=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # TODO: Review if we can make the exception less bare, or if we can use a conditional for the changed property instead
    try:  # Try to make the API call
        response = execute_request_with_global_keys(
            'get', url=module.params['host'], api_key_id=module.params['api_key_id'], api_key_secret=module.params['api_key_secret'])
        result.update({"privacy_data_types": response.json()})
    except Exception as e:  # we need to except in order to do else; use bare except and just raise the exception as normal
        # raise  # raises the exact error that would have otherwise been raised.
        module.fail_json(
            msg=u'An exception occurred when creating the case: {}'.format(e), **result)
    else:  # if no expections are raised we can assume the API call is successful and has changed state
        result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


# TODO: Move to module utils
def execute_request_with_global_keys(operation, url, **kwargs):
    """execute_request_with_global_keys helper function 
    which takes a global CP4S API Key and Secret rather than one 
    derived from cases.
    These API keys use different authentication methods and
    API calls using this client will be slightly different to cases

    That being said, this client provides full access to the CP4S
    instance.
    TODO: Should we rename this
    """
    import requests
    from requests.auth import HTTPBasicAuth

    url = "https://{}/rest/privacy/{}".format(url, "data_type_categories")
    # TODO: This design could be improved
    if operation == 'get':
        return requests.get(url,
                            auth=HTTPBasicAuth(kwargs.get(
                                'api_key_id'), kwargs.get('api_key_secret')),
                            verify=kwargs.get('verify', False))
    elif operation == 'post':
        return requests.post(url,
                             auth=HTTPBasicAuth(kwargs.get(
                                 'api_key_id'), kwargs.get('api_key_secret')),
                             body=kwargs.get('body'),
                             verify=kwargs.get('verify', False))


def main():
    run_module()


if __name__ == '__main__':
    main()
