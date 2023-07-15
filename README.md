![build](https://github.com/FZJ-JSC/jupyter-nestdesktop/workflows/build/badge.svg)

# jupyter-nestdesktop-proxy
Integrate NEST Desktop in your Jupyter environment for an fast, feature-rich and easy to use remote desktop in the browser.

## Requirements
- Python 3.6+
- Jupyter Notebook 6.0+
- JupyterLab >= 3.x
- jupyter-server-proxy >= 3.1.0

This package executes the `nest-desktop` command. This command assumes the `nest-desktop` command is available in the environment's $PATH.

## Security
Be aware, [NEST Desktop](https://nest-desktop.readthedocs.io) does not encrypt the communication and/or requires password to connect.  

### NEST Desktop
[NEST Desktop](https://nest-desktop.readthedocs.io) is a web-based GUI application for NEST Simulator, an advanced simulation tool for the computational neuroscience.

### Jupyter-Server-Proxy
[Jupyter-Server-Proxy](https://jupyter-server-proxy.readthedocs.io) lets you run arbitrary external processes (such as Xpra-HTML5) alongside your notebook, and provide authenticated web access to them.

## Install 

#### Create and Activate Environment
```
virtualenv -p python3 venv
source venv/bin/activate
```

#### Install jupyter-nestdesktop-proxy
```
pip install git+https://github.com/FZJ-JSC/jupyter-nestdesktop-proxy.git
```

#### Enable jupyter-nestdesktop-proxy Extensions
For Jupyter Classic, activate the jupyter-server-proxy extension:
```
jupyter serverextension enable --sys-prefix jupyter_server_proxy
```

For Jupyter Lab, install the @jupyterlab/server-proxy extension:
```
jupyter labextension install @jupyterlab/server-proxy
jupyter lab build
```

#### Start Jupyter Classic or Jupyter Lab
Click on the NEST Desktop icon from the JupyterLab Launcher or the NEST Desktop item from the New dropdown in Jupyter Classic.  
Connect to your database as instructed in the Quickstart section.

## Configuration
This package calls `nest-desktop` with settings. Please read the [NEST Desktop](https://nest-desktop.readthedocs.io/en/latest/user/index.html) if you want to know the details.  
You have to modify `setup_nestdesktop()` in `jupyter_nestdesktop_proxy/__init__.py` for change.

## Credits
- NEST Desktop
- jupyter-server-proxy

## License
BSD 3-Clause
