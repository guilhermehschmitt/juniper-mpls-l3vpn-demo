#!/usr/bin/bash

sshpass -p "juniper123" scp ../junos/downloaded/pe1.conf automation@192.168.110.11:/var/tmp/
sshpass -p "juniper123" scp ../junos/downloaded/p1.conf automation@192.168.110.12:/var/tmp/
sshpass -p "juniper123" scp ../junos/downloaded/pe2.conf automation@192.168.110.13:/var/tmp/
sshpass -p "juniper123" scp ../junos/downloaded/pe3.conf automation@192.168.110.14:/var/tmp/
sshpass -p "juniper123" scp ../junos/downloaded/p2.conf automation@192.168.110.15:/var/tmp/
sshpass -p "juniper123" scp ../junos/downloaded/pe4.conf automation@192.168.110.16:/var/tmp/
sshpass -p "juniper123" scp ../junos/downloaded/ce2.conf automation@192.168.110.17:/var/tmp/
sshpass -p "juniper123" scp ../junos/downloaded/ce1.conf automation@192.168.110.18:/var/tmp/
