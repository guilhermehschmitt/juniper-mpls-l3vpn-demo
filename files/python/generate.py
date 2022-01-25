"""Generate bootstrap configurations for our network devices."""
import yaml  # type: ignore
from inventory import routers
from jinja2 import Environment, FileSystemLoader

# define Jinja2 environment
CONFIG_PATH = "../junos/generated"


def main():
    """Template configuration with Jinja2 and store locally."""
    # set up our Jinja2 environment
    file_loader = FileSystemLoader("./")
    env = Environment(loader=file_loader, autoescape=True)
    env.trim_blocks = True
    env.lstrip_blocks = True

    # begin loop over devices
    for each in routers:
        # create a template based on variables stored in file
        with open(f"vars/{each['device']}.yaml", "r") as stream:
            try:
                # set up  our environment and render configuration
                variables = yaml.safe_load(stream)
                template = env.get_template("templates/junos.j2")
                output = template.render(configuration=variables)

                # write our rendered configuration to a local file
                with open(f"{CONFIG_PATH}/{each['device']}.conf", "w") as f:
                    for line in output.splitlines():
                        cleanedLine = line.strip()
                        if cleanedLine:
                            f.write(cleanedLine + str("\n"))
                print(f"config built: {CONFIG_PATH}/{each['device']}.conf")  # noqa T001
            except yaml.YAMLError as exc:
                print(exc)  # noqa T001


if __name__ == "__main__":
    main()
