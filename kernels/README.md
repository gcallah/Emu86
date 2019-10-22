# Emu86 Kernel
## Installation Instructions in Terminal
1. `pip install emu86`
2. `python -m kernels.INSERT_LANGUAGE_NAME.install`
    - INSERT_LANGUAGE_NAME is the name of the assembly language as spelled for folders [here](https://github.com/gcallah/Emu86/tree/master/kernels)
    - eg: `python -m kernels.mips_asm.install`
## Using Emu86 Kernel in Jupyter Notebook
1. Type `jupyter notebook` in terminal
2. After jupyter notebook launches in browser, click the `New` dropdown on the upper right and then click on the assembly language you want
## Update to Latest Version in Terminal (if you already have Emu86 Kernel Installed)
1. `pip install emu86==LATEST_VERSION_NUMBER`
    - Find the latest version [here](https://pypi.org/project/emu86/#history) 
    - eg: if latest version number is 0.0.2: `pip install emu86==0.0.2`
## Uninstallation Instruction in Terminal
1. `python -m kernels.INSERT_LANGUAGE_NAME.uninstall`
    - INSERT_LANGUAGE_NAME is the name of the assembly language as spelled for folders [here](https://github.com/gcallah/Emu86/tree/master/kernels)
    - eg: `python -m kernels.mips_asm.uninstall`
## For Development Purposes
Steps to properly deploy new releases to PYPI:
1. Update the version variable value in [setup.py](https://github.com/gcallah/Emu86/blob/master/setup.py)
2. Git commit messages must be written in this format: `pypi release v*`
    - the * represents where you can put the version number and additional information about this new release
    - eg: `pypi release v0.0.1 upload emu86`
3.  Make sure the version is the same for [setup.py](https://github.com/gcallah/Emu86/blob/master/setup.py) and git commit message and that it also increases from the last PYPI version release (see [PYPI release history](https://pypi.org/project/emu86/#history)) before pushing the git commit 


