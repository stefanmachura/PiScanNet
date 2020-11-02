import os
import subprocess
import xml.etree.ElementTree as ET

subprocess.check_output("sudo nmap -sn -oX a.xml  192.168.2.0/24", shell=True)


response = ET.parse("a.xml")

root = response.getroot()

hosts = [child for child in root if child.tag ==  "host"]

results = []

for tags in hosts:
	result = {}
	for tag in tags:
		if tag.tag == "status":
			if tag.get("reason") == "localhost-response":
				result["comment"] = "(It's me)!"
			else:
				result["comment"] = ""
		if tag.tag == "address" and tag.get("addrtype") == "ipv4":
			result["ip4"] = tag.get("addr")
		if tag.tag == "address" and tag.get("addrtype") == "mac":
			result["mac"] = f"{tag.get('addr')} {tag.get('vendor')}"
	results.append(result)

for result in results:
	print(result)


os.remove("a.xml")
