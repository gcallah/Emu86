from ipykernel.kernelbase import Kernel
from assembler.virtual_machine import MIPSMachine
from assembler.assemble import assemble


class Mips_mmlKernel(Kernel):
    implementation = 'mips_mml_kernel'
    implementation_version = '1.0'
    language = 'mips_mml'
    language_version = '1.0'
    language_info = {
        'name': 'mips_mml',
        'mimetype': 'mips_mml',
        'file_extension': 'x86',
    }
    banner = "Mips_mml kernel - run mips_mml assembly language"
    vm_machine = None

    def has_one_data_first(self, code):
        data_first = -1
        text_first = -1
        data_seg = False
        text_seg = True
        lines = code.split("\n")
        data_seg_count = 0
        data_seg_found = False
        text_seg_found = False
        for index in range(len(lines)):
            line = lines[index]
            if line.find(';') > -1:
                line = line[:line.find(';')]

            line = line.strip()
            if len(line) == 0:
                continue

            if line[:5] == ".data":
                data_seg = True
                text_seg = False
                data_seg_count += 1
                data_seg_found = True
                continue
            elif line[:5] == ".text":
                data_seg = False
                text_seg = True
                text_seg_found = True
                continue
            if data_seg and data_first == -1:
                data_first = index
            elif text_seg and text_first == -1:
                text_first = index

        if data_seg_found and not text_seg_found:
            return ""
        errors = []
        if data_first > text_first:
            errors.append("Data segment is after text segment.")
        if data_seg_count > 1:
            errors.append("Code has more than one data segment.")
        return "\n".join(errors)

    def parse_changes(self):
        reg_changes = []
        mem_changes = []
        flag_changes = []
        for reg in self.vm_machine.registers:
            if reg in self.vm_machine.changes:
                reg_val = self.vm_machine.registers[reg]
                reg_changes.append((reg, reg_val))

        for chng in self.vm_machine.changes:
            if "MEM" in chng:
                loc = chng.replace("MEM", "")
                mem_changes.append((loc, self.vm_machine.memory[loc]))
            if "FLAG" in chng:
                flag_nm = chng.replace("FLAG", "")
                flag_changes.append((flag_nm, self.vm_machine.flags[flag_nm]))

        return reg_changes, mem_changes, flag_changes

    def construct_table(self, reg_changes, mem_changes, flag_changes):
        output = '<table><tr><th>Type</th><th>Identifier</th><th>Value</th>'
        for reg_name, reg_val in reg_changes:
            output += f'''<tr><td>Register</td><td>{reg_name}</td>
            <td>{reg_val}</td></tr>'''
        for mem_loc, mem_val in mem_changes:
            output += f'''<tr><td>Memory</td><td>{mem_loc}</td>
            <td>{mem_val}</td></tr>'''
        for flag_nm, flag_val in flag_changes:
            output += f'''<tr><td>Flag</td><td>{flag_nm}</td>
            <td>{flag_val}</td></tr>'''
        output += "</table>"
        return output

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):

        if not silent:
            if not self.vm_machine:
                self.vm_machine = MIPSMachine()
                self.vm_machine.base = 'hex'
                self.vm_machine.flavor = 'mips_mml'

            self.vm_machine.changes_init()

            data_check_errors = self.has_one_data_first(code)
            if data_check_errors:
                error_msg = {'name': 'error_msg',
                             'text': data_check_errors}
                self.send_response(self.iopub_socket, 'stream', error_msg)

            else:
                (last_instr, error, bit_code) = assemble(code, self.vm_machine,
                                                         web=False)
                if error == "":
                    vm_machine_info = {}
                    reg_info, mem_info, flag_info = self.parse_changes()
                    output = "Changes: <br />"
                    output += self.construct_table(reg_info, mem_info,
                                                   flag_info)
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
