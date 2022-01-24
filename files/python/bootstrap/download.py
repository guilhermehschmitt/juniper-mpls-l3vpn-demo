from jnpr.junos import Device
from lxml import etree

from inventory import routers

CONFIG_PATH = "./configurations"

for each in routers:
    dev = Device(
        host=f"192.168.110.{each['id']}",
        user="automation",
        password="juniper123",
        gather_facts=False,
    )
    dev.open()

    formats = ["text", "set"]

    for each_format in formats:
        configuration = dev.rpc.get_config(options={"format": each_format})
        local_file = open(
            f"{CONFIG_PATH}/downloaded/{each_format}/{each['device']}.conf",
            "w",
        )
        local_file.write(etree.tostring(configuration).decode("utf-8"))
        local_file.close()

    print(f"downloaded: {each['device']}")