#!/usr/bin/env python3

import os,re 

configFile = '/etc/openvpn/client.conf'

piaConnections = {
	"chicago":['us-chicago.privacy.network','chicago.conf'],
	"atlanta":['us-atlanta.privacy.network','atlanta.conf']
}
def killRestart():
	os.system('sudo killall openvpn')
	os.system('sudo service openvpn start')
def getLatency(ip):
	ret = os.popen('ping -c 1 '+ip).read()
	sStr = r"time=(.+) ms" 
	ret = re.findall(sStr,str(ret))
	return str(ret)

def loop():
	low = [0,0]
	for each in piaConnections:
		currentServer = piaConnections[each][0]
		cur = getLatency(currentServer)
		print(cur)

def overWrite vpn(newServer):
	sStr = r'remote (.+) 1198'
	with open(configFile, 'r+') as myfile:
		y = myfile.read()
		currentServer = re.findall(sStr,y)[0]
		y = re.sub(sStr, 'remote '+newServer+' 1198', y)
		myfile.seek(0)
		myfile.write(y)
		myfile.truncate()

tester(piaConnections['chicago'][0])
killRestart()
ip = '192.168.1.1'

#res = getLatency(ip)
#loop()
#print(res)
