import json
import os
import subprocess
import xml.etree.ElementTree as ET

DICT = 1
TEXT = 2


def get_known_macs():
    try:
        with open("addrs.json") as jfile:
            addrs = json.load(jfile)
            return addrs
    except FileNotFoundError:
        return {}


def scan(cached=False, format=DICT):
    known_macs = get_known_macs()
    if not cached:
        subprocess.check_output("sudo nmap -sn -oX tmp.xml  192.168.2.0/24", shell=True)
    response = ET.parse("tmp.xml")
    hosts = [child for child in response.getroot() if child.tag == "host"]
    results = []
    for tags in hosts:
        result = {}
        for tag in tags:
            if tag.tag == "address" and tag.get("addrtype") == "ipv4":
                result["ip4"] = tag.get("addr")
            if tag.tag == "address" and tag.get("addrtype") == "mac":
                mac_addr = tag.get("addr")
                if mac_addr in known_macs:
                    result["mac"] = f"{known_macs[mac_addr]}"
                else:
                    result["mac"] = f"{mac_addr} {tag.get('vendor')}"
        results.append(result)
    if format == DICT:
        return results
    if format == TEXT:
        result_text = ""
        for result in results:
            for _, item in result.items():
                result_text += item + " "
            result_text += "\n"
        return result_text
    if not cached:
        os.remove("tmp.xml")


print(scan(cached=True, format=TEXT))