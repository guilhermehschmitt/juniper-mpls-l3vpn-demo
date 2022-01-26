"""Pushes a device's bootstrap configuration in an overwrite method."""
import yaml  # type: ignore
from jnpr.junos import Device  # type: ignore
from jnpr.junos.utils.config import Config  # type: ignore


def inventory():
    """Load our inventory.yaml into a python object called routers."""
    routers = yaml.safe_load(open("inventory.yaml"))
    print(routers)
    return routers


def main(routers):
    """Template configuration with Jinja2 and store locally."""
    for each in routers:
        dev = Device(
            host=f"{each['ip']}",
            user="jcluser",
            password="Juniper!1",  # nosec
            gather_facts=False,
        )
        dev.open()

        print(f"connected to {each['name']}")  # noqa T001

        cu = Config(dev)
        cu.load(
            path=f"./configurations/downloaded/text/{each['name']}.conf",
            overwrite=True,
        )
        cu.pdiff()

        if cu.commit_check():
            cu.commit()
        else:
            cu.rollback()

        dev.close()


if __name__ == "__main__":
    """Main script execution.

    We will first load our inventory.yaml file into a new Python object `routers`
    Our main function will run next, which will take care of the templating
    and pushing of our configurations to the remote devices.
    """
    routers = inventory()
    main(routers)
