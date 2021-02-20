
#todo:
# Add ipv6 (have interfaces passed in) to construct the dhcp
from __future__ import absolute_import, division, print_function
__metaclass__ = type
import re
from ansible.module_utils.network.pfsense.module_base import PFSenseModuleBase
from ansible.module_utils.network.pfsense.rule import PFSenseRuleModule
from ansible.module_utils.compat.ipaddress import ip_network

DHCP_ARGUMENT_SPEC = dict(
    state=dict(default='present', choices=['present', 'absent']),
    interface=dict(required=True, type='str'),
    enable=dict(required=False, type='bool'),
    range_from=dict(required=True, type='str'),
    range_to=dict(required=True, type='str'),
)

class PFSenseDhcpModule(PFSenseModuleBase):
    """ module managing pfsense dhcp server """

    @staticmethod
    def get_argument_spec():
        """ return argument spec """
        return DHCP_ARGUMENT_SPEC

    ##############################
    # init
    #
    def __init__(self, module, pfsense=None):
        super(PFSenseDhcpModule, self).__init__(module, pfsense)
        self.name = "pfsense_dhcp"
        self.obj = dict()

        self.root_elt = self.pfsense.dhcpd
        if self.root_elt is None:
            self.module.fail_json(msg='Unable to find dhcpd XML configuration entry. Are you sure we are alive ?')

        
    ##############################
    # params processing
    #
    def _params_to_obj(self):
        """ return an dhcpd dict from module params """
        params = self.params

        obj = dict()
        self.obj = obj
        
        #interface lookup
        obj['if'] = params['interface']
        self.target_elt = self.root_elt.get_element(obj['if'])
        
        if self.target_elt is None:
            self.module.fail_json(msg='Unable to locate target element >'+obj['if']+'<')

        #load if we are enabling/present
        self._get_ansible_param_bool(obj, 'enable', value = '')
        if params['state'] == 'present':    
            self._get_ansible_param(obj, 'range_from', fname='from')
            self._get_ansible_param(obj, 'range_to',fname='to')

    #
    def _create_target(self):
        """ create the XML target_elt """
        server_elt = self.pfsense.new_element('item')
        return server_elt

