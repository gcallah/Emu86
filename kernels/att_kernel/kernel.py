from ipykernel.kernelbase import Kernel
from assembler.virtual_machine import IntelMachine
from assembler.assemble import assemble


class AttKernel(Kernel):
    implementation = 'att_kernel'
    implementation_version = '1.0'
    language = 'att'
    language_version = '1.0'
    language_info = {
        'name': 'att',
        'mimetype': 'att',
        'file_extension': 'x86',
    }
    banner = "Att kernel - run att assembly language"
    vm_machine = None

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):

        if not silent:
            if not self.vm_machine:
                self.vm_machine = IntelMachine()
                self.vm_machine.base = 'dec'
                self.vm_machine.flavor = 'att'
            (last_instr, error, bit_code) = assemble(code, self.vm_machine)

            if error == "":
                vm_machine_info = {'name': 'att_machine_info'}
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
