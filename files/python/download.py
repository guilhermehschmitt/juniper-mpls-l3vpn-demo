"""Download our configurations and store locally."""
import yaml  # type: ignore
from jnpr.junos import Device  # type: ignore
from lxml import etree

CONFIG_PATH = "../junos/downloaded"


def inventory():
    """Load our inventory.yaml into a python object called routers."""
    routers = yaml.safe_load(open("inventory.yaml"))
    print(routers)
    return routers


def main(routers):
    """Download configurations from devices."""
    # loop over routers from inventory
    for each in routers:
        dev = Device(
            host=f"{each['ip']}",
            user="jcluser",
            password="Juniper!1",
            gather_facts=False,
        )
        dev.open()

        formats = ["text", "set"]

        for each_format in formats:
            configuration = dev.rpc.get_config(options={"format": each_format})
            local_file = open(
                f"{CONFIG_PATH}/{each['name']}.{each_format}.conf",
                "w",
            )
            local_file.write(etree.tostring(configuration).decode("utf-8"))
            local_file.close()

        print(f"downloaded: {each['name']}")  # noqa T001


if __name__ == "__main__":
    """Main script execution.

    We will first load our inventory.yaml file into a new Python object `routers`
    Our main function will run next, which will take care of the templating
    and pushing of our configurations to the remote devices.
    """
    routers = inventory()
    main(routers)
