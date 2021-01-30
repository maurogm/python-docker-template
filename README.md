# python-docker-template


## Prerequisites

### Install Docker

- [for Mac](https://docs.docker.com/docker-for-mac/install/)
- [for Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [for Windows](https://docs.docker.com/docker-for-windows/install/)

After following the instructions, remember running the following:
```
sudo groupadd docker
sudo usermod -aG docker $USER
```
You may need to logout/reboot before the changes come into effect.


### Install required extensions in VSCode:

- Docker: ms-azuretools.vscode-docker
- Remote - Containers : ms-vscode-remote.remote-containers
  - Documentation available [here](https://code.visualstudio.com/docs/remote/containers)


## Setting up docker within VSCode

To access the Remote-Containers functionalities, toggle the menu by clicking the left-bottom corner of VSCode IDE.

You can add configuration files to an existing project by selecting `Add Development Container Configuration Files` and selecting the Python 3 template.

### Install libraries listed in requirements.txt during image build
Uncomment this section in the Dockerfile:
```
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp
```

### Set the PYTHONPATH to the directory that contains your modules
For example, if your modules are in the `src` directory inside your root folder, you should add the following to the Dockerfile:
```
ENV PYTHONPATH "${PYTHONPATH}:/src"
```
This way, whenever you try to import one of your modules, the interpretar will always look for them (among other places) in `/src`, without you having to manually add it to sys.path during runtime.

For more info on how Python handles paths for the `import` statement, refer to [this article](https://www.devdungeon.com/content/python-import-syspath-and-pythonpath-tutorial#toc-5)


### Add to devcontainer.json the extensions you wish to be automatically available
The _extensions_ field of the json contains an array with the IDs of the VSCode extensions you wish to have installed during the image build.

By default, the python plugin should be added.

If you are going to use Jupyter Notebooks, you should install the appropriate plugin, along with pylance (since linting inside notebooks is better when using pylance). The extensions array would then look like this:
```
"extensions": [
	"ms-python.python",
	"ms-toolsai.jupyter",
	"ms-python.vscode-pylance"
],
```

### Customize your VSCode settings in devcontainer.json
The _settings_ field of devcontainer.json contains a settings.json that will override the VSCode default settings inside the container.

By default it contains some paths configuring the linter and the formatter, as well as the integrated terminal and Python itself.

- To enable Pylance, add `"python.languageServer": "Pylance",`.

- Add `"jupyter.notebookFileRoot": "${workspaceFolder}"` so notebooks will execute from workspace, and find the PYTHONPATH to import modules.

- If you are using a library for unit testing, you have to enable it here. Beware that only one among unittest, pytest and nosetest can be enabled at once. Refer to [the documentation](https://code.visualstudio.com/docs/python/testing#_test-configuration-settings) to see how to configure your testing framework of choice.

In order to use `pytest`, add:
```
"python.testing.pytestEnabled": true,
```


### Comment out the remoteUser line in devcontainer.json
By default, the `"remoteUser": "vscode"` line is uncommented, but this may cause conflicts. If this happens, you can comment the line and just connect to the container as root.



## Running the container
To run the project inside the container, just toggle the Remote-Container prompt (by clicking on the bottom-left corner of the IDE) and select `Open in Container`.

The first time you try to run the container the image will be built. This might take a while.

While you are inside the container, the bottom left will say `Dev Container: _name_` (by default, name = "Python 3").

To exit the container, toggle the menu and select `Reopen locally`, or just `Close Remote Connection`.


## Possible problems

#### **Limited notebook functionalities**
Possible fixes:
- Check the jupyter plugin is installed.
- Check the pylance plugin is installed and enabled in the settings.
- Remember enabling the appropriate kernel for the version of python you are using. Sometimes it is not selected by default.

#### **VSCode discovers the tests but fails to import the test module**
Check that you have an `__init__.py` file in every subfolder up to the script containing the test, or VSCode won't be able to find load it.
It might run from the console, though.


#### **Image build fails when trying to download something from the internet (e.g. during pip install -r requirements) due to conflict with VPN**
Edit `/etc/docker/daemon.json` (or create it if it doesn't exist) and add `"bip": "172.37.0.1/16"`.

#### **You need to download an image from an insecure registry**
Edit `/etc/docker/daemon.json` (or create it if it doesn't exist) and add `"insecure-registries" : ["YOUR_REGISTRY"]`.
