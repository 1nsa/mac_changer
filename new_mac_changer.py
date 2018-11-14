#!/usr/bin/env python

import subprocess
import re
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address.")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address.")
    (_options, _arguments) = parser.parse_args()
    if not _options.interface:
        parser.error("Please specify an interface, use --help for more info.")
    if not _options.new_mac:
        parser.error("Please specify a MAC address, use --help for more info.")
    return _options


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read current MAC address.")


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


# Start
options = get_arguments()

# Print current mac
current_mac = get_current_mac(options.interface)
print("* Current MAC is " + str(current_mac) + " *")

# Change mac
change_mac(options.interface, options.new_mac)

# Check if mac changed
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Mac address changed successfully.")
    print("* Current MAC is " + str(current_mac) + " *")
else:
    print("[+] Mac is changed successfully.")
    print("* Current MAC is " + str(current_mac) + " *")
