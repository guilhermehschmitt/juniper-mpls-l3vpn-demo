"""Build and push our bootstrap config with PyEZ."""
import yaml  # type: ignore
from inventory import routers
from jnpr.junos import Device  # type: ignore
from jnpr.junos.utils.config import Config  # type: ignore


def main():
    """Build connection, template config, and push to device.

    Loop over our list of routers that we imported from inventory.py
    Utilize the ID as the last octet within the IP address of the router
    Once the connection is open, print a message to the console
    Ingest the configuration variables stored in our device's' YAML file
    """
    for each in routers:
        dev = Device(
            host=f"192.168.110.{each['id']}",
            user="automation",
            password="juniper123",
            gather_facts=False,
        )
        dev.open()

        print(f"connected to {each['device']}")  # noqa T001

        # creating an empty dictionary called `data`
        # then stuffing our YAML vars into it as 'configuration'
        # this is to help handle PyEZ loading YAML vars differently than Jinja2
        data = dict()
        data["configuration"] = yaml.safe_load(open(f"./{each['device']}.yaml"))

        cu = Config(dev)

        cu.load(
            template_path="../templates/junos.j2",
            template_vars=data,
            format="set",
        )
        cu.pdiff()
        if cu.commit_check():
            cu.commit()
        else:
            cu.rollback()

        dev.close()


if __name__ == "__main__":
    main()
