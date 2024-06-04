class CodeWriter:
    def __init__(self,inputArr, fileName):
        # self.file = open(fileName.replace(".vm",".asm"), "w")
        self.fileName = fileName
        # self.outputFileName = inputFile.replace(".vm", ".asm")
        self.mathDict = {
            "add": "M=D+M",
            "sub": "M=M-D",
            "neg": "-M",
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT",
            "and": "M=D&M",
            "or": "M=D|M",
            "not": "!M"
        }
        self.addrDict = {
            "local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT", "temp": "R5"
        }
        self.line = ""
        self.arr = inputArr
        self.command = ""
        self.operation = ""
        self.arg1 = ""
        self.arg2 = ""
        # self.output = ["@256\nD=A\n@SP\nM=D\n@300\nD=A\n@LCL\nM=D\n@400\nD=A\n@ARG\nM=D\n@3000\nD=A\n"
        #                "@THIS\nM=D\n@3010\nD=A\n@THAT\nM=D"]
        self.output = []

        self.arrRaw = inputArr.copy()
        self.lineNum = 0
        self.writeCode()




    def writeArithmetic(self):
        getXandY = '@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\n'
        logAnswer = '@SP\nA=M-1\nM=D'
        localCommand = ""
        op = self.mathDict[self.arg1]
        if self.arg1 in ["gt", "lt", "eq"]:
            s = getXandY + f'D=M-D\n@TRUE{self.lineNum}\nD;{op}\nD=0\n@END{self.lineNum}\n0;JMP\n(TRUE{self.lineNum})\nD=-1\n(END{self.lineNum})\n'
            return s + logAnswer
        elif self.arg1 in ["add", "sub", "and", "or"]:
            return f'{getXandY}{op}' #D equal val from top of stack Address is 2nd from top
        else:
            return f'@SP\nA=M-1\nM={op}'
    # /TODO else
    def writePushPop(self):
        getDataAndIncrementStack = "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
        getDataFromStack = f'@SP\nM=M-1\nA=M\nD=M'
        if self.operation == "C_PUSH":
            if self.arg1 == "constant":
                return f'@{self.arg2}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1'
            else:
                s = ""
                if self.arg1 == "static":
                    print(self.fileName)
                    s = f'@{self.fileName.split("/")[-1].replace("vm","")}{self.arg2}'
                elif self.arg1 == "pointer":
                    if self.arg2 == "0":
                        s = "@THIS"
                    else:
                        s = "@THAT"
                    s = s + getDataAndIncrementStack
                    return s
                else:
                    if self.arg1 == "temp":
                        s = f'@{self.addrDict[self.arg1]}'
                    else:
                        s = f'@{self.addrDict[self.arg1]}\nA=M'
                    for i in range(int(self.arg2)):
                        s = s + f'\nA=A+1'
                s = s + getDataAndIncrementStack
                return s
        else:

            s = getDataFromStack
            if self.arg1 == "static":
                s = s + f'\n@{self.fileName.split("/")[-1].replace("vm","")}{self.arg2}\nM=D'
                return s
            if self.arg1 == "pointer":
                if self.arg2 == "0":
                    s = s + "\n@THIS\nM=D"
                else:
                    s = s + "\n@THAT\nM=D"
                return s
            else:
                s= s + f'\n@{self.addrDict[self.arg1]}'
                if self.arg1 != "temp":
                    s = s + "\nA=M"
                # s= f'@SP\nM=M-1\nA=M\nD=M\n@{self.addrDict[self.arg1]}\nA=M'
                for i in range(int(self.arg2)):
                    s = s + f'\nA=A+1'
                s = s + f'\nM=D'
                return s

    def writeCode(self):
        while len(self.arr) > 0:
            self.lineNum= self.lineNum + 1
            current = self.arr.pop(0)
            self.operation = current.split(" ")[0]
            if "//" in current:
                self.output.append(current)
            elif self.operation == "C_ARITHMETIC":
                self.arg1 = current.split(" ")[1]
                line = self.writeArithmetic()
                self.output.append(line)
            elif self.operation in ["C_PUSH", "C_POP"]:
                self.arg1, self.arg2 = current.split(" ")[1],current.split(" ")[2]
                line = self.writePushPop()
                self.output.append(line)
        # print(self.output)

        with open(self.fileName.replace(".vm", ".asm"), "w") as file:
            file.writelines("\n".join(self.output))
