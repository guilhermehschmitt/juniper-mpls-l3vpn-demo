from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import yaml

from inventory import routers

for each in routers:
    dev = Device(
        host=f"192.168.110.{each['id']}",
        user="root",
        password="juniper123",
        gather_facts=False,
    )
    dev.open()

    data = yaml.load(open(f"vars/{each['device']}.yaml"))

    cu = Config(dev)

    cu.load(template_path="protocol_temp.j2", template_vars=data, format="text")
    cu.pdiff()
    if cu.commit_check():
        cu.commit()
    else:
        cu.rollback()

    dev.close()
