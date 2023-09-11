# This script parses a MySQL database source file and creates a public java
# class for every table in the database.
# Several assumptions have been made about the database and the sql file,
# so the script will probably need modification for different use cases.

import sys
from os.path import exists as file_exists

def formatattrname(name):
    temp = name.lower().split("_")
    return "".join([temp[0]] + [x.capitalize() for x in temp[1:]])

def yes_no_prompt(message):
    answer = input(message + " (y/n) ")
    while (answer not in ["",'y','n']):
        answer = input("y or n? ")
    if answer == 'n':
        print("Terminating...")
        sys.exit(0)

def create_file(entry, out_filename, import_date):
    out_lines = [f"package {package_name};\n\n"]
    if (import_date): out_lines.append("import java.util.Date;\n\n")
    out_lines.append(f"public class {entry[0]}" + " {\n\n")

    # Declarations
    for attr_name,attr_type in entry[3:]:
        out_lines.append(f"\tfinal {attr_type} {attr_name};\n")
    
    # Constructor
    out_lines.append(f"\n\tpublic {entry[0]}({entry[3][1]} {entry[3][0]}")
    for attr_name,attr_type in entry[4:]:
        out_lines.append(f",{attr_type} {attr_name}")
    out_lines.append(") {\n\t\tsuper();\n")
    for attr_name,_ in entry[3:]:
        out_lines.append(f"\t\tthis.{attr_name} = {attr_name};\n")
    out_lines.append("\t}\n\n")

    # Getters
    for attr_name,attr_type in entry[3:]:
        out_lines.append(f"\tpublic {attr_type} get{attr_name.capitalize()}() " +
                         '{\n\t\treturn ' + attr_name + ";\n\t}\n\n")
    
    out_lines.append("}")

    with open(out_filename,"w+") as outfile:
        outfile.write("".join(out_lines))


filename = input("Provide the filename: ")
while (not file_exists(filename)):
    filename = input("Error! No such file. Try again: ")
package_name = input("Provide the package name: ")

with open(filename) as f:
    lines = f.readlines()

entries = []
for lindex,line in enumerate(lines):
    if "DROP TABLE IF EXISTS " in line: entries.append([line.split("`")[1].capitalize(),lindex+2])
    if ") ENGINE=InnoDB " in line: entries[-1].append(lindex)

yes_no_prompt(f"Found {len(entries)} entries. Continue?")

for i,entry in enumerate(entries):
    print(f"Parsing entry #{i+1}...")
    import_entry = False
    for line in lines[entry[1]:entry[2]]:
        line = line.strip()
        
        # Skip lines that don't contain attributes
        if (line[0]!="`"): continue

        # Add name
        attr_name = formatattrname(line.split("`")[1])
        # Add type
        if ("int(" in line):
            attr_type = "Integer"
        elif ("char(" in line or " text " in line):
            attr_type = "String"
        elif (" date " in line or " datetime " in line):
            attr_type = "Date"
        else:
            attr_type = input(f"Encountered problem: Attribute with name {attr_name}.\nPlease specify type maually:")
        
        if attr_type == "Date": import_entry = True
        entry.append((attr_name,attr_type))
    print("Parsing complete! Found the following:")
    print(entry[3:])
    java_filn = entry[0] + ".java"
    yes_no_prompt(f'Create file "{java_filn}"?')
    create_file(entry,java_filn,import_entry)
    print("File created!\n================================================")