import re
import xml.dom.minidom


class Compiler:
    def __init__(self, file, fileName,test):
        self.runTests = test
        self.file_name = file
        self.file = []
        with open(file, "r") as f:
            [self.file.append(line.replace("\n","")) for line in f]
        self.lastStatement = ""
        self.current = self.file[0]
        self.index = 0

    def advance(self):
        if len(self.file) > self.index + 1:
            self.index = self.index+1
            self.current = self.file[self.index]
        else:
            self.current = "eof"

    def buildException(self, parent, dict):
        return f'Parent of type: {parent} expected child of type: {dict[parent]}, but received type: {self.current} instead'

    def compileClass(self):
        errors= {
            "none": "keyword class",
            "class": "class name",
            "className": " { "
        }
        result = ""
        parent = "none"
        while "{" not in self.current:
            if parent == "none" and "class" in self.current:
                result = result + "<class>" + self.current
                parent = "class"
                self.advance()
            elif parent == "class" and  re.search("> [A-Z].* <", self.current):
                result = result + self.current
                parent = "className"
                self.advance()
            else:
                return ""
        if "{" not in self.current:
            exception = self.buildException(parent, errors)
            raise Exception(exception)
        else:
            result = result + self.current
            self.advance()
            result = result + self.compileClassVarDecs() + self.compileSubroutines()
            if self.current == "<symbol> } </symbol>":
                result = result + self.current +"</class>"
                self.advance()
                return result
            else:
                raise Exception(f'Expected closing bracket for Class, but saw {self.current} at token index {self.index} in file {self.file_name}')

    def compileClassVarDecs(self):
        if not re.search("(field|static)", self.current):
            return ""
        s = "<classVarDec>"
        parent = "varDecs"
        while self.current != "<symbol> ; </symbol>":
            if parent == "varDecs" and re.search("(field|static)", self.current):
                s = s + self.current
                parent = "field"
            elif parent == "field" and re.search("(<keyword> (int|char|boolean)|<identifier> [A-Z])", self.current):
                s = s + self.current
                parent = "type"
            elif parent == "type" and re.search("<identifier>", self.current):
                s = s + self.current
                parent = "identifier"
            elif parent == "identifier" and re.search("<symbol> ,", self.current):
                s = s + self.current
                parent = "type"
            else:
                e = f'{self.current} is not a valid child of type: {parent}'
                raise Exception(e)
            self.advance()
        s = s + self.current + "</classVarDec>"
        self.advance()
        if not re.search("(field|static)", self.current):
            return s
        else:
            return s + self.compileClassVarDecs()

    def compileSubroutines(self):
        method = self.current
        mType = self.file[self.index + 1]
        mName = self.file[self.index + 2]
        s = ""
        if not re.search("(constructor|function|method)", self.current):
            print("No Constructor, methods or functions")
            return ""
        elif re.search("(constructor|function|method).*(int|char|boolean|void|<identifier> [A-Z]).*<identifier>", f'{method}{mType}{mName}'):
            s = f'<subroutineDec>{method}{mType}{mName}'
            self.advance()
            self.advance()
            self.advance()
            s = s + self.compileParameterList()

        if self.current != "<symbol> { </symbol>":
            raise Exception(f'Expected open bracket but saw {self.current} instead.')
        s = s + "<subroutineBody>"+self.current
        self.advance()
        s = s + self.compileVarDec()

        if re.search("(let|do|if|while|return)", self.current):
            s = s + "<statements>"
            s = s + self.compileStatements() + "</statements>"
        if self.current == "<symbol> } </symbol>":
            s = s + self.current
            self.advance()
        s = s + "</subroutineBody></subroutineDec>"
        if re.search("(function|method)", self.current):

            s = s + self.compileSubroutines()
        return s

    def compileVarDec(self):
        if self.current != "<keyword> var </keyword>":
            return ""
        s = "<varDec>"
        parent = "varDecs"
        while self.current != "<symbol> ; </symbol>":
            if parent == "varDecs" and re.search("var", self.current):
                s = s + self.current
                parent = "field"
            elif parent == "field" and re.search("(<keyword> (int|char|boolean)|<identifier> [A-Z])", self.current):
                s = s + self.current
                parent = "type"
            elif parent == "type" and re.search("<identifier>", self.current):
                s = s + self.current
                parent = "identifier"
            elif parent == "identifier" and re.search("<symbol> ,", self.current):
                s = s + self.current
                parent = "type"
            else:
                e = f'{self.current} is not a valid child of type: {parent}'
                raise Exception(e)
            self.advance()
        s = s + self.current + "</varDec>"
        self.advance()
        if not re.search("var", self.current):
            return s
        else:
            return s + self.compileVarDec()

    def compileStatements(self):
        s = ""
        if self.current == "<keyword> } <keyword>":
            return ""
        if self.current == "<keyword> let </keyword>":
            s = s + self.compileLetStatement()
        elif self.current == "<keyword> do </keyword>":
            s = s + self.compileDoStatement()
        elif self.current == "<keyword> while </keyword>":
            s = s + self.compileWhileStatement()
        elif self.current == "<keyword> if </keyword>":
            s = s + self.compileIfStatement()
        elif self.current == "<keyword> return </keyword>":
            s = s + self.compileReturnStatement()

        if re.search("<keyword> (let|while|do|if|return)", self.current):
            return s + self.compileStatements()
        else:
            return s

    def compileReturnStatement(self):
        s = "<returnStatement>" + self.current
        self.advance()
        if self.current == "<symbol> ; </symbol>":
            s = s + self.current
            self.advance()
            s = s + "</returnStatement>"
        else:
            s = s + self.compileExpression()
        if self.current == "<symbol> ; </symbol>":
            s = s + self.current
            self.advance()
            s = s + "</returnStatement>"
        return s

    def compileWhileStatement(self):
        s = "<whileStatement>" + self.current
        self.advance()
        if self.current == "<symbol> ( </symbol>":
            s = s + self.current
            self.advance()
        else:
            raise Exception(f'Expected open paranthesis in WHILE statement, but saw {self.current}')
        s = s + self.compileExpression()
        if self.current == "<symbol> ) </symbol>":
            s = s + self.current
            self.advance()
        else:
            raise Exception(f'Expected close Parenthesis in WHILE statement but saw {self.current}')
        if self.current == "<symbol> { </symbol>":
            s = s + self.current
            self.advance()
        else:
            raise Exception(f'Expected open bracket in WHILE statement but saw {self.current}')
        if re.search("(let|do|if|while|return)", self.current):
            s = s + "<statements>"
            s = s + self.compileStatements()
            s = s + "</statements>"
        if self.current == "<symbol> } </symbol>":
            s = s + self.current
            self.advance()
        else:
            raise Exception(f'Expected close bracket in IF statement but saw {self.current}')
        return s + "</whileStatement>"

    def compileIfStatement(self):
        s = "<ifStatement>" + self.current
        self.advance()
        if self.current == "<symbol> ( </symbol>":
            s = s + self.current
            self.advance()
        else:
            raise Exception(f'Expected open Parenthesis in IF statement but saw {self.current} at token index {self.index}')
        s = s + self.compileExpression()
        if self.current == "<symbol> ) </symbol>":
            s = s + self.current
            self.advance()
        else:
            raise Exception(f'Expected close Parenthesis in IF statement but saw {self.current} at token index {self.index}')
        if self.current == "<symbol> { </symbol>":
            s = s + self.current
            self.advance()
        else:
            raise Exception(f'Expected open bracket in IF statement but saw {self.current} at token index {self.index}')
        if re.search("(let|do|if|while|return)", self.current):
            s = s + "<statements>"
            s = s + self.compileStatements()
            s= s + "</statements>"
        if self.current == "<symbol> } </symbol>":
            s = s + self.current
            self.advance()
        else:
            raise Exception(f'Expected close bracket in IF statement but saw {self.current} at token index {self.index}')
        if not re.search(r"<keyword> else", self.current ):
            return s + "</ifStatement>"
        else:
            s = s + self.current
            self.advance()
            if self.current == "<symbol> { </symbol>":
                s = s + self.current
                self.advance()
            else:
                raise Exception(f'Expected open bracket in ELSE statement but saw {self.current}')
            if re.search("(let|do|if|while|return)", self.current):
                s = s + "<statements>"
                s = s + self.compileStatements()
                s = s + "</statements>"
            if self.current == "<symbol> } </symbol>":
                s = s + self.current
                self.advance()
                return s + "</ifStatement>"
            else:
                raise Exception(f'Expected close bracket in ELSE statement but saw {self.current}')

    def compileDoStatement(self):
        next = self.file[self.index +1]
        s = "<doStatement>" + self.current
        self.advance()
        if re.search(r"<identifier>.*<symbol> [(.]", self.current + self.file[self.index+1]):
            s = s + self.compileSubroutineCall()
        else:
            raise Exception(f'Expected subroutineCall, but saw {self.current + self.file[self.index+1]}' )
        if self.current != "<symbol> ; </symbol>":
            raise Exception(f'Expected end of do statement, but saw {self.current }')
        else:
            s = s + self.current + "</doStatement>"
        self.advance()
        return s


    def compileExpression(self): #one of
        next = self.file[self.index +1]
        s = "<expression>"
        s = s + self.compileTerm() + "</expression>"
        return s

    def compileSubroutineCall(self):
        next = self.file[self.index +1]
        if re.search(r"<identifier>.*<symbol> \(", self.current + next ):
            s = self.current
            self.advance()
            s = s + self.current
            self.advance()
            s = s + "<expressionList>" + self.compileExpressionList() + "</expressionList>" + self.current
            self.advance()
            return s
        elif re.search(r"<identifier>.*<symbol> \.", self.current + next):
            s = self.current
            self.advance()
            s = s + self.current
            self.advance()
            s = s + self.current
            self.advance()
            s = s + self.current
            self.advance()
            s = s +"<expressionList>" + self.compileExpressionList() + "</expressionList>" + self.current
            self.advance()
            return s


    def compileTerm(self): # one or more of
        next = self.file[self.index + 1]
        s = ""
        if re.search("(<keyword> (true|false|null|this)|<integerConstant>|<stringConstant>)", self.current):
            s = s + "<term>" + self.current + "</term>"
            self.advance()
        elif re.search(r"<identifier>.*<symbol> \[",self.current + self.file[self.index + 1]):
            s = s + "<term>" + self.current
            self.advance()
            s = s + self.current
            self.advance()
            s = s + self.compileExpression()
            if self.current != "<symbol> ] </symbol>":
                if re.search(r"<symbol> (\\+|-|&gt;|&lt;|&amp;|\*|/|\|)", self.current):
                    s = s + self.current
                    self.advance()
                else:
                    raise Exception(f"Unclosed bracket notation at token index {self.index}")
            if self.current == "<symbol> ] </symbol>":
                s = s + self.current + "</term>"
                self.advance()
        elif re.search(r"<identifier>.*<symbol> \(", self.current ):
            s = "<term>" + self.current
            self.advance() # issue with unadvanced line in next string
            s = s + self.current + "<expressionList>" + self.compileExpressionList() + "</expressionList>" + self.current + "</term>"
        elif re.search(r"<identifier>.*<symbol> \.", self.current + self.file[self.index + 1]):
            s = "<term>" + self.current #Class
            self.advance()
            s = s + self.current #.
            self.advance()
            s = s + self.current  # method
            self.advance()
            s = s + self.current #(
            self.advance()
            s = s + "<expressionList>" + self.compileExpressionList() + "</expressionList>" + self.current + "</term>"
            self.advance()


        elif re.search(r"<identifier> ", self.current):
            s = s + "<term>" + self.current + "</term>"
            self.advance()
        elif re.search(r"<symbol> [-~]", self.current ):
            s = "<term>" + self.current
            self.advance()
            s = s + self.compileTerm() + "</term>"
        elif self.current == "<symbol> ( </symbol>":
            s = s + "<term>" + self.current
            self.advance()
            s = s + self.compileExpression()
            # self.advance()
            if self.current == "<symbol> ) </symbol>":
                s = s + self.current
                self.advance()
                s = s + "</term>"
        if re.search(r"<symbol> (\+|-|&gt;|&lt;|&amp;|=|\*|/|\|)", self.current):
            s = s + self.current
            self.advance()
            s = s + self.compileTerm()
        return s

    def compileExpressionList(self):
        if self.current == "<symbol> ) </symbol>":
            return "\n "
        s = self.compileExpression()
        if self.current == "<symbol> , </symbol>":
            s = s + self.current
            self.advance()
            s = s + self.compileExpressionList()

        if self.current == "<symbol> ) </symbol>":

            return s
        else:
            raise Exception(f'Expected closing parenthesis or comma in expression List but saw {self.current} instead. at token index {self.index}')


    def compileLetStatement(self):
        s = "<letStatement>"+ self.current
        self.advance()
        if not re.search("<identifier>", self.current):
            raise Exception(f'Expected varName but saw {self.current} at token index {self.index}')
        s = s + self.current
        self.advance()
        if self.current == "<symbol> [ </symbol>":
            s = s + self.current
            self.advance()
            s = s + self.compileExpression() + self.current
            self.advance()
        if self.current != "<symbol> = </symbol>":
            raise Exception(f'Expected = operator but saw {self.current} at token index {self.index}')
        s = s + self.current
        self.advance()
        s = s + self.compileExpression()
        if self.current != "<symbol> ; </symbol>":
            raise Exception(f'Expected ; operator but saw {self.current} at token index {self.index}')
        s = s + self.current + "</letStatement>"
        self.advance()
        return s

    def compileParameterList(self):
        parent = "paramList"
        if self.current != "<symbol> ( </symbol>":
            raise Exception(f'Expected opening parenthesis, but saw {self.current} at token index {self.index}')
        s = self.current +"<parameterList>"
        self.advance()
        while self.current != "<symbol> ) </symbol>" and self.current != "eof": # prevent infinite loop
            if parent == "paramList" and re.search("(int|char|boolean|<identifier> [A-Z])", self.current):
                s = s + self.current
                parent = "type"
                self.advance()
            elif parent == "type" and re.search("<identifier> [A-Za-z]", self.current):
                s = s + self.current
                parent = "ident"
                self.advance()
            elif parent == "ident" and re.search("<symbol> ,", self.current):
                s = s + self.current
                parent = "paramList"
                self.advance()
        if s == "":
            s = "test" + "</parameterList>"  + self.current
        else:
            s = s  + "</parameterList>"+ self.current
        self.advance()
        return s


    def compileVarDecs(self):
        varDecs = ""
        parent = "varDecs"
        i = 0
        errors = {
            "varDecs": "varDec",
            "varDec": "Type or Class Name",
            "type": "identifier",
            "identifier": "comma or semicolon",
        }

        while not re.compile(r'<keyword> (do|let|if|\\})').search(self.current):
            if parent == "varDecs" and re.search("var", self.current):
                varDecs = varDecs + "<varDec>" + self.current
                parent = "varDec"
            elif parent == "varDec" and re.compile('(int|char|boolean|[A-Z]\\w*)').search(self.current):
                varDecs = varDecs + self.current
                parent = "type"
            elif parent == "type" and re.search("<identifier> [a-z]", self.current):
                varDecs = varDecs + self.current
                parent = "identifier"
            elif parent == "identifier" and re.search("<symbol> ,", self.current):
                varDecs = varDecs + self.current
                parent = "type"
            elif parent == "identifier" and re.search("<symbol> ;", self.current):
                varDecs = varDecs + self.current + "</varDec>"
                parent = "varDecs"
            else:
                exception = self.buildException(parent, errors)
                raise Exception(exception)
            self.advance()
        return varDecs

    def compile(self):
        output = self.compileClass()
        fn = self.file_name.replace(".tk", ".xml")
        tree = xml.dom.minidom.parseString(output)
        tree = tree.childNodes[0].toprettyxml()

        for line in tree:
            if "List> <" in line:
                line = line.replace("List> <","List>\n<")


        with open (fn, "w") as f:
            f.write(tree)






