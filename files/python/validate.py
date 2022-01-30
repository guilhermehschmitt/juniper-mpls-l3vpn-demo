"""validate.py: use JSNAPy to validate the L3VPN circuit."""
from pprint import pprint

from jnpr.jsnapy import SnapAdmin

JSNAPY = SnapAdmin()

CONFIG = """
hosts:
  - device: 100.123.1.4
    username : automation
    passwd: juniper123
  - device: 100.123.1.7
    username : automation
    passwd: juniper123
tests:
  - test_check_bgp_states.yaml
"""


def main():
    """Primary function to take and validate our snapcheck."""
    snapcheck = JSNAPY.snapcheck(CONFIG, "bgp_test")

    for val in snapcheck:
        print("Tested on", val.device)
        print("Final result: ", val.result)
        print("Total passed: ", val.no_passed)
        print("Total failed:", val.no_failed)
        pprint(dict(val.test_details))


if __name__ == "__main__":
    """Main script execution.

    We will first load our inventory.yaml file into a new Python object `devices`
    Our main function will run next, which will take care of the templating
    and pushing of our configurations to the remote devices.
    """
    main()
