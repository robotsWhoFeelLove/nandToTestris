from CompilationEngine import Compiler
from tokenizer import Tokenizer
import sys, os, glob, re

jack = ".jack$"
def get_files(args):
    """
    :param args: the arguments given to the program.
    :return: the list of paths to .jack files
    """
    list_of_files_path = []
    if len(args) == 2:
        if os.path.isfile(args[1]) and ".jack" in args[1]:
            list_of_files_path.append(args[1])
        elif os.path.isdir(args[1]):
            for file in os.listdir(args[1]):
                if re.compile(".*\\.jack$").match(file):
                    list_of_files_path.append(args[1] + "/" + file)
        return list_of_files_path
    else:
        print("input is invalid")
        exit()

test = False
try:
    input_directory = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "-t":
        test = True
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <input directory")
fPaths =get_files(sys.argv)

for file in fPaths:
    print(file)
    t = Tokenizer(file)
    t.tokenize()
    fn = file.replace(".jack",".tk")
    with open(f'{fn}', "w") as out:
        [out.writelines(line + "\n") for line in t.output]
    c = Compiler(f'{fn}', file, test)
    tree = c.compile()





