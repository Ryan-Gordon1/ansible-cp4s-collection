
# Copyright: (c) 2021, Ryan Gordon
# The MIT License
#  
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule


__metaclass__ = type

DOCUMENTATION = r'''
---
module: cp4s_query_incidents

short_description: A Module used to query Cases/Incidents in CP4S or Resilient

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This module is an example of how you can choose to use a module or a role to achieve a similar outcome. An almost identical piece of functionality exists in the CP4S role but this gives a programmatic way to do it.

options:
    conditions:
        description:
            - list of conditions to query
            - [field, value, method] if querying one field
            - [ [field, value, method], [field, value, method] ] if multiple field query is desired
        required: true
        type: list
    method:
        description: set global method for conditions
        required: false
        type: string
    plan_status:
        description: pass "C" to query closed incidents
        required: false
        type: string
    multiple_fields:
        description: "true"/"True"/etc. to perform multifield query.
        required: false
        type: string
    fail:
        description: provide any value to fail the module
        required: false
        type: string
    

author:
    - Brian Reid (@breid1313)
'''

#TODO
EXAMPLES = r'''
# Query open incidents by name, non-exact match
- name: Test query on CP4S cases
  ryan_gordon1.cloud_pak_for_security.cp4s_query_incidents:
    conditions: ["name", "example_name", "contains"]

# Query open incidents by name, exact match
- name: Test query on CP4S cases
  ryan_gordon1.cloud_pak_for_security.cp4s_query_incidents:
    conditions: ["name", "example_name", "equals"]

# Query closed incidents by name
- name: Test query on CP4S cases
  ryan_gordon1.cloud_pak_for_security.cp4s_query_incidents:
    conditions: ["name", "example_name", "equals"]
    plan_status: "C"

# Query open incidents on multiple fields
- name: Test query on CP4S cases
  ryan_gordon1.cloud_pak_for_security.cp4s_query_incidents:
    conditions: [
                    ["name", "example_name", "equals"],
                    ["name2", "example_name2", "contains"]
                ]
    multiple_fields: "true"

# Query open incidents on multiple fields with global method condition
- name: Test query on CP4S cases
  ryan_gordon1.cloud_pak_for_security.cp4s_query_incidents:
    conditions: [
                    ["name", "example_name"],
                    ["name2", "example_name2"]
                ]
    method: "equals"
    multiple_fields: "true"


# fail the module (pass anything to fail param)
- name: Test failure of the module
  ryan_gordon1.cloud_pak_for_security.cp4s_query_incidents:
    fail: fail me
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
        conditions=dict(type='list', required=True),
        method=dict(type='str', required=False, default=None),
        plan_status=dict(type='str', required=False, default="A"),
        multiple_fields=dict(type='str', required=False, default=False),
        fail=dict(type="str", required=False, default="")
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

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params["fail"]:
        module.fail_json(msg='You requested this to fail', **result)

    # cast string to bool for multiple_fields param
    module.params["mulitple_fields"] = False if module.params.get("mulitple_fields", "false").lower() == "false" else True

    module.params["plan_status"] = module.params.get("plan_status", "A").upper()

    # TODO: Review if we can make the exception less bare, or if we can use a conditional for the changed property instead
    try:  # Try to make the API call
        response = query_incident(
            module.params["conditions"],
            method=module.params.get("method", None),
            plan_status=module.params.get("plan_status", "A"),
            mulitple_fields=module.params.get("multiple_fields", False)
        )
        result.update({"response": response})
    except Exception as e:  # we need to except in order to do else; use bare except and just raise the exception as normal
        # raise  # raises the exact error that would have otherwise been raised.
        module.fail_json(msg=u'An exception occurred when querying cases : {}'.format(e), **result)
    else:  # if no expections are raised we can assume the API call is successful and has changed state
        result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def query_incident(conditions: list, method=None, plan_status="A", mulitple_fields=False):
    """
    Queries incidents in Resilient/CP4S

    :param condition_list: list of conditions as [field_name, field_value, method] or a list of list conditions if multiple_fields==True
    :param method: set all field conditions to this method (save user from typing it for each field)
    :param plan_status: "A" == Active, "C" == Closed
    :param multiple_fields: query more than one field
    """

    def buildConditionDict(conditions, method=method):
        return {
            'field_name': conditions[0],
            'value': conditions[1],
            "method": method if method else conditions[2],
        }
    
    conditionList = []
    query_uri = u"/incidents/query?return_level=normal"

    if not mulitple_fields:
        conditions.append(buildConditionDict(conditions))
        query_uri += u"&field_handle={}".format(conditions[0])
    else:
        for condition in conditions:
            conditions.append(buildConditionDict(condition))
            query_uri += u"&field_handle={}".format(condition[0])

    conditionList.append({
                    'field_name': 'plan_status',
                    'method': 'equals',
                    'value': plan_status
                })

    query = {
        'filters': [{
            'conditions': conditionList
        }],
        "sorts": [{
            "field_name": "create_date",
            "type": "desc"
        }]
    }

    client = create_authenticated_client()

    return client.post(query_uri, query)


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
