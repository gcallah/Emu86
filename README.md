# Emu86
This project will emulate an x86 assembler in Python, as a learning tool for students.

This project has now been expanded to emulating x86 assembler in Jupyter notebooks: [Emu86 Kernel](https://github.com/gcallah/Emu86/blob/master/kernels/README.md)

## View this project on web
[Link to Pythonanywhere](https://emu86.pythonanywhere.com)

## To Run (Bypassing Docker)
Create and activate the virtual environment
```
source venv.sh
```

Install dev dependencies
```
make dev_env
```

Generate a secret key for Django settings
```
./manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Exit the interactive mode, and run:
```
export SECRET_KEY = "<the generated key>"
```

Run
```
make dev
```