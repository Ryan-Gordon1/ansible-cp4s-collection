
# Copyright: (c) 2021, Ryan Gordon
# The MIT License
#  
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule

# Additional import of common code
# from cp4s_common import create_authenticated_client

__metaclass__ = type

DOCUMENTATION = r'''
---
module: cp4s_trigger_action

short_description: A Module used to trigger an Action on a CP4S Case

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This module is an example of how you can choose to use a module or a role to achieve a similar outcome. An almost identical piece of functionality exists in the CP4S role but this gives a programmatic way to do it.

options:
    case_id:
        description: This is the ID number of the Case to be closed.
        required: true
        type: int
    action_id:
        description: This is the ID number of the Action to be invoked.
        required: true
        type: int

author:
    - Ryan Gordon (@Ryan-Gordon)
'''

EXAMPLES = r'''
# Invoke the action with ID 42 on the Case with ID 2095
- name: Test creation of a Case with a name
  ryan_gordon1.cloud_pak_for_security.cp4s_trigger_action:
    case_id: 2095
    action_id: 42

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


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        case_id=dict(type='int', required=True),
        rule_id=dict(type='int', required=False, default=False)
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

    # TODO: Review if we can make the exception less bare, or if we can use a conditional for the changed property instead
    try:  # Try to make the API call
        response = trigger_rule(case_id=module.params.get(
            'case_id', 0), rule_id=module.params.get('rule_id', 0))

        # Add the response to the result to return
        result.update({"rule_trigger_result": response})

    except Exception as e:  # we need to except in order to do else; use bare except and just raise the exception as normal
        # raise  # raises the exact error that would have otherwise been raised.
        module.fail_json(msg=u'An exception occurred when triggering the action on Case {}: {}'.format(
            module.params['case_id'], e), **result)
    else:  # if no expections are raised we can assume the API call is successful and has changed state
        result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def trigger_rule(case_id: int, rule_id: int):
    client = create_authenticated_client()
    # This API is NOT SUPPORTED at the time of this modules development. You can see it using chrome dev tools.
    return client.post("/incidents/{case_id}/action_invocations".format(case_id), {"action_id": rule_id, "properties": {"job_status": [], "last_updated": 152}})


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
