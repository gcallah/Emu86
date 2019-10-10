from ipykernel.kernelbase import Kernel
from assembler.virtual_machine import IntelMachine
from assembler.assemble import assemble


class IntelKernel(Kernel):
    implementation = 'intel_kernel'
    implementation_version = '1.0'
    language = 'intel'
    language_version = '1.0'
    language_info = {
        'name': 'intel',
        'mimetype': 'intel',
        'file_extension': 'x86',
    }
    banner = "Intel kernel - run intel assembly language"
    vm_machine = None

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):

        if not silent:
            if not self.vm_machine:
                self.vm_machine = IntelMachine()
                self.vm_machine.base = 'dec'
                self.vm_machine.flavor = 'intel'
            (last_instr, error, bit_code) = assemble(code, self.vm_machine)

            if error == "":
                vm_machine_info = {'name': 'intel_machine_info'}
                output = "Registers Changes: /n"
                for reg in self.vm_machine.registers:
                    if reg in self.vm_machine.changes:
                        output += f'{reg}: {self.vm_machine.registers[reg]}/n'

                output = "Memory Changes: /n"
                for chng in self.vm_machine.changes:
                    if "MEM" in chng:
                        loc = chng.strip("MEM")
                        output += f'{loc}: {self.vm_machine.memory[loc]}/n'

                vm_machine_info['text'] = output
                self.send_response(self.iopub_socket,
                                   'stream', vm_machine_info)
            else:
                error_msg = {'name': 'error_msg', 'text': error}
                self.send_response(self.iopub_socket, 'stream', error_msg)

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}
                }
