class Parser:
    def __init__(self, fileName):
        with open(fileName, "r") as vm:
            self.vm = vm
            self.inputs = [line.strip() for line in self.vm if line != "\n"]
            self.fileName = fileName
            self.line = ""
            self.command = ""
            self.type = ""
            self.argument1 = ""
            self.argument2 = ""
            self.output = []
            self.cmDict = {
                            "add": "C_ARITHMETIC",
                            "sub": "C_ARITHMETIC",
                            "neg": "C_ARITHMETIC",
                            "eq": "C_ARITHMETIC",
                            "gt": "C_ARITHMETIC",
                            "lt": "C_ARITHMETIC",
                            "and": "C_ARITHMETIC",
                            "or": "C_ARITHMETIC",
                            "not": "C_ARITHMETIC",
                            "push": "C_PUSH",
                            "pop": "C_POP",
                            "function": "C_FUNCTION",
                            "label": "C_LABEL",
                            "goto": "C_GOTO",
                            "if": "C_IF",
                            "return": "C_RETURN",
                            "call": "C_CALL"
            }
            self.addrDict = {
                "local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT", "temp": "TEMP"
            }
            self.parse()



    # def hasMoreLines(self):
    #     # print(self.inputs)
    #     if len(self.inputs) > 0:
    #         return True
    #     else:
    #         return False

    def advance(self):
        self.line = self.line.replace("\n", "").strip()
        if self.line and "//" not in self.line and self.line != '\n':
            self.command = self.line
            self.commandType()
            return self.command
        else:
            return False


    def commandType(self):
        temp = self.command.split(" ")[0]
        self.type = self.cmDict[temp]
        return self.type

    def arg1(self):
        if self.type == "C_ARITHMETIC":
            self.argument1 = self.command.split(" ")[0]
            return self.argument1
        else:
            self.argument1 = self.command.split(" ")[1]
            return self.argument1

    def arg2(self):
        if self.type == "C_ARITHMETIC":
            self.argument2 = ""
            return self.argument2
        else:
            self.argument2 = self.command.split(" ")[2]
            return self.argument2

    def parse(self):
        for line in self.inputs:
            if "//" in line:
                continue
            else:
                self.line = line
                self.advance()
                arg1 = self.arg1().replace("\n","")
                arg2 = self.arg2().replace("\n","")
                self.output.append(f'//{self.command}')
                prefix = f'{self.type} {arg1}'
                if arg2:
                    prefix = prefix + f' {arg2}'
                self.output.append(prefix)


        return self.output
