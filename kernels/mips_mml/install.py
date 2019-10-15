import json
import os
import sys

from IPython.utils.tempdir import TemporaryDirectory
from jupyter_client.kernelspec import KernelSpecManager


kernel_name = "mips_mml"
kernel_json = {
    "argv": [sys.executable, "-m", "kernels." + kernel_name,
             "-f", "{connection_file}"],
    "display_name": kernel_name.capitalize()
}


def install_kernel(user=True, prefix=None):
    with TemporaryDirectory() as tempdir:
        os.chmod(tempdir, 0o755)  # Starts off as 700, not user readable
        with open(os.path.join(tempdir, "kernel.json"), "w") as f:
            json.dump(kernel_json, f, sort_keys=True)
        print("Installing", kernel_name, "kernel...")
        KernelSpecManager().install_kernel_spec(tempdir, kernel_name, user,
                                                replace=True, prefix=prefix)
        print(kernel_name.capitalize(), "kernel installation complete")


if __name__ == '__main__':
    install_kernel()
