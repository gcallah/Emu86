from ipykernel.kernelapp import IPKernelApp
from .kernel import IntelKernel

IPKernelApp.launch_instance(kernel_class=IntelKernel)
