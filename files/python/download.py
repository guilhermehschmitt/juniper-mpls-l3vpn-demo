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

    configuration = dev.rpc.get_config(options={"format": "text"})

    f = open(f"../junos/downloaded/{each['device']}.conf", "w")
    f.write(etree.tostring(configuration).decode("utf-8"))
    f.close()

    print(f"downloaded: {each['device']}")
