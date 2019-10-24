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
            
            self.vm_machine.changes_init()
            (last_instr, error, bit_code) = assemble(code, self.vm_machine,
                                                     web=False)

            if error == "":
                vm_machine_info = {}
                reg_changes = []
                mem_changes = []
                output = "Changes: <br />"
                for reg in self.vm_machine.registers:
                    if reg in self.vm_machine.changes:
                        reg_val = self.vm_machine.registers[reg]
                        reg_changes.append((reg, reg_val))

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
        output = '<table><tr><th>Type</th><th>Identifier</th><th>Value</th>'
        for reg_name, reg_val in reg_changes:
            output += f'''<tr><td>Register</td><td>{reg_name}</td>
            <td>{reg_val}</td></tr>'''
        for mem_loc, mem_val in mem_changes:
            output += f'''<tr><td>Memory</td><td>{mem_loc}</td>
            <td>{mem_val}</td></tr>'''
        output += "</table>"
        return output
        output += "</table>"
        return output
