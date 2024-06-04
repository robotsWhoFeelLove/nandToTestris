import os
import sys

from CodeWriter import CodeWriter
from Parser import Parser



if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <input filename>")
    # output_file = input_file
    print(input_file)
    # fileName = input_file.split("/")[-1]
    # path = input_file.split("/")[:-1]
    # print(fileName)

p = Parser(input_file)
cw = CodeWriter(p.output, input_file)


