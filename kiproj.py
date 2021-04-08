import os
import sys

# Working Directory
pwd = os.path.dirname(os.path.realpath(__file__))

# Config File
config_file = os.path.join(pwd, "config.txt")

# KiCAD Project Folder
kicad_dir = os.path.join(pwd, "kicad_proj/")

# KiCAD Project-Specific Symbols Library
kicad_proj_symbols_lib_dir = os.path.join(kicad_dir, "libs/symbols/")
kicad_proj_fp_lib_dir = os.path.join(kicad_dir, "libs/footprints/")
kicad_proj_models_lib_dir = os.path.join(kicad_dir, "libs/models/")
kicad_proj_sym_lib_table = os.path.join(kicad_dir, "sym-lib-table")

###############################################
# clean()
###############################################
def clean():
    if os.path.exists(config_file):
        project_name = "temp"
        project_title = ""

        with open(config_file, 'r') as cfg:
            lines = cfg.readlines()
            print(lines)
            proj_line = lines[0]
            project_name = proj_line.split("=")[1][1:-2]
            title_line = lines[1]
            project_title = title_line.split("=")[1][1:-2]
            cfg.close()
        
        # KiCAD specific files
        pro_file = os.path.join(kicad_dir, f"{project_name}.pro")
        sch_file = os.path.join(kicad_dir, f"{project_name}.sch")
        pcb_file = os.path.join(kicad_dir, f"{project_name}.kicad_pcb")
        
        symbol_lib_file = os.path.join(kicad_proj_symbols_lib_dir, f"{project_name}.lib")
        symbol_dcm_file = os.path.join(kicad_proj_symbols_lib_dir, f"{project_name}.dcm")

        if project_name != "temp":
            print("Renaming files...")
            os.rename(pro_file, os.path.join(kicad_dir, "temp.pro"))
            os.rename(sch_file, os.path.join(kicad_dir, "temp.sch"))
            os.rename(pcb_file, os.path.join(kicad_dir, "temp.kicad_pcb"))

            os.rename(symbol_lib_file, os.path.join(kicad_proj_symbols_lib_dir, "temp.lib"))
            os.rename(symbol_dcm_file, os.path.join(kicad_proj_symbols_lib_dir, "temp.dcm"))

            print("Done")

        with open(os.path.join(kicad_dir, "temp.sch"), 'r+') as sch:
            sch_contents = sch.read()
            print("Cleaning schematic file...")
            lines = sch_contents.split('\n')
            new_text = ""
            for line in lines:
                if line != "":
                    if "Title \"" in line:
                        new_text += "Title \"title\"\n"
                    elif "Date \"" in line:
                        new_text += "Date \"date\"\n"
                    elif "Rev \"" in line:
                        new_text += "Rev \"rev\"\n"
                    elif "Comp \"" in line:
                        new_text += "Comp \"company\"\n"
                    elif "Comment1 \"" in line:
                        new_text += "Comment1 \"comment1\"\n"
                    elif "Comment2 \"" in line:
                        new_text += "Comment2 \"comment2\"\n"
                    elif "Comment3 \"" in line:
                        new_text += "Comment3 \"comment3\"\n"
                    elif "Comment4 \"" in line:
                        new_text += "Comment4 \"comment4\"\n"
                    else:
                        new_text += (line+"\n")
            
            sch.seek(0)
            sch.truncate(0)
            sch.write(new_text)
            sch.close()
            print("Done")
        
        with open(kicad_proj_sym_lib_table, 'r+') as slt:
            print("Cleaning Symbol Library Table")
            slt_contents = slt.read()
            slt_contents = slt_contents.replace("" + project_name, "PROJECT_NAME")
            slt_contents = slt_contents.replace(f"descr \"{project_title} Symbol Library\"", "descr \"\"")
            slt.seek(0)
            slt.truncate(0)
            slt.write(slt_contents)
            slt.close()
            print("Done")


###############################################
# setup()
###############################################
def setup():
    # BOM file
    bom_file = os.path.join(pwd, "bom/bom_template.csv")

    # Creating relevant KiCad paths
    pro_file = os.path.join(kicad_dir, "temp.pro")
    sch_file = os.path.join(kicad_dir, "temp.sch")
    pcb_file = os.path.join(kicad_dir, "temp.kicad_pcb")

    # Initialize project name
    project_name = "temp"
    project_title = ""

    # Configures the .sch file for Title Block population and page settings
    if os.path.exists(sch_file):
        print("Configuring EESchema file...")
        with open(config_file, 'r') as cfg:
            cfg_contents = cfg.read()
        
            lines = cfg_contents.split("\n")
            cnt=0
            with open(sch_file, 'r+') as sch:
                sch_contents = sch.read()
                for line in lines:
                    cnt += 1
                    if line != "":
                        if len(lines) >= cnt:
                            attr = line.split("=")
                            field = attr[0]
                            val = attr[1][1:-1]

                            if field == "PROJECT_NAME" and val != "":
                                project_name = val
                            elif field == "TITLE":
                                project_title = val
                                sch_contents=sch_contents.replace("title", val)
                            elif field == "REV":
                                sch_contents=sch_contents.replace("rev", val)
                            elif field == "COMPANY":
                                sch_contents=sch_contents.replace("company", val)
                            elif field == "COMMENT1":
                                sch_contents=sch_contents.replace("comment1", val)
                            elif field == "COMMENT2":
                                sch_contents=sch_contents.replace("comment2", val)
                            elif field == "COMMENT3":
                                sch_contents=sch_contents.replace("comment3", val)
                            elif field == "COMMENT4":
                                sch_contents=sch_contents.replace("comment4", val)
                            elif field == "DATE":
                                sch_contents=sch_contents.replace("date", val)
                sch.seek(0)
                sch.truncate(0)
                sch.write(sch_contents)
                sch.close()
            cfg.close()
        print("Done")

    # Renames project and library folders if renamed by configuration file
    if project_name != "temp":
        print("Renaming project files...")
        for f in os.listdir(kicad_dir):
            if f[:4] == "temp":
                fsplit = f.split(".")
                newName = os.path.join(kicad_dir, project_name + "." + fsplit[1])
                try:
                    os.rename(os.path.join(kicad_dir, f), newName)
                    print("Renamed:\nOLD:", os.path.join(kicad_dir, f), "\nNEW:", newName)
                except Exception as e:
                    print("Exception:", e)

        print("Done")    
        print("Renaming library files...")
        for f in os.listdir(kicad_proj_symbols_lib_dir):
            if f[:4] == "temp":
                fsplit = f.split(".")
                newName = os.path.join(kicad_proj_symbols_lib_dir, project_name + "." + fsplit[1])
                try:
                    os.rename(os.path.join(kicad_proj_symbols_lib_dir, f), newName)
                    print("Renamed:\nOLD:", os.path.join(kicad_proj_symbols_lib_dir, f), "\nNEW:", newName)
                except Exception as e:
                    print("Exception:", e)

        print("Done")
    
        # Update sym_lib_table
        print(kicad_proj_sym_lib_table)
        if os.path.exists(kicad_proj_sym_lib_table):
            print(f"Updating symbol library table with project name {project_name}...")
            with open(kicad_proj_sym_lib_table, 'r+') as slt:
                slt_contents = slt.read()
                slt_contents = slt_contents.replace("PROJECT_NAME", project_name)
                slt_contents = slt_contents.replace("descr \"\"", f"descr \"{project_title} Symbol Library\"")
                slt.seek(0)
                slt.truncate(0)
                slt.write(slt_contents)
                slt.close()
            print("Done")


    # Initializes a BOM CSV with basic headers to be opened in your favorite spreadsheet editor
    if os.path.exists(bom_file):
        print("Initializing BOM Template")
        with open(bom_file, 'w') as bom:
            bom.write("Item #,Designator,Qty.,Description,Manufacturer,Mfr Part Number")
            bom.close()
        print("Done")

###############################################
# config()
###############################################
def config():
    project_name = "P-001" #input("Project Name: ")
    title = "PROTIS 1" #input("Title: ")
    rev = "0" #input("Revision: ")
    company = "Mimmotronics" #input("Company Name: ")
    sheet1 = "Overview" #input("Sheet 1: ")
    date = "2021-04-08" #input("Date (YYYY-MM-DD): ")

    with open(config_file, 'w') as cfg:
        cfg.write(f"PROJECT_NAME='{project_name}'\n")
        cfg.write(f"TITLE='{title}'\n")
        cfg.write(f"REV='{rev}'\n")
        cfg.write(f"COMPANY='{company}'\n")
        cfg.write(f"COMMENT1='{title}'\n")
        cfg.write(f"COMMENT2='{sheet1}'\n")
        cfg.write("COMMENT3=''\n")
        cfg.write("COMMENT4=''\n")
        cfg.write(f"DATE='{date}'")
        
        cfg.close()




EXPECTED_ARGC = 2
ERR_ARG_NUM = f"\
Takes 1 argument, {len(sys.argv)-1} given.\nArgument must be 'clean', 'config' or 'setup'."

if (EXPECTED_ARGC > len(sys.argv)):
    print(ERR_ARG_NUM)
elif (len(sys.argv) > EXPECTED_ARGC):
    print(ERR_ARG_NUM)
else:
    if sys.argv[1] == 'clean':
        clean()
    elif sys.argv[1] == 'setup':
        setup()
    elif sys.argv[1] == 'config':
        config()
    else:
        print("Invalid argument.\nArgument must be 'clean', 'config', or 'setup'.")