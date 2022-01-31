## Dockerfile

A Dockerfile has also been provided for those that would like to execute this within an isolated container instead of a virtual environment.

For those that created a virtual environment with Poetry, we have provided a couple of additional Invoke tasks below to help with building and accessing the Docker container environment.

| Command        | Action                                                   |
| -------------- | -------------------------------------------------------- |
| `invoke build` | Build an instance of the Docker container image locally. |
| `invoke shell` | Get access to the BASH shell within our container.       |

FWIW, all tasks within Invoke's `tasks.py` file are tied to Docker containers.

---

### 🚀 Workflow

The workflow will look like this:

1. Have Poetry install your Python packages in a virtual environment (one-time operation)
2. Activate your new virtual environment with Poetry
3. Build Docker container image (one-time operation)
4. Run locally or within a container using the Invoke package

```bash
poetry install
poetry shell
invoke build
invoke configure
```

![poetry install](./site/content/assets/images/poetry_install.png)

![poetry shell](./site/content/assets/images/poetry_shell.png)
