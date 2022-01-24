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

    print(f"connected to {each['device']}")

    # creating an empty dictionary called `data`, then stuffing our YAML vars into it as 'configuration'
    # this is to help handle the fact that PyEZ loads the YAML vars differently than Jinja2
    data = dict()
    data["configuration"] = yaml.safe_load(open(f"vars/{each['device']}.yaml"))

    cu = Config(dev)

    cu.load(template_path="templates/junos.j2", template_vars=data, format="set")
    cu.pdiff()
    if cu.commit_check():
        cu.commit()
    else:
        cu.rollback()

    dev.close()
