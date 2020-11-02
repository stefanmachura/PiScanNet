with open("x.xml") as xfile:
	devices = xfile.readlines()[1:-1] 
	
for device in devices:
	host, status = device.rstrip("\n").split("\t")
	host = host.split(": ")[1]
	status = status.split(": ")[1]
	print(f"device {host} is {status}")

