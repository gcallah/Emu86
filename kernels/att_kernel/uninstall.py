from jupyter_client.kernelspec import KernelSpecManager

kernel_name = "att"


def uninstall_intel_kernel():
    print("Uninstalling", kernel_name, "kernel...")
    KernelSpecManager().remove_kernel_spec(kernel_name)
    print(kernel_name.capitalize(), "kernel uninstallation complete")


if __name__ == '__main__':
    uninstall_intel_kernel()
