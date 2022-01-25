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

# ---------------------------------------------------------------------------
# DOCKER PARAMETERS
# ---------------------------------------------------------------------------
DOCKER_IMG = "ghcr.io/cdot65/juniper-mpls-l3vpn-demo"
DOCKER_TAG = "0.0.1"


# ---------------------------------------------------------------------------
# SYSTEM PARAMETERS
# ---------------------------------------------------------------------------
PWD = os.getcwd()


# ---------------------------------------------------------------------------
# DOCKER CONTAINER BUILD
# ---------------------------------------------------------------------------
@task
def build(context):
    """Build an instance of the Docker container image locally."""
    context.run(
        f"docker build -t {DOCKER_IMG}:{DOCKER_TAG} files/docker/",
    )


# ---------------------------------------------------------------------------
# DOCKER CONTAINER SHELL
# ---------------------------------------------------------------------------
@task
def shell(context):
    """Get access to the BASH shell within our container."""
    print("Jumping into the container's bash shell")  # noqa T001
    context.run(
        f"docker run -it --rm \
            -v {PWD}/files:/home/files \
            -w /home/files/ \
            --hostname l3vpn-demo \
            {DOCKER_IMG}:{DOCKER_TAG} /bin/bash",
        pty=True,
    )


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------
@task
def generate(context):
    """Run the generate.py script to build configs without PyEZ."""
    print("Building the configuration locally with Jinaj2")  # noqa T001
    context.run(
        f"docker run -it --rm \
            -v {PWD}/files/:/home/files \
            -w /home/files/python/ \
            {DOCKER_IMG}:{DOCKER_TAG} python generate.py",
        pty=True,
    )


@task
def bandit(context):
    """Check to see if there are any security issues with our code."""
    print("Test for any security problems with our code")  # noqa T001
    context.run(
        f"docker run -it --rm \
            -v {PWD}/files/:/home/files \
            -w /home/files/ \
            {DOCKER_IMG}:{DOCKER_TAG} bandit -r .",
        pty=True,
    )


@task
def flake8(context):
    """Check to see if there are any formatting issues with our code."""
    print("Test for any formatting issues within our code")  # noqa T001
    context.run(
        f"docker run -it --rm \
            -v {PWD}/files/:/home/files \
            -w /home/files/ \
            {DOCKER_IMG}:{DOCKER_TAG} flake8 .",
        pty=True,
    )


@task
def pydocstyle(context):
    """Check to see if there are any documentation issues with our code."""
    print("Test for any missing documentation within our code")  # noqa T001
    context.run(
        f"docker run -it --rm \
            -v {PWD}/files/:/home/files \
            -w /home/files/ \
            {DOCKER_IMG}:{DOCKER_TAG} pydocstyle .",
        pty=True,
    )


# ---------------------------------------------------------------------------
# USE PyEZ TO BUILD CONFIGURATION AND PUSH TO DEVICES
# ---------------------------------------------------------------------------
@task
def configure(context):
    """Build and push our configurations with PyEZ."""
    print("Build and push configurations to devices")  # noqa T001
    context.run(
        f"docker run -it --rm \
            -v {PWD}/files/:/home/files \
            -w /home/files/python/ \
            {DOCKER_IMG}:{DOCKER_TAG} python configure.py",
        pty=True,
    )


# ---------------------------------------------------------------------------
# USE Jinja2 TO BUILD CONFIGURATION AND STORE IN bootstrap DIRECTORY
# ---------------------------------------------------------------------------
@task
def bootstrap(context):
    """Build and push our configurations with PyEZ."""
    print("Build and push configurations to devices")  # noqa T001
    context.run(
        f"docker run -it --rm \
            -v {PWD}/files/:/home/files \
            -w /home/files/python/bootstrap \
            {DOCKER_IMG}:{DOCKER_TAG} python bootstrap.py",
        pty=True,
    )
