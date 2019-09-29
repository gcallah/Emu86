from ipykernel.kernelapp import IPKernelApp
from .kernel import Mips_asmKernel

IPKernelApp.launch_instance(kernel_class=Mips_asmKernel)
