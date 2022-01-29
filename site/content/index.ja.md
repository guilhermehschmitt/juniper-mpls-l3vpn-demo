# 🐍 Build and Deploy a MPLS L3VPN with Juniper Networks PyEZ

<img src="https://raw.githubusercontent.com/cdot65/juniper-mpls-l3vpn-demo/main/files/images/topology-100.jpg" width="720px"/>


## Welcome

First off, hello and welcome to the landing page of my demo's documentation. My name is Calvin and I work in the sales organization at Juniper Networks; I hope that you will find this project helpful.

In this demonstration, we will deploy a L3VPN circuit across an MPLS backbone using Juniper's PyEZ library. For those without access to Juniper's vLabs, I have provided a sample lab topology for EVE-NG within the project files.

This landing page will provide an overview of the components of this project, for a more detailed look at a specific topic please reference the navigation bar or click on the provided links within a topic.

---

### Table of Contents

| Link                                                                           | Description                                                       |
| ------------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| [Automation](https://cdot65.github.io/juniper-mpls-l3vpn-demo/#automation)     | Overview on scripts, tools, and workflows.                        |
| [Network](https://cdot65.github.io/juniper-mpls-l3vpn-demo/#network)           | Design of the network, protocols used, IP address scheme.         |
| [Provisioning](https://cdot65.github.io/juniper-mpls-l3vpn-demo/#provisioning) | Using PyEZ to template and push configurations.                   |
| [Validating](https://cdot65.github.io/juniper-mpls-l3vpn-demo/#validating)     | Running JSNAPy tests to validate the network's operational state. |

---

## Automation

### 📝 Overview

Our primary goal today is to use PyEZ to provision eight Juniper vMX routers into various elements of an MPLS network.

While PyEZ has the capability of pushing individual lines, or groups of lines, of configurations to a device, here we will be building and pushing an entire configuration.

We will also be following the guiding principles of [Infrastructure-as-Code]("https://en.wikipedia.org/wiki/Infrastructure_as_code"), where we will store our the elements of our configuration as YAML, to be ran through a Jinja2 template to output our configurations.

### 🐍 Python scripts, Jinja2 templates, and variable files

All of our project's scripts, variables, and template files are stored within the [files/python](https://github.com/cdot65/juniper-mpls-l3vpn-demo/tree/main/files/python) directory.

```bash
files/python
├── configurations/
├── templates/
├── vars/
├── configure.py
├── download.py
├── generate.py
├── inventory.yaml
└── rollback.py
```

#### Python Scripts

You likely don't need me to explain that the files that end with `.py` are the various Python scripts. Here is a quick glimpse into the four provided.

| Script         | Action                                              |
| -------------- | --------------------------------------------------- |
| `generate.py`  | Build the configurations locally with Jinaj2.       |
| `configure.py` | Build and push our configurations with PyEZ.        |
| `download.py`  | Download our configurations with PyEZ.              |
| `rollback.py`  | Rollback to our bootstrap configurations with PyEZ. |

#### Inventory file

The `inventory.yaml` file stores information about our devices, basic information like hostname and IP address.

#### `configurations/` directory

If you choose to generate the configurations locally but _not_ push them to the devices, then you will find the generated configurations within the `configurations` directory. I had also included the working final configurations in this directory if you just want to see the resulting configurations.

#### `templates/` directory

Since we are storing our configuration as code, we will need some kind of templating engine to run our variables through to produce the configurations. For this we have Jinja2 to handle the templating, and its template files are stored in the `templates` directory.

#### `vars/` directory

Finally, the device's configuration will be stored as YAML files found within the `vars/` directory. Each device will have its own file to represent its configuration. We will run these files through the Jinaj2 templates to produce our configurations.

---

### 🛠️ Tools

In hopes to making this project as easy as possible to execute, I have provided many tools to help with execution of the tasks within this project.

#### Poetry

A [Poetry](https://python-poetry.org/docs/) lock file to help you create a Python environment that mirrors my own. As long as you [have Poetry installed on your machine](https://python-poetry.org/docs/), to you can simply type `poetry install` to create the virtual environment, followed by `poetry shell` to activate it.

#### Invoke

You will find a packaged called [Invoke](http://www.pyinvoke.org/) installed within the virtual environment. Invoke is an elegant way to create CLI shortcuts for commands that are long to type out. Here is a short list of some of the Invoke operations created in the `tasks.py` file.

| Command            | Action                                              |
| ------------------ | --------------------------------------------------- |
| `invoke generate`  | Build the configurations locally with Jinaj2.       |
| `invoke configure` | Build and push our configurations with PyEZ.        |
| `invoke download`  | Download our configurations with PyEZ.              |
| `invoke rollback`  | Rollback to our bootstrap configurations with PyEZ. |

#### Dockerfile

A Dockerfile has also been provided for those that would like to execute this within an isolated container instead of a virtual environment. A couple of additional Invoke tasks are listed below to help with building and accessing the Docker container environment.

| Command        | Action                                                   |
| -------------- | -------------------------------------------------------- |
| `invoke build` | Build an instance of the Docker container image locally. |
| `invoke shell` | Get access to the BASH shell within our container.       |

---

### 🚀 Workflow

The workflow will look like this:

1. Have Poetry install your Python packages in a virtual environment (one-time operation)
2. Activate your new virtual environment with Poetry
3. Run locally or within a container using the Invoke package

```bash
poetry install
poetry shell
invoke xyz
```

---

## Network

### Topology

When talking about our network design, I will be referencing the following Juniper vLabs topology image below; the color tagging used within the topology makes it easier to associate a router to a specific role.

<img src="https://raw.githubusercontent.com/cdot65/juniper-mpls-l3vpn-demo/main/files/images/vlabs.png" width="720px"/>

### IP Addressing

I take a pragmatic approach to building an IP address schema.

Each router will be given an ID of 11-17, and its loopback/router-id will be built upon it within the prefix of `192.168.255.{x}/32`, where `{x}` represents the local device's ID.

Additionally, P2P connections will follow a pattern of `10.{x}.{y}.{x}/24`, where `{x}` represents the local device's ID and `{y}` represents the ID of the remote router.

> **Example: Router1**

```yaml
loopback0 = "192.168.255.11"
router id = "192.168.255.11"
p2p to router2 = "10.11.12.11/24"
p2p to router3 = "10.11.13.11/24"
p2p to router5 = "10.11.15.11/24"
```

### MPLS

The MPLS-aware routers are tagged with the green label of "MPLS" in the vLabs topology. We will be using LDP for signaling labels, which will limit the features we can perform within the network while conversely making it easier to provision.

To build an MPLS neighborship with LDP between two router interfaces, you will see in the configurations that a few parameters need to be setup:

> **enable the family of MPLS on the interface configuration**

```
set interfaces ge-0/0/1.0 family mpls
```

> **list the interface under the protocols/mpls configuration**

```
set protocols mpls interface ge-0/0/1.0
set protocols ldp interface ge-0/0/1.0
```

#### L3VPN

Each router participating within the MPLS L3VPN circuit will build their route-distinguisher off a similar pattern to our loopbacks, `192.168.255.{x}:100`, where `{x}` represents the router's ID

```
set routing-instances Customer1 instance-type vrf
set routing-instances Customer1 route-distinguisher 192.168.255.11:100
```

The routes that we import and export will be managed by the `target:{a}:{b}` structure, where `{a}` represents the BGP ASN and `{b}` respresents the customer's ID

```
set routing-instances Customer1 vrf-target target:300:100
```

### Routing

To best emulate a small ISP, I have opted to use OSPF between the MPLS routers, with external BGP peering with both customer connections.

> **PE1 Configuration: OSPF to MPLS backbone**

```
set protocols ospf area 0.0.0.0 interface ge-0/0/2.0 interface-type p2p
set protocols ospf area 0.0.0.0 interface ge-0/0/3.0 interface-type p2p
set protocols ospf area 0.0.0.0 interface lo0.0 passive
```

> **PE1 Configuration: external BGP to CE1**

```
set routing-instances Customer1 instance-type vrf
set routing-instances Customer1 protocols bgp group Customer1 type external
set routing-instances Customer1 protocols bgp group Customer1 peer-as 65000
set routing-instances Customer1 protocols bgp group Customer1 neighbor 74.51.192.1
```

As iBGP is needed to signal PE routers to share L3VPN routes, we will of course be using it for that usecase in our topology.

> **PE1 Configuration: L3VPN PE4**

```
set protocols bgp group MPLS type internal
set protocols bgp group MPLS local-address 192.168.255.11
set protocols bgp group MPLS family inet-vpn unicast
set protocols bgp group MPLS peer-as 300
set protocols bgp group MPLS neighbor 192.168.255.16

```

---

## Provisioning

There are four elements of job briefings:

1. Daily briefing.
2. Job site assessment.
3. Job briefing.
4. Post-job briefing.

Every job requires these four elements, including storm response and service restoration jobs.

> **Note:**
> When you work alone, you must complete the four elements of a job briefing as carefully as when you are part of a crew. Lone worker briefings are planning processes that include thinking through all of the same topics as crew briefings, including hazards, work procedures, and emergency plans.
>
> You do not have to document job briefings as a lone worker. If you start a job by working alone, but another crew member or entire crew arrives later to help, you do have to document job briefings, starting when the other crew member or crew arrives at the job site.

### Workflow

The EIC or DCM will hold a daily briefing at the beginning of each work day. All the crew members who will work on the job that day have to attend the daily briefing. The daily briefing gets the entire crew involved in planning for the day’s work.

The daily briefing is held at your reporting location, not at the job site.

---

## Validating

# Attollite incipit vestes et tamen et luctus

## Volvitur similes

Lorem markdownum diris ad saligno solae. Est tuo huic facinusque tamen tegat
saevit nec notam citharae dedit Phoebes talis. Inquam tali nasci! Dux tenui,
alas edere **effodit** Procrusten.

    wavelength += scalableFileP.formula_passive_type(lunWavelengthAjax(-1,
            cmsBluetoothBasic, tween(checksumComponentDdr, impactDebugger)),
            -3);
    var intellectual = -3;
    readSystemRipcording.ip = ttlJoystickOn(ribbon, cycle_format);
    nonFull /= ipIp;
    if (powerpoint_software(17910, application) >= copyrightCloudPlatform) {
        page.textCameraXhtml(appletMedia, waveSymbolic + 5);
        uml_dram_binary(consoleWindowArchive + cgi_uri, balance_pop_json -
                vista_bit, javaServiceFramework(3, multi_express, hypermedia));
    } else {
        output = encoding * firmwareCore + 4;
        video *= -1;
    }

### Workflow

Lorem markdownum diris ad saligno solae. Est tuo huic facinusque tamen tegat
saevit nec notam citharae dedit Phoebes talis. Inquam tali nasci! Dux tenui,
alas edere **effodit** Procrusten.

    wavelength += scalableFileP.formula_passive_type(lunWavelengthAjax(-1,
            cmsBluetoothBasic, tween(checksumComponentDdr, impactDebugger)),
            -3);
    var intellectual = -3;
    readSystemRipcording.ip = ttlJoystickOn(ribbon, cycle_format);
    nonFull /= ipIp;
    if (powerpoint_software(17910, application) >= copyrightCloudPlatform) {
        page.textCameraXhtml(appletMedia, waveSymbolic + 5);
        uml_dram_binary(consoleWindowArchive + cgi_uri, balance_pop_json -
                vista_bit, javaServiceFramework(3, multi_express, hypermedia));
    } else {
        output = encoding * firmwareCore + 4;
        video *= -1;
    }