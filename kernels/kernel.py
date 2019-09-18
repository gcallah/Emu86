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
        'file_extension': '.txt',
    }

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        intel_machine = IntelMachine()
        intel_machine.base = 'dec'
        intel_machine.flavor = 'intel'
        (last_instr, error, bit_code) = assemble(code, intel_machine)
        if not error:
            result = {'name': 'return_value', 'text': intel_machine.registers}
            self.send_response(self.iopub_socket, 'result', result)
        else:
            self.send_response(self.iopub_socket, 'result', error)
        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}
                }
