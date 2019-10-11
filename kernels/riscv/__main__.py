from ipykernel.kernelapp import IPKernelApp
from .kernel import RiscvKernel

IPKernelApp.launch_instance(kernel_class=RiscvKernel)
