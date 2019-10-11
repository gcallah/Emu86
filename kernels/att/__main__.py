from ipykernel.kernelapp import IPKernelApp
from .kernel import AttKernel

IPKernelApp.launch_instance(kernel_class=AttKernel)
