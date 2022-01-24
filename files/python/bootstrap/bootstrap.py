import yaml
from inventory import routers
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

for each in routers:
    dev = Device(
        host=f"192.168.110.{each['id']}",
        user="automation",
        password="juniper123",
        gather_facts=False,
    )
    dev.open()

    print(f"connected to {each['device']}")

    cu = Config(dev)
    cu.load(
        path=f"./configurations/downloaded/text/{each['device']}.conf",
        overwrite=True,
    )
    cu.pdiff()

    if cu.commit_check():
        cu.commit()
    else:
        cu.rollback()

    dev.close()
