from ipykernel.kernelapp import IPKernelApp
from .kernel import Mips_mmlKernel

IPKernelApp.launch_instance(kernel_class=Mips_mmlKernel)
