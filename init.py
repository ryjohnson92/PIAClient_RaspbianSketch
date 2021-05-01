#!/usr/bin/env python3

import os,re,sys,time
defaultMsgTime =1.75
logfile = './log.txt'

preReqs = {
	'openvpn':{
		"config": '/etc/',
		"default": './defaults/openvpn.default'
	},
	'iptables':{
		"config":'/etc/',
		"clearCommands":'./data/iptables/iptables.clearcommands',
		"openVPNrouting":'./data/iptables/iptables.openvpnroute'
	},
	'isc-dhcp-server':{
		"config":"/etc/"
	}
}

def run():
	if not os.geteuid()==0:
    		sys.exit('This script must be run as root!')
	checkPrereqs()
	openVPNrouting()
	pass

### Proccess the default settings for open vpn connections
### The commands listed are set to route to tun0 from eth1 
### this can be changed via the ****
def openVPNrouting():
	iptablesConfig = preReqs['iptables']
	runCommands(iptablesConfig['clearCommands'],'iptables prexisting settings cleared removed...')
	runCommands(iptablesConfig['openVPNrouting'],'iptables has been set to openvpn routing')
### Runs a list of provided commands
### This function auto runs these commands as sudo as that is already required to run the script 
###
def runCommands(commandsList,note='command list executed'):
	clearScreen()
	with open(commandsList) as f:
		lines = f.readlines()
		for l in lines:
			os.system('sudo '+l+ " > "+logfile)
		print(note)
		time.sleep(defaultMsgTime)

#### Clears out existing rules in IP tables so that the correct commands can be entered
def clearIpTables():
	clearScreen()
	with open(preReqs['iptables']['clearCommands']) as f:
		lines = f.readlines()
		for l in lines:
			os.system('sudo '+l+ " > "+logfile)
	print('iptables prexisting settings cleared removed...')

### Loops Prereqs and checks for pressence, or installs as required. 
### NOTE:::
### Additional setup may still be required at this time to make the router functional if prereq needs installins
def checkPrereqs():
	clearScreen()
	print('Testing prereqs')
	for each in preReqs:
		status = installProgram(each)
		if not status:
			sys.exit('Prereq '+each+" is not installed, please install and re-attempt setup process")
	clearScreen()
	print('all prereqs accounted for, continuing to setup')

### Does a version check on prereq and determines if it is installed on the system.
def installProgram(program):
	output = os.popen('sudo apt-get install '+program+' -y').read()
	mStr=r'is already the newest version'
	x = re.findall(mStr,output)
	if len(x) > 0:
		return True
	return False

	#print(output)

def clearScreen():
	os.system('clear')



run()

