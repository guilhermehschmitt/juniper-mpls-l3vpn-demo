"""Download our configurations and store locally."""
from inventory import routers  # type: ignore
from jnpr.junos import Device  # type: ignore
from lxml import etree

CONFIG_PATH = "../junos/downloaded"


def main():
    """Download configurations from devices."""
    # loop over routers from inventory
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
                f"{CONFIG_PATH}/{each['device']}.{each_format}.conf",
                "w",
            )
            local_file.write(etree.tostring(configuration).decode("utf-8"))
            local_file.close()

        print(f"downloaded: {each['device']}")  # noqa T001


if __name__ == "__main__":
    main()
