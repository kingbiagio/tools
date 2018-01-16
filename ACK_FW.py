#!/usr/bin/python
# Auhtor Biagio
#
# It Send TCP ACK Flag, will determine if port is Filtred or Not 
# if port is filtered we received a RST flag
# Requirements termcolor "pip install termcolor"

from termcolor import*
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from threading import *

if len(sys.argv) != 3:	
	print (colored("Usage- ./ACK_FW.py [IP] [Port]", 'yellow'))
	sys.exit()			

ip = sys.argv[1]
port = int (sys.argv[2])

#Change here for different Timeout&Verbose
ACK_response = sr1(IP(dst= ip)/TCP(dport= port, flags='A'), timeout=1, verbose=0)
SYN_response = sr1(IP(dst= ip)/TCP(dport= port, flags='S'), timeout=1, verbose=0)

print (colored("<--FIREWALL DETECTION-->",'red'))

# If ACK_response and SYN_response are NONE, the Port
# is either unstatefully filtered or Host is Down
if (ACK_response == None) and (SYN_response == None) :
	print(colored("[+]Port is either Unstatefully Filtered, or Host is Down!",'red')), [port]

#if one Response of Variable is None, Port is Filtered
elif ((ACK_response == None) or (SYN_response == None)) and not ((ACK_response == None) and (SYN_response == None)):
	print(colored("[!]Port is Filtered and Open",'red')), [port]

elif int(SYN_response[TCP].flags) == 18:#Change different flag value
	print(colored("[+]Port is Unfiltered and Open",'green')), [port]

elif int(SYN_response[TCP].flags) == 20:#Change here for different Flag value
	print(colored("[+]Port is Unfiltered and Close",'yellow')), [port]

else:   
	print(colored("[!]ERROR Unable to determine if the Port is Filtered",'red')), [port]
