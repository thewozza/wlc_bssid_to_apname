import csv
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException,NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
import time
import sys


# these are just simple python formatted files with variables in them
# the WLC IP and credentials are in here
from credentials import *

# first we want to grab all the APs that the WLC knows about

wlc = {
		'device_type': 'cisco_wlc',
		'ip': controller,
		'username': controller_u,
		'password': controller_p,
		'port' : 22,          # optional, defaults to 22
		'secret': secret,     # optional, defaults to ''
		'verbose': False,       # optional, defaults to False
	}

wlc_connect = ConnectHandler(**wlc)

ap_summary = wlc_connect.send_command('show ap summary').split("\n")

summary_start = 0
ap_on_wlc = []

# we put the APs into a list of dictionaries for easy reference later
for ap_summary_output in ap_summary:
	if "-" in ap_summary_output:
		summary_start = 1
	elif summary_start == 0:
		continue
	if len(ap_summary_output.split()) <= 0:
		continue
	ap_on_wlc.append(ap_summary_output.split()[0])
	
for access_point in ap_on_wlc:
	if "------------------" in access_point:
		continue
	
	command = 'show ap wlan 802.11-abgn ' + access_point
	ap_wlan = wlc_connect.send_command(command).split("\n")
	
	print access_point,
	
	wlans_next = 0
	for ap_wlan_line in ap_wlan:
		if "-------" in ap_wlan_line:
			wlans_next = 1
			continue
		elif wlans_next == 0:
			continue
		if "non-routable-interface" in ap_wlan_line:
			print ap_wlan_line.split("non-routable-interface")[1].split()[0],
		#print ap_wlan_line
		if len(ap_wlan_line.split()) >= 2:
			print ap_wlan_line.split()[2],
	
	print

	
wlc_connect.disconnect()

