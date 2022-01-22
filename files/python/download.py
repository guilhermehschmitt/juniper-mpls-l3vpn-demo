from jnpr.junos import Device
from lxml import etree

inventory = [
    {"id": "11", "device": "houston"},
    {"id": "12", "device": "dallas"},
    {"id": "13", "device": "amarillo"},
    {"id": "14", "device": "sanantonio"},
    {"id": "15", "device": "austin"},
    {"id": "16", "device": "fortworth"},
    {"id": "17", "device": "elpaso"},
    {"id": "18", "device": "galveston"},
]

for each in inventory:
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
