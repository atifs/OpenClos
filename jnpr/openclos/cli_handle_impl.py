#------------------------------------------------------------------------------
#                             cli_handle_impl.py
#------------------------------------------------------------------------------
'''
@author : rgiyer
Date    : October 20th, 2014

This module implements all "handle" and "macro" specified in cliCommands.yaml.
Command context from the openclos CLI will invoke one or more functions (or handles) implemented in this module

'''

# Standard python libraries
import os

# Python frameworks required for openclos
import yaml

# openclos classes
import util
from l3Clos import L3ClosMediation
from model import Pod
from ztp import ZtpServer
import dao
import rest


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class CLIImplementor:

    def show_pods ( self, *args ):
        ret_list = []
        pods_yaml_file = os.path.join ( util.configLocation,
                                        'closTemplate.yaml' )
        pods_file_stream = open ( pods_yaml_file, 'r' )
        pods_template = yaml.load ( pods_file_stream )
        pods_definition = {}
        if ( pods_template.has_key ( "pods" ) ):
            pods_definition = pods_template [ "pods" ]
            for pods in pods_definition:
                ret_list.append ( pods )

        return ret_list

#------------------------------------------------------------------------------
    def handle_create_cabling_plan ( self, pod_name ):
        l3ClosMediation = L3ClosMediation ()
        pod_objects = l3ClosMediation.dao.getAll ( Pod )
        for pod in pod_objects:
            if ( pod.name == pod_name ):
                l3ClosMediation.createCablingPlan ( pod.id )
                return None

        # No Pods found
        pods = l3ClosMediation.loadClosDefinition()
        new_pod = l3ClosMediation.createPod ( pod_name,
                                              pods [ pod_name ] )
        l3ClosMediation.createCablingPlan ( new_pod.id )
        

#------------------------------------------------------------------------------
    def handle_create_device_config ( self, pod_name ):
        l3ClosMediation = L3ClosMediation ()
        pod_objects = l3ClosMediation.dao.getAll ( Pod )
        for pod in pod_objects:
            if ( pod.name == pod_name ):
                l3ClosMediation.createDeviceConfig ( pod.id )
                return None

        # No Pods found
        pods = l3ClosMediation.loadClosDefinition()
        new_pod = l3ClosMediation.createPod ( pod_name,
                                              pods [ pod_name ] )
        l3ClosMediation.createDeviceConfig ( new_pod.id )

#------------------------------------------------------------------------------
    def handle_create_ztp_config ( self, pod_name ):
        ztpServer = ZtpServer()
        ztpServer.createPodSpecificDhcpConfFile ( pod_name )
        installedDhcpConf = "/etc/dhcp/dhcpd.conf"
        generatedDhcpConf = "/home/regress/OpenClos-R1.0.dev1/jnpr/openclos/out/anotherPod/dhcpd.conf"

        if util.isPlatformUbuntu():
            os.system('sudo apt-get -y install isc-dhcp-server')
            os.system('sudo cp ' + generatedDhcpConf + ' ' + installedDhcpConf)
            os.system("/etc/init.d/isc-dhcp-server restart")

        elif util.isPlatformCentos():
            os.system('yum -y install dhcp')
            os.system('sudo cp ' + generatedDhcpConf + ' ' + installedDhcpConf)
            os.system("/etc/rc.d/init.d/dhcpd restart")

#------------------------------------------------------------------------------
    def handle_update_password ( self, *args ):
        print "TODO: handle_update_password"

#------------------------------------------------------------------------------
    def handle_run_reports ( self, *args ):
        print "TODO: handle_run_reports"

#------------------------------------------------------------------------------
    def handle_run_rest_server ( self, *args ):
        print "TODO: handle_run_rest_server"

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
