Post-BootCheck

EEM and Python Scripts for NXOS(NX5600) automation including:

    Post-BootCheck - EEM script that triggers after system boot (syslog "vdc 1 has come online" message).  It calls igmp-snoopcheck.py, but the actions can be modified to suit your application.
    igmp-snoopcheck.py - written to address CSCvc90289 where igmp snooping is randomly enabled on VNI VLANs.  This shut/no shuts interface NVE1 if igmp snooping is enabled on any VNI vlans.
    

