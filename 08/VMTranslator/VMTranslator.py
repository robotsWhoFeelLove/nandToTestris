import os
import glob
import sys
from Bootstrap import bootstrap
from CodeWriter import CodeWriter
from Parser import Parser



if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <input filename>")
    print(input_file)
    outputs = []
    if ".vm" not in input_file:
        os.chdir(input_file)
        path = os.path.abspath("")
        globs = glob.glob("*.vm")
        for file in globs:
            p = Parser(file)
            cw = CodeWriter(p.output, file)
            outputs = outputs + cw.output
        if "//function Sys.init 0" in outputs:
                outputs.insert(0, bootstrap)
        print(outputs)
        with open(f'{path}/{path.split("/")[-1]}.asm', "w") as file:
            file.writelines("\n".join(outputs))
    else:
        p = Parser(input_file)
        cw = CodeWriter(p.output, input_file)
        outputs = cw.output
        for line in outputs:
            if line == "function Sys.init 0":
                print("found sys")
            if "Sys.init" in line:
                outputs.insert(0, "@256\nD=A\n@SP\nM=D\n@Sys.init\n0;JMP")
        print(outputs)
        with open(f'{input_file.replace(".vm",".asm")}', "w") as file:
            file.writelines("\n".join(outputs))

