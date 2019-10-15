from distutils.core import setup

setup(
    name='emu86',
    version='0.0.3',
    packages=['kernels', 'kernels/att', 'kernels/intel', 'kernels/riscv',
              'kernels/mips_asm', 'kernels/mips_mml', 
              'assembler', 'assembler/Intel', 'assembler/MIPS',
              'assembler/RISCV', 'assembler/WASM'],
)
