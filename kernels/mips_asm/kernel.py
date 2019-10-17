from ipykernel.kernelbase import Kernel
from assembler.virtual_machine import MIPSMachine
from assembler.assemble import assemble


class Mips_asmKernel(Kernel):
    implementation = 'mips_asm_kernel'
    implementation_version = '1.0'
    language = 'mips_asm'
    language_version = '1.0'
    language_info = {
        'name': 'mips_asm',
        'mimetype': 'mips_asm',
        'file_extension': 'x86',
    }
    banner = "Mips_asm kernel - run mips_asm assembly language"
    vm_machine = None

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):

        if not silent:
            if not self.vm_machine:
                self.vm_machine = MIPSMachine()
                self.vm_machine.base = 'hex'
                self.vm_machine.flavor = 'mips_asm'
            (last_instr, error, bit_code) = assemble(code, self.vm_machine)

            if error == "":
                vm_machine_info = {}
                reg_changes = []
                mem_changes = []
                output = "Changes: <br />"
                for reg in self.vm_machine.registers:
                    if reg in self.vm_machine.changes:
                        reg_changes.append((reg, self.vm_machine.registers[reg]))

                for chng in self.vm_machine.changes:
                    if "MEM" in chng:
                        loc = chng.strip("MEM")
                        mem_changes.append((loc, self.vm_machine.memory[loc]))

                output += self.construct_table(reg_changes, mem_changes)
                vm_machine_info['data'] = {
                    'text/html': output
                }
                self.send_response(self.iopub_socket,
                                   'display_data', vm_machine_info)
            else:
                error_msg = {'name': 'error_msg', 'text': error}
                self.send_response(self.iopub_socket, 'stream', error_msg)

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}
                }

    def construct_table(self, reg_changes, mem_changes):
        output = '<table><tr><th>Register</th><th>Register Value</th>'
        output += '<th>Memory Location</th><th>Memory Value</th></tr>'
        index = 0
        while index < max(len(reg_changes), len(mem_changes)):
            row = '<tr>'
            empty_cells = '<td></td><td></td>'
            if index >= len(reg_changes):
                row += empty_cells
            else:
                reg_name, reg_val = reg_changes[index]
                row += f'<td>{reg_name}</td><td>{reg_val}</td>'
            if index >= len(mem_changes):
                row += empty_cells
            else:
                mem_loc, mem_val = mem_changes[index]
                row += f'<td>{mem_loc}</td><td>{mem_val}</td>'
            row += "</tr>"
            output += row
            index += 1
        output += "</table>"
        return output
