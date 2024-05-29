def instruction_parser(ins):
    jump = ""

    if ";" in ins:
        ins, jump = ins.split(";")
    match jump:
        case "JGT":
            jump = "001"
        case "JEQ":
            jump = "010"
        case "JGE":
            jump = "011"
        case "JLT":
            jump = "100"
        case "JNE":
            jump = "101"
        case "JLE":
            jump = "110"
        case "JMP":
            jump = "111"
        case _:
            jump = "000"

    dest = ""
    if "=" in ins:
        dest, ins =ins.split("=")

    match dest:
        case "":
            dest = "000"
        case "M":
            dest = "001"
        case "D":
            dest = "010"
        case "DM":
            dest = "011"
        case "MD":
            dest = "011"
        case "A":
            dest = "100"
        case "AM":
            dest = "101"
        case "MA":
            dest = "101"
        case "AD":
            dest = "110"
        case "DA":
            dest = "110"
        case "ADM":
            dest = "001"

    match ins:
        case "0":
            ins = "1110101010"
        case "1":
            ins = "1110111111"
        case "-1":
            ins = "1110111010"
        case "D":
            ins = "1110001100"
        case "A":
            ins = "1110110000"
        case "!D":
            ins = "1110001101"
        case "!A":
            ins = "1110110001"
        case "-D":
            ins = "1110001111"
        case "-A":
            ins = "1110110011"
        case "D+1":
            ins = "1110011111"
        case "A+1":
            ins = "1110110111"
        case "D-1":
            ins = "1110001110"
        case "A-1":
            ins = "1110110010"
        case "D+A":
            ins = "1110000010"
        case "D-A":
            ins = "1110010011"
        case "A-D":
            ins = "1110000111"
        case "D&A":
            ins = "1110000000"
        case "D|A":
            ins = "1110010101"
        case "M":
            ins = "1111110000"
        case "!M":
            ins = "1111110001"
        case "-M":
            ins = "1111110011"
        case "M+1":
            ins = "1111110111"
        case "M-1":
            ins = "1111110010"
        case "D+M":
            ins = "1111000010"
        case "D-M":
            ins = "1111010011"
        case "M-D":
            ins = "1111000111"
        case "D&M":
            ins = "1111000000"
        case "D|M":
            ins = "1111010101"
    return ins + dest + jump
