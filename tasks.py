"""Tasks for use with Invoke.

(c) 2021 Calvin Remsburg
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from invoke import task

### ---------------------------------------------------------------------------
### DOCKER PARAMETERS
### ---------------------------------------------------------------------------
DOCKER_IMG = "ghcr.io/cdot65/juniper-mpls-l3vpn-demo"
DOCKER_TAG = "0.0.1"


### ---------------------------------------------------------------------------
### SYSTEM PARAMETERS
### ---------------------------------------------------------------------------
PWD = os.getcwd()


### ---------------------------------------------------------------------------
### DOCKER CONTAINER BUILD
### ---------------------------------------------------------------------------
@task
def build(context):
    # Build our docker image
    context.run(
        f"docker build -t {DOCKER_IMG}:{DOCKER_TAG} files/docker/",
    )


### ---------------------------------------------------------------------------
### DOCKER CONTAINER SHELL
### ---------------------------------------------------------------------------
@task
def shell(context):
    # Get access to the BASH shell within our container
    print("Jump into a container")
    context.run(
        f"docker run -it --rm \
            -v {PWD}/files:/home/files \
            -w /home/files/ \
            --hostname l3vpn-demo \
            {DOCKER_IMG}:{DOCKER_TAG} /bin/bash",
        pty=True,
    )


### ---------------------------------------------------------------------------
### TESTS
### ---------------------------------------------------------------------------
@task
def template(context):
    # Run the template_config.py script to build configurations without PyEZ
    print("Test the configuration build process")
    context.run(
        f"docker run -it --rm \
            -v {PWD}/files/:/home/files \
            -w /home/files/python/ \
            {DOCKER_IMG}:{DOCKER_TAG} python template_config.py",
        pty=True,
    )


### ---------------------------------------------------------------------------
### USE PyEZ TO BUILD CONFIGURATION AND PUSH TO DEVICES
### ---------------------------------------------------------------------------
@task
def pyez(context):
    # Run the configure.py script to build configurations and push with PyEZ
    print("Build and push configurations to devices")
    context.run(
        f"docker run -it --rm \
            -v {PWD}/files/:/home/files \
            -w /home/files/python/ \
            {DOCKER_IMG}:{DOCKER_TAG} python configure.py",
        pty=True,
    )
