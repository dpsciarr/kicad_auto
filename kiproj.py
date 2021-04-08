import os
import sys

# Working Directory
pwd = os.path.dirname(os.path.realpath(__file__))

# Config File
config_file = os.path.join(pwd, "config.txt")

# KiCAD Project Folder
kicad_dir = os.path.join(pwd, "kicad_proj/")

bom_file = os.path.join(pwd, "bom/bom_template.csv")

###############################################
# clean()
###############################################
def clean():
    if os.path.exists(config_file):
        proj_name = "temp"

        with open(config_file, 'r') as cfg:
            proj_line = cfg.readlines(1)[0]
            proj_name = proj_line.split("=")[1][1:-2]
            
            cfg.close()
        
        # KiCAD specific folders
        pro_file = os.path.join(kicad_dir, f"{proj_name}.pro")
        sch_file = os.path.join(kicad_dir, f"{proj_name}.sch")
        pcb_file = os.path.join(kicad_dir, f"{proj_name}.kicad_pcb")
        
        if proj_name != "temp":
            print("Renaming folders...")
            os.rename(pro_file, os.path.join(kicad_dir, "temp.pro"))
            os.rename(sch_file, os.path.join(kicad_dir, "temp.sch"))
            os.rename(pcb_file, os.path.join(kicad_dir, "temp.kicad_pcb"))

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

###############################################
# setup()
###############################################
def setup():
    # BOM file
    bom_file = os.path.join(pwd, "bom/bom_template.csv")

    pro_file = os.path.join(kicad_dir, "temp.pro")
    sch_file = os.path.join(kicad_dir, "temp.sch")
    pcb_file = os.path.join(kicad_dir, "temp.kicad_pcb")

    project_name = "temp"

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


    if project_name != "temp":
        print("Renaming project files...")
        for f in os.listdir(kicad_dir):
            if f[:4] == "temp":
                fsplit = f.split(".")
                newName = os.path.join(kicad_dir, project_name + "." + fsplit[1])
                try:
                    os.rename(os.path.join(kicad_dir, f), newName)
                    print("Renamed:\n\t", os.path.join(kicad_dir, f), " to ", newName)
                except Exception as e:
                    print("Exception:", e)
        print("Done")


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
    project_name = input("Project Name: ")
    title = input("Title: ")
    rev = input("Revision: ")
    company = input("Company Name: ")
    sheet1 = input("Sheet 1: ")
    date = input("Date (YYYY-MM-DD): ")

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