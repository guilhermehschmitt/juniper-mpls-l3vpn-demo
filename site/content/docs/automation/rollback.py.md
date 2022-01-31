## Code Deep Dive

### 📝 Deep Dive

#### Imports

asdf

```python
import yaml  # type: ignore
from jnpr.junos import Device  # type: ignore
from jnpr.junos.utils.config import Config  # type: ignore
```

asdf

#### Inventory

asdf

```python
def inventory():
    """Load our inventory.yaml into a python object called routers."""
    devices = yaml.safe_load(open("inventory.yaml"))
    return devices
```

asdf

#### Main

asdf

```python
def main(devices):
    """Build connection, template config, and push to device.

    Loop over our list of routers that we imported from inventory.py
    Utilize the ID as the last octet within the IP address of the router
    Once the connection is open, print a message to the console
    Ingest the configuration variables stored in our device's' YAML file
    """
    for each in devices["routers"]:
        dev = Device(
            host=f"{each['ip']}",
            user="jcluser",
            password="Juniper!1",
            gather_facts=False,
        )
        dev.open()

        print(f"connected to {each['name']}")  # noqa T001

        """
        creating an empty dictionary called `data`
        then stuffing our YAML vars into it as 'configuration'
        this is to help handle PyEZ loading YAML vars differently than Jinja2
        """
        data = dict()
        data["configuration"] = yaml.safe_load(open(f"vars/{each['name']}.yaml"))

        configuration = Config(dev)

        configuration.load(
            template_path="templates/junos.j2", template_vars=data, format="set"
        )
        configuration.pdiff()
        if configuration.commit_check():
            configuration.commit()
        else:
            configuration.rollback()

        dev.close()
```

asdf

---

#### Initialize script

asdf

```python
if __name__ == "__main__":
    """Main script execution.

    We will first load our inventory.yaml file into a new Python object `devices`
    Our main function will run next, which will take care of the templating
    and pushing of our configurations to the remote devices.
    """
    devices = inventory()
    main(devices)

```

asdf

---

### 🚀 Workflow

The workflow will look like this:

1. Have Poetry install your Python packages in a virtual environment (one-time operation)
2. Activate your new virtual environment with Poetry
3. Run locally or within a container using the Invoke package

```bash
poetry install
poetry shell
invoke configure
```

---

### 🐍 Script

```python
"""rollback.py: perform a 'rollback 1' operation on our network devices."""
import yaml  # type: ignore
from jnpr.junos import Device  # type: ignore
from jnpr.junos.exception import CommitError  # type: ignore
from jnpr.junos.exception import ConnectError  # type: ignore
from jnpr.junos.exception import LockError  # type: ignore
from jnpr.junos.exception import RpcError  # type: ignore
from jnpr.junos.exception import UnlockError  # type: ignore
from jnpr.junos.utils.config import Config  # type: ignore


def inventory():
    """Load our inventory.yaml into a python object called routers."""
    devices = yaml.safe_load(open("inventory.yaml"))
    return devices


def main(devices):
    """Rollback the configuration to the previous state.

    Loop over our list of routers that we imported from inventory.py
    Utilize the ID as the last octet within the IP address of the router
    Once the connection is open, perform the following steps

    1. Print a message to the console
    2. Perform a "lock" on the configuration
    3. Rollback to the previous state
    4. Commit the configuration
    5. Perform an "unlock" on the configuration
    6. Gracefully exit the NETCONF session

    Various error handling mechanisms have been included to ensure that
    the operator safely exits the script when a known failure occurs.
    """
    for each in devices["routers"]:
        dev = Device(
            host=f"{each['ip']}",
            user="jcluser",
            password="Juniper!1",
            gather_facts=False,
        )
        try:
            dev.open()
            print(f"connected to {each['name']}")  # noqa T001
        except ConnectError as err:
            print(f"Cannot connect to {each['name']}: {err}")  # noqa T001
            return

        configuration = Config(dev)

        # Lock the configuration
        print("Locking the configuration")  # noqa T001
        try:
            configuration.lock()
        except LockError as err:
            print(f"Unable to lock configuration: {err}")
            dev.close()
            return
        try:
            print("Rolling back the configuration")  # noqa T001
            configuration.rollback(rb_id=1)
            print("Committing the configuration")  # noqa T001
            configuration.commit()
        except CommitError as err:
            print(f"Error: Unable to commit configuration: {err}")  # noqa T001
        except RpcError as err:
            print(f"Unable to roll back configuration changes: {err}")  # noqa T001

        print("Unlocking the configuration")  # noqa T001
        try:
            configuration.unlock()
        except UnlockError as err:
            print(f"Unable to unlock configuration: {err}")  # noqa T001
        dev.close()


if __name__ == "__main__":
    """Main script execution.

    We will first load our inventory.yaml file into a new Python object `devices`
    Our main function will run next, which will take care of the rolling back the
    configurations on the remote devices.
    """
    devices = inventory()
    main(devices)

```
