from setuptools import setup

with open('Emu86 Kernel PYPI Description.md', 'r') as f:
    long_description = f.read()

setup(
    name='emu86',
    version='0.0.9.4',
    packages=['kernels', 'kernels/att', 'kernels/intel', 'kernels/riscv',
              'kernels/mips_asm', 'kernels/mips_mml',
              'assembler', 'assembler/Intel', 'assembler/MIPS',
              'assembler/RISCV', 'assembler/WASM'],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
