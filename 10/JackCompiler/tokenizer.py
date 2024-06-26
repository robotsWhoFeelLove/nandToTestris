import re


class Tokenizer:
    def __init__(self, file):
        self.symbols = re.compile(r'[{}()\[\],+\\|*&<>=~/;.-]')
        self.stringConst = re.compile(r'".*"')
        self.file_name = file
        self.keywords = re.compile(
            r'(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)')
        self.text = []
        # print(file)
        with open(file, "r") as f:
            self.text = f.read()
            # print(self.text)

        self.output = []

    def addTags(self, tag, regEx, text):

        matches = regEx.finditer(text)
        offset = 0
        newText = text
        lenOfTags = (len(tag) * 2) + 7 + 2
        # newText = text.strip()
        for match in matches:
            span = match.span()
            if tag == "keyword" and newText[span[0]-1 + offset].isalpha():
                # print (newText[span[0]-1])
                # print(newText[span[0] + offset:span[1] + offset])
                continue
            else:
                newText = newText[:span[0] + offset] + f' <{tag}>' + "\r" + newText[span[0]  + offset:span[
                                                                                              1] + offset].replace(" ","\r") + "\r" + f'</{tag}> ' + newText[
                                                                                                                            span[
                                                                                                                                1] + offset:]
            offset = offset + lenOfTags
        return newText

    def tokenize(self):

        self.text = re.sub('//.*\n',"", self.text)
        # self.text = re.sub('(/\\*\\*).*\n', "", self.text)

        self.text = re.sub(r'/\*\*.*?\*/', '', self.text, flags=re.DOTALL)
        # print(self.text)
        # self.text = self.text.replace(r'/\*\*.*', "")

        text = self.addTags("symbol", self.symbols, self.text)
        text = self.addTags("stringConstant", self.stringConst, text)
        # print(text)
        text = self.addTags("keyword", self.keywords, text)

        tokens = text.strip().replace("\n", "").split(" ")
        tokens = [val.replace("\r"," ").replace('"',"") for val in tokens if val not in ["", "\n"]]

        results = []
        for token in tokens:
            if "</" not in token and '"' not in token and not token.isspace():
                if token.isdigit():
                    results.append(f'<integerConstant> {token} </integerConstant>')
                else:
                    results.append(f'<identifier> {token} </identifier>')
            elif not token.isspace():
                results.append(token)
            # print(token)


        self.output = [line.replace("<symbol> > </symbol>","<symbol> &gt; </symbol>").replace("<symbol> < </symbol>","<symbol> &lt; </symbol>")
                       .replace("<symbol> & </symbol>","<symbol> &amp; </symbol>",) for line in results]
        # print("output",self.output)

