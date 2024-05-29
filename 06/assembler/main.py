import os, glob
from location_table import location_table
from parser import instruction_parser

#=====================================
#    Hack Machine Assembler:
#       Place asm files in Input folder and run.
#       Output will appear in output folder.
#       Scroll down for troubleshooter if issue.
#



fName=""

for filename in glob.glob("Input/*.asm"):
    fName = os.path.basename(filename)
    with open(os.path.join(os.getcwd(), filename), 'r') as asm_file:
        asm = asm_file.read()

        lines = asm.split("\n")
        lines = [line for line in lines if "//" not in line]
        lines = [line.strip() for line in lines if line != ""]
        lines = [line.replace(" ", "") for line in lines]
        locations = []

        for line in lines:
            if "(" in line:
                location_table[line.replace("(","").replace(")","")] = ""

        locations = locations+[line[1:] for line in lines
                               if "@" in line and
                               "(" not in line and
                               ";" not in line and
                               not line.replace("@","").isdigit()]
        unique_locations = []
        for location in locations:
            if location not in unique_locations and location not in location_table:
                unique_locations.append(location)

        i = 16
        for location in unique_locations:
            if location not in location_table:
                location_table[location] = i
                i = i+1
        i = 0
        for line in lines:
            if "(" in line:
                location_table[line.replace("(","").replace(")","")] = i
            else:
                i= i+1
    #=====================================================
    # troubleshooter
    #     To Check Vals:
    #       Set troubleshoot to true
    #         options are
    #             unique_locations
    #             lines
    #             locations
    #             location_table

        printText = location_table
        troubleshoot = False
        raw=""
        if troubleshoot:
            for line in printText:
                raw = raw + line + "\n"

            with open("output/"+fName.replace("asm","txt"), "w") as output:
                output.write(raw)
    #=======================================================
        def to_bin(val, instruction = False):
            return '{0:016b}'.format(int(val))


        try:
            binaries = ""
            i = 0
            for line in lines:
                if "(" in line:
                    continue
                elif "@" in line:
                    if line.replace("@","").isdigit():
                        binaries = binaries + to_bin(line.replace("@","")) + "\n"
                    else:
                        var = line.replace("@","")
                        val = to_bin(location_table[var])
                        binaries = binaries + val + "\n"
                else:

                    binaries = binaries + instruction_parser(line) + "\n"
                i = i+1
        except:
            print(filename)

        with open("output/"+fName.replace("asm","hack"), "w") as output:
            output.write(binaries)
