import sys
import logger as log

class Instruction:
    def __init__(self, name, params, line):
        self.name = name
        self.params = params
        self.line = line


class Eval:
    def __init__(self, state):
        self.instructions = []
        self.state = state
        self.tmp_instruction = None
        self.tmp_argument = None

    def add_label(self, name, line):
        if name in self.state.labels:
            log.error(f"label {name} already exists", line)
        self.state.labels[name] = len(self.instructions)

    def add_const(self, name, value, line):
        if name in self.state.consts:
            log.warning("{name} already defined", line)
            return
        self.state.consts[name] = value

    def add_instruction(self, name, line):
        self.tmp_instruction = Instruction(name, {}, line)

    def add_argument(self, argument):
        self.tmp_argument = []
        self.tmp_argument.append(argument)

    def argument_append(self, part):
        self.tmp_argument.append(part)

    def argument_done(self, name):
        self.tmp_instruction.params[name] = self.tmp_argument

    def instruction_done(self):
        self.instructions.append(self.tmp_instruction)

    def run(self):
        self.instructions.append(Instruction("NOP", None, None))

        # TODO
