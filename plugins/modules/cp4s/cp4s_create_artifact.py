
# Copyright: (c) 2021, Ryan Gordon
# The MIT License
#  
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from __future__ import (absolute_import, division, print_function)

# Additional import of common code 
# from cp4s_common import create_authenticated_client

__metaclass__ = type

DOCUMENTATION = r'''
---
module: cp4s_close_incident

short_description: A Module used to create an Case in CP4S or Resilient

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This module is an example of how you can choose to use a module or a role to achieve a similar outcome. An almost identical piece of functionality exists in the CP4S role but this gives a programmatic way to do it.

options:
    type:
        description: The Type of the artifact to be created. e.g 'DNS Name'.
        required: true
        type: str
    value:
        description: The value of the artifact to be created. e.g 'www.google.com'.
        required: true
        type: str
    other:
        description:
            - Control to pass any extra information that might be needed to create an artifact.
        required: false
        type: dict

author:
    - Ryan Gordon (@Ryan-Gordon)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test closure of a Case
  ryan_gordon1.cloud_pak_for_security.cp4s_close_incident:
    type: 'DNS Name'
    value: 'google.com'

# pass in a message and have changed true
- name: Test closure of a Case
  ryan_gordon1.cloud_pak_for_security.cp4s_close_incident:
    type: 'IP Address'
    value: '9.9.9.9'

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

import resilient

from ansible.module_utils.basic import AnsibleModule
from resilient_lib import close_incident


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        type=dict(type='str', required=True),
        value=dict(type='str', required=True),
        other=dict(type='dict', required=False, default={})
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
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

    client = create_authenticated_client()
    
    # TODO: Review if we can make the exception less bare, or if we can use a conditional for the changed property instead
    try:  # Try to make the API call
        # Make an API call to the global artifacts endpoint for the org
        # Pass the provided name and value 
        # the 'other' module param is dict and is expanded to provide a way to add any other properties to the call 
        response = client.post('/artifacts', {
            'type': {
                'name': module.params['type']
            },
            'value': module.params['value'],
            **module.params['other']
        })
        # Add the response to the result to return
        result.update({"note_creation_result": response})

    except Exception as e:  # we need to except in order to do else; use bare except and just raise the exception as normal
        # raise  # raises the exact error that would have otherwise been raised.
        module.fail_json(msg=u'An exception occurred when creating an artifact: {}'.format(module.params['case_id'],e), **result)
    else:  # if no expections are raised we can assume the API call is successful and has changed state
        result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def create_authenticated_client():
    """create_authenticated_client uses the resilient package
    to gather values from a standard app.config file; the configuration file
    used for an Integration Server or App Host App.
    This means all credentials needed to run this module can be kept 
    separate and we can also avoid var prompts.
    Note: If your running this module on a host other than localhost, 
    that host needs to have an app.config file or you need to copy one over.

    :return: An authenticated rest client to CP4S or Resilient
    :rtype: SimpleClient
    """
    import resilient
    # Create Resilient API Client
    resilient_parser = resilient.ArgumentParser(
        config_file=resilient.get_config_file())
    resilient_opts = resilient_parser.parse_known_args()
    # Instantiate a client using the gathered opts
    return resilient.get_client(resilient_opts[0])


def main():
    run_module()


if __name__ == '__main__':
    main()

    

