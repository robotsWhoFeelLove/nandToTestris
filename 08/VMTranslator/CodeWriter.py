class CodeWriter:
    def __init__(self,inputArr, fileName):
        # self.file = open(fileName.replace(".vm",".asm"), "w")
        self.fileName = fileName
        # self.outputFileName = inputFile.replace(".vm", ".asm")
        self.functionName = "OS"
        self.labelCounter = 1
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




    def writeArithmetic(self, arg1):
        getXandY = '@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\n'
        logAnswer = '@SP\nA=M-1\nM=D'
        localCommand = ""
        op = self.mathDict[arg1]
        if arg1 in ["gt", "lt", "eq"]:
            s = getXandY + f'D=M-D\n@TRUE{self.lineNum}\nD;{op}\nD=0\n@END{self.lineNum}\n0;JMP\n(TRUE{self.lineNum})\nD=-1\n(END{self.lineNum})\n'
            return s + logAnswer
        elif arg1 in ["add", "sub", "and", "or"]:
            return f'{getXandY}{op}' #D equal val from top of stack Address is 2nd from top
        else:
            return f'@SP\nA=M-1\nM={op}'
    # /TODO else
    def writePushPop(self,operation, arg1, arg2):
        getDataAndIncrementStack = "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
        getDataFromStack = f'@SP\nM=M-1\nA=M\nD=M'
        if operation == "C_PUSH":
            if arg1 == "constant":
                return f'@{arg2}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1'
            else:
                s = ""
                if arg1 == "static":
                    s = f'@{self.fileName.split("/")[-1].replace("vm","")}{arg2}'
                elif arg1 == "pointer":
                    if arg2 == "0":
                        s = "@THIS"
                    else:
                        s = "@THAT"
                    s = s + getDataAndIncrementStack
                    return s
                else:
                    if arg1 == "temp":
                        s = f'@{self.addrDict[arg1]}'
                    else:
                        s = f'@{self.addrDict[arg1]}\nA=M'
                    for i in range(int(arg2)):
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

    def writeLabel(self,functionName, arg1):
        return f'({functionName}${arg1})'

    def writeGoto(self, functionName, arg1):
        return f'@{functionName}${arg1}\n0;JMP'

    def writeIf(self):
        return f'@SP\nM=M-1\nA=M\nD=M\n@{self.functionName}${self.arg1}\nD;JNE'


    def callFunction(self, functionName, arg1, arg2):

        label = f'{functionName}$ret.{self.labelCounter}'
        self.labelCounter = self.labelCounter + 1
        stackFrame = ""
        stackFrame = "\n".join([stackFrame + f'@{item}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1' for item in ["LCL","ARG","THIS","THAT"]])
        arg = f'@{5 + int(arg2)}\nD=A\n@SP\nD=M-D\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D' #check for issue
        goto = f'@{arg1}\n0;JMP'
        return f'@{label}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n{stackFrame}\n{arg}\n{goto}\n({label})'

    def writeFunction(self, functionName, arg1, arg2):
        # jumpOverFunction = f'@{functionName}${arg1}\n0;JMP\n'
        jump = f'({arg1})'
        # vars = '@SP\nD=A\nA=M\nM=D\n@SP\nM=M+1'
        vars = f'@0\nD=A\n@SP\nAM=M+1\nA=A-1\nM=D\n'
        nVars = ""
        for i in range(int(arg2)):
            nVars = nVars + "\n" + vars
        return jump + nVars

    def writeReturn(self):
        # self.labelCounter = self.labelCounter + 1
        endFrame = f'@LCL\nD=M\n@R13\nM=D\n'
        retAddress = f'@5\nA=D-A\nD=M\n@R14\nM=D\n'
        argPointer = f'@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n'
        repositionSP = f'@ARG\nD=M+1\n@SP\nM=D\n'
        that = f'@R13\nAM=M-1\nD=M\n@THAT\nM=D\n'
        this = f'@R13\nAM=M-1\nD=M\n@THIS\nM=D\n'
        arg = f'@R13\nAM=M-1\nD=M\n@ARG\nM=D\n'
        lcl = f'@R13\nAM=M-1\nD=M\n@LCL\nM=D\n'
        ret = f'@R14\nA=M\n0;JMP'
        # self.functionName = 'OS'
        # jumpOverAddress = f'({self.functionName}${self.arg1})'
        return endFrame + retAddress + argPointer + repositionSP + that + this + arg + lcl + ret


    def writeCode(self):
        while len(self.arr) > 0:
            self.lineNum = self.lineNum + 1
            current = self.arr.pop(0)
            self.operation = current.split(" ")[0]
            line = ""
            if "//" in current:
                line = current
            elif self.operation == "C_ARITHMETIC":
                self.arg1 = current.split(" ")[1]
                line = self.writeArithmetic(self.arg1)
                # self.output.append(line)
            elif self.operation in ["C_PUSH", "C_POP"]:
                self.arg1, self.arg2 = current.split(" ")[1],current.split(" ")[2]
                line = self.writePushPop(self.operation,self.arg1,self.arg2)
                # self.output.append(line)
            elif self.operation == "C_LABEL":
                self.arg1 = current.split(" ")[1]
                line = self.writeLabel(self.functionName, self.arg1)
            elif self.operation == "C_GOTO":
                self.arg1 = current.split(" ")[1]
                line = self.writeGoto(self.functionName, self.arg1)
            elif self.operation == "C_IF":
                self.arg1 = current.split(" ")[1]
                line = self.writeIf()
            elif self.operation == "C_CALL":
                self.arg1, self.arg2 = current.split(" ")[1], current.split(" ")[2]
                line = self.callFunction(self.functionName, self.arg1, self.arg2)
            elif self.operation == "C_FUNCTION":
                self.functionName, self.arg1 = current.split(" ")[1], current.split(" ")[2]
                line = self.writeFunction(self, self.functionName,self.arg1)
            elif self.operation == "C_RETURN":
                line = self.writeReturn()
            self.output.append(line)

