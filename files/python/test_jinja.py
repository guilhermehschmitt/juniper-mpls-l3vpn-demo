#!/usr/bin/env python

from jinja2 import Environment, FileSystemLoader
import yaml

from inventory import routers

# define path for config files
CONFIG_PATH = "../junos/generated"

# define Jinja2 environment
file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True

for each in routers:
    # create a template based on variables stored in file
    with open(f"vars/{each['device']}.yaml", "r") as stream:
        try:
            variables = yaml.safe_load(stream)
            template = env.get_template("junos.j2")
            output = template.render(configuration=variables)
            with open(f"{CONFIG_PATH}/{each['device']}.conf", "w") as f:
                for line in output.splitlines():
                    cleanedLine = line.strip()
                    if cleanedLine:  # is not empty
                        f.write(cleanedLine + str("\n"))
                        print(cleanedLine)

        except yaml.YAMLError as exc:
            print(exc)
