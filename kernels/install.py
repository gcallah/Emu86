from jupyter_client.kernelspecapp  import InstallKernelSpec, RemoveKernelSpec


class InstallIntelKernel(InstallKernelSpec):
    version = 1.0
    kernel_name = "intel_kernel"
    description = "Install Intel kernel"
    
    def parse_command_line(self, argv):
        super(InstallKernelSpec, self).parse_command_line(argv)


class UninstallIntelKernel(RemoveKernelSpec):
    version = 1.0
    kernel_name = "intel_kernel"
    description = "Uninstall Intel kernel"

    def parse_command_line(self, argv):
        super(RemoveKernelSpec, self).parse_command_line(argv)

   
