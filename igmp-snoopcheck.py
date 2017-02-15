#!/bin/env python
import re
import cisco


def get_igmp_status(cli_output):
    """ takes str output from 'show ip igmp snooping | include "IGMP Snooping" n 1' command
        and returns a dictionary containing enabled/disabled state of each vlan
    """
    search_prefix = "IGMP Snooping information for vlan "
    vlan_status={}
    counter = 0
    line_list = cli_output.splitlines()
    for line in line_list:
        if line.startswith(search_prefix):
            vlan_status.update({line.strip(search_prefix):line_list[counter+1].strip('IGMP snooping ')})
        counter += 1
    return vlan_status


def get_vni_vlans(cli_output):
    """takes str output from 'show ip igmp snooping | include "VxLAN VNI VLANS"' command'
       and returns a list of vxlan vni vlans
    """
    # obtain list of vni vlans & vlan ranges
    vni_vlan_ranges = cli_output[19:].split(",")
    vni_vlans = []
    #convert list of vlan/vlan ranges into a list of individual vlans
    for range in vni_vlan_ranges:
        dash_loc = range.find("-")
        if dash_loc != -1:
            first_vlan = range[:dash_loc]
            last_vlan = range[dash_loc +1 :]
            counter = int(first_vlan)
            while counter <= int(last_vlan):
                vni_vlans.append(str(counter))
                counter += 1
        else:
            vni_vlans.append(range)

    return vni_vlans


def igmp_snoop_check(vni_vlans, vlan_status):
    """checks the igmp status of each vni vlan and resets interface NVE1 if igmp snooping is enabled on any of them"""
    for vlan in vni_vlans:
        if vlan_status[vlan] == "enabled":
            cli('configure terminal')
            cli('interface nve1')
            cli('shutdown')
            cli('no shutdown')
            command = str("event manager environment igmpCheckMsg IGMP snooping was enabled on VNI VLAN" + vlan + ".  igmp_snoopcheck.py reset interface NVE1")
            cli(command)
            cli('end')
            return
    cli('configure terminal')
    cli('event manager environment igmpCheckMsg IGMP snooping was correctly disabled on all VNI VLANs.  igmp_snoopcheck.py took no action')
    cli('end')
    return


def main():
    # Get list of vni vlans
    vni_vlans = get_vni_vlans(cli('show ip igmp snooping | include "VxLAN VNI VLANS" n 1'))


    # Create dictionary of all vlan igmp snooping status (enabled/disabled)
    vlan_status = get_igmp_status(cli('show ip igmp snooping | include "IGMP Snooping" n 1'))


    # Reset NVE 1 if igmp enabled on any vni vlans.  Create EEM env variable w/ status msg.
    igmp_snoop_check(vni_vlans, vlan_status)
    return


if __name__ == "__main__":
    main()
