import sys
import logger as log
from token import TokenType

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
        self.state.consts[name] = int(value)

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

    def get_src_value(self, src_tokens):
        if src_tokens[0].type == TokenType.BP:
            offset = 0
            if len(src_tokens) > 1:
                offset = int(src_tokens[2].text)
            src = self.state.index(self.state.bp + offset)
        elif src_tokens[0].type == TokenType.SP:
            offset = 0
            if len(src_tokens) > 1:
                offset = int(src_tokens[2].text)
            src = self.state.index(self.state.sp + offset)
        elif src_tokens[0].type == TokenType.ASTERISK:
            src = self.state.index(self.get_src_value(src_tokens[1:]))
        else:
            src = self.get_primary_value(src_tokens[0])
        return src

    def get_dst_index(self, dst_tokens):
        if dst_tokens[0].type == TokenType.BP:
            index = self.state.bp + int(dst_tokens[2].text)
        elif dst_tokens[0].type == TokenType.SP:
            index = self.state.sp + int(dst_tokens[2].text)
        elif dst_tokens[0].type == TokenType.ASTERISK:
            index = self.get_src_value(dst_tokens[1:])
        return index

    def get_primary_value(self, token):
        if token.type == TokenType.ACC:
            value = self.state.acc
        elif token.type == TokenType.NIL:
            value = 0
        elif token.type == TokenType.NUMBER:
            value = int(token.text)
        elif token.type == TokenType.IDENT:
            value = self.consts[token.text]
        return value

    def limit(self, number):
        if number > 999:
            return 999
        if number < -999:
            return -999
        return number

    def run(self):
        self.instructions.append(Instruction("NOP", None, None))

        # TODO
        i_num = 0
        while i_num < len(self.instructions):
            self.state.line = self.instructions[i_num].line

            i_name = self.instructions[i_num].name
            i_params = self.instructions[i_num].params

            # mov src, dst
            if i_name == TokenType.MOV.name:
                src = self.get_src_value(i_params["src"])

                if i_params["dst"][0].type == TokenType.ACC:
                    self.state.acc = self.limit(src)
                elif i_params["dst"][0].type == TokenType.BP and len(i_params["dst"]) == 1:
                    self.state.bp = src
                elif i_params["dst"][0].type == TokenType.SP and len(i_params["dst"]) == 1:
                    self.state.sp = src
                else:
                    dst = self.get_dst_index(i_params["dst"])
                    self.state.insert(dst, self.limit(src))

            elif i_name == TokenType.SWP.name:
                tmp = self.state.acc
                self.state.acc = self.state.bak
                self.state.bak = tmp

            elif i_name == TokenType.SAV.name:
                self.state.bak = self.state.acc

            i_num += 1
