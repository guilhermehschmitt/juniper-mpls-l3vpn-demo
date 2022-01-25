"""Pushes a device's bootstrap configuration in an overwrite method."""
from inventory import routers
from jnpr.junos import Device  # type: ignore
from jnpr.junos.utils.config import Config  # type: ignore

for each in routers:
    dev = Device(
        host=f"192.168.110.{each['id']}",
        user="automation",
        password="juniper123",  # nosec
        gather_facts=False,
    )
    dev.open()

    print(f"connected to {each['device']}")  # noqa T001

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
