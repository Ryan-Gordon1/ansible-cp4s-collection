# Ansible Collection - ibm.cloud_pak_for_security
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)



A collection which exposes and interfaces with the Cloud Pak for Security (CP4S) Cases Rest API. The collection provides you the ability to perform API calls to make changes to the system through either the Ansible Role or Ansible Module paradigms.
This approach gives you a choice in how you interface with your cloud pak instance.

> Its your choice.
> -- Marco Pierre White

Are you a business focused user? The roles are the most heavy in ansible language rather than code.

Are you a technical user? The modules provide the most flexibility for accessing the REST API. 



If you have a use case you think would be good as a part of an Ansible Collection, submit a PR. The hope is to build up this collection over time and speed up our go-to-market on the CP4S and Ansible story by creating a suite of use cases all achievable through automation and powered by Ansible.

Requirements
------------
All the content in this collection works entirely with either the Cloud Pak for Security Cases API or the Resilient On-Prem Rest API. 
Certain values are needed in order to make calls such as usernames, passwords and api keys. For security, it is advised to keep these values in a Ansible Vault if you plan to use these roles. 

## Modules 
#### Available modules 
+ get_open_cases
+ get_related_cases
+ privacy_data_types
+ privacy_regulator_types
+ query_cases
+ create_artifact
+ create_case
+ close_case
+ create_note
+ delete_case
+ trigger_action (or a playbook)



## Role
The role in this repo is a git submodule of another repo located [here](https://github.ibm.com/Ryan-Gordon1/ansible-cp4s-role/).
That repo is published independently on Ansible Galaxy you can find this [here](https://galaxy.ansible.com/ryan_gordon1/cp4s)


License
-------

MIT

Author Information
------------------

This collection was developed by Brian Reid, Dara Meaney and Ryan Gordon @ IBM Security. See this link for our [community forum](http://ibm.biz/resilientcommunity). Please raise a github issue with problems.

This repository was started and incubated in this repo before we added it to the IBM Org: https://github.com/Ryan-Gordon1/ansible-cp4s-collection