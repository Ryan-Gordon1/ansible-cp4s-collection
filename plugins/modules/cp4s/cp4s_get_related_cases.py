
# Copyright: (c) 2021, Dara Meaney
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
module: cp4s_get_related_cases

short_description: A Module used to return a list of related Incident/Cases in CP4S or Resilient

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This module is an example of how you can choose to use a module or a role to achieve a similar outcome. An almost identical piece of functionality exists in the CP4S role but this gives a programmatic way to do it.

author:
    - Dara Meaney
'''

def run_module():
    # define available arguments/parameters a user can pass to the module
    # ansible module_args cannot accept a dict for custom modules so use a json str for input
    module_args = dict(
        incidentId=dict(type='str', required=True)
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
    if module.params['incidentId'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # TODO: Review if we can make the exception less bare, or if we can use a conditional for the changed property instead
    try:  # Try to make the API call
        incident = get_related_cases(incident_id=module.params.get(
            'incidentId', {}))
        result.update({"case": incident})
    except Exception as e:  # we need to except in order to do else; use bare except and just raise the exception as normal
        # raise  # raises the exact error that would have otherwise been raised.
        module.fail_json(msg=u'An exception occurred when creating the case: {}'.format(e), **result)
    else:  # if no expections are raised we can assume the API call is successful and has changed state
        result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def get_related_cases(incident_id: str):
    """get_related_cases is a helper function which
    will get a handle on an instance of the REST API client.

    :param incident_id: The incident/case id used when making the request
    :type incident_id: str
    :return: A list of the related Incident/Cases; no exceptions are handled here. If a 4XX code is returned for Auth or something else, this will fail
    :rtype: dict (IncidentDTO)
    """
    client = create_authenticated_client()

    return client.get("/incidents/{}/related_ex".format(incident_id))


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
