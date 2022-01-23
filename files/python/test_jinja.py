#!/usr/bin/env python

from jinja2 import Environment, FileSystemLoader
import yaml

# define Jinja2 environment
file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True

# create a template based on variables stored in file
with open("vars/sanantonio.yaml", "r") as stream:
    try:
        variables = yaml.safe_load(stream)
        template = env.get_template("junos.j2")
        output = template.render(configuration=variables)
        with open("../junos/generated/sanantonio.conf", "w") as f:
            for line in output.splitlines():
                cleanedLine = line.strip()
                if cleanedLine:  # is not empty
                    f.write(cleanedLine + str("\n"))
                    print(cleanedLine)

    except yaml.YAMLError as exc:
        print(exc)
