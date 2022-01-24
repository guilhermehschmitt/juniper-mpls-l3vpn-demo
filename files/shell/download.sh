#!/usr/bin/bash

sshpass -p "juniper123" scp automation@192.168.110.11:/var/tmp/config.conf ../junos/downloaded/pe1.conf
sshpass -p "juniper123" scp automation@192.168.110.12:/var/tmp/config.conf ../junos/downloaded/p1.conf
sshpass -p "juniper123" scp automation@192.168.110.13:/var/tmp/config.conf ../junos/downloaded/pe2.conf
sshpass -p "juniper123" scp automation@192.168.110.14:/var/tmp/config.conf ../junos/downloaded/pe3.conf
sshpass -p "juniper123" scp automation@192.168.110.15:/var/tmp/config.conf ../junos/downloaded/p2.conf
sshpass -p "juniper123" scp automation@192.168.110.16:/var/tmp/config.conf ../junos/downloaded/pe4.conf
sshpass -p "juniper123" scp automation@192.168.110.17:/var/tmp/config.conf ../junos/downloaded/ce2.conf
sshpass -p "juniper123" scp automation@192.168.110.18:/var/tmp/config.conf ../junos/downloaded/ce1.conf
