from jnpr.junos import Device
from lxml import etree

from inventory import routers

for each in routers:
    dev = Device(
        host=f"192.168.110.{each['id']}",
        user="root",
        password="juniper123",
        gather_facts=False,
    )
    dev.open()

    formats = ["text", "set"]

    for each_format in formats:
        configuration = dev.rpc.get_config(options={"format": each_format})
        f = open(f"../junos/downloaded/{each['device']}_{each_format}.conf", "w")
        f.write(etree.tostring(configuration).decode("utf-8"))

    f.close()

    print(f"downloaded: {each['device']}")
