# Emu86
This project will emulate an x86 assembler in Python, as a learning tool for students.

This project has now been expanded to emulating x86 assembler in Jupyter notebooks: [Emu86 Kernel](https://github.com/gcallah/Emu86/blob/master/kernels/README.md)

## To Run (Bypassing Docker)
Create and activate the virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```
pip install -r docker/requirements-dev.txt --upgrade
```
Run
```
python3 manage.py runserver
```