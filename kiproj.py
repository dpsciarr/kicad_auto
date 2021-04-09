import os
import sys
from datetime import datetime

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
kicad_proj_fp_lib_table = os.path.join(kicad_dir, "fp-lib-table")

today_date = datetime.today().strftime('%Y-%m-%d')

###############################################
# clean()
###############################################
def clean():
    if os.path.exists(config_file):
        project_name = "temp"
        project_title = ""

        with open(config_file, 'r') as cfg:
            lines = cfg.readlines()
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
        
        fp_pretty_dir = os.path.join(kicad_proj_fp_lib_dir, f"{project_name}.pretty")

        if project_name != "temp":
            print("Renaming files...")
            # Rename main application files
            os.rename(pro_file, os.path.join(kicad_dir, "temp.pro"))
            os.rename(sch_file, os.path.join(kicad_dir, "temp.sch"))
            os.rename(pcb_file, os.path.join(kicad_dir, "temp.kicad_pcb"))

            # Rename project symbol library files
            os.rename(symbol_lib_file, os.path.join(kicad_proj_symbols_lib_dir, "temp.lib"))
            os.rename(symbol_dcm_file, os.path.join(kicad_proj_symbols_lib_dir, "temp.dcm"))

            # Rename project .pretty folder
            os.rename(fp_pretty_dir, os.path.join(kicad_proj_fp_lib_dir, "temp.pretty"))

            print("Done")

        # Cleans schematic file (.sch)
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
        
        with open(os.path.join(kicad_dir, "temp.kicad_pcb"), 'r+') as pcb:
            pcb_contents = pcb.read()
            print("Cleaning pcb file...")
            lines = pcb_contents.split('\n')
            new_text = ""
            for line in lines:
                if line != "":
                    if "(title \"" in line:
                        new_text += "    (title \"PROJECT_TITLE\")\n"
                    elif "(date " in line:
                        new_text += "    (date DATE)\n"
                    elif "(rev " in line:
                        new_text += "    (rev REV)\n"
                    elif "(company " in line:
                        new_text += "    (company \"COMPANY\")\n"
                    elif "(comment 1 \"" in line:
                        new_text += "    (comment 1 \"COMMENT1\")\n"
                    elif "(comment 2 \"" in line:
                        new_text += "    (comment 2 \"COMMENT2\")\n"
                    elif "(comment 3 \"" in line:
                        new_text += "    (comment 3 \"COMMENT3\")\n"
                    elif "(comment 4 \"" in line:
                        new_text += "    (comment 4 \"COMMENT4\")\n"
                    else:
                        new_text += (line+"\n")
            pcb.seek(0)
            pcb.truncate(0)
            pcb.write(new_text)
            pcb.close()
            print("Done")
                    
        
        # Cleans symbol library table file
        with open(kicad_proj_sym_lib_table, 'r+') as slt:
            print("Cleaning symbol library table...")
            slt_contents = slt.read()
            slt_contents = slt_contents.replace(f"{project_name}", "PROJECT_NAME")
            slt_contents = slt_contents.replace(f"descr \"{project_title} Symbol Library\"", "descr \"\"")
            slt.seek(0)
            slt.truncate(0)
            slt.write(slt_contents)
            slt.close()
            print("Done")
        
        # Cleans footprint library table file
        with open(kicad_proj_fp_lib_table, 'r+') as flt:
            print("Cleaning footprint library table...")
            flt_contents = flt.read()
            flt_contents = flt_contents.replace(f"{project_name}", "PROJECT_NAME")
            flt_contents = flt_contents.replace(f"descr \"{project_title} Footprint Library\"", "descr \"\"")
            flt.seek(0)
            flt.truncate(0)
            flt.write(flt_contents)
            flt.close()
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
    pretty_dir = os.path.join(kicad_proj_fp_lib_dir, "temp.pretty")

    # Initialize project variables
    project_name = "temp"
    project_title = ""
    project_rev = ""
    project_company = ""
    project_comment1 = ""
    project_comment2 = ""
    project_comment3 = ""
    project_comment4 = ""

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
                                project_rev = val
                                sch_contents=sch_contents.replace("rev", val)
                            elif field == "COMPANY":
                                project_company = val
                                sch_contents=sch_contents.replace("company", val)
                            elif field == "COMMENT1":
                                project_comment1 = val
                                sch_contents=sch_contents.replace("comment1", val)
                            elif field == "COMMENT2":
                                project_comment2 = val
                                sch_contents=sch_contents.replace("comment2", val)
                            elif field == "COMMENT3":
                                project_comment3 = val
                                sch_contents=sch_contents.replace("comment3", val)
                            elif field == "COMMENT4":
                                project_comment4 = val
                                sch_contents=sch_contents.replace("comment4", val)
                            else:
                                sch_contents=sch_contents.replace("date", today_date)
                sch.seek(0)
                sch.truncate(0)
                sch.write(sch_contents)
                sch.close()
            cfg.close()
        print("Done")
    
    # Configures the .kicad_pcb file for Title Block population and page settings
    if os.path.exists(pcb_file):
        print("Configuring PCBNew file...")
        with open(pcb_file, 'r+') as pcb:
            pcb_contents = pcb.read()
            pcb_contents = pcb_contents.replace("PROJECT_TITLE", project_title)
            pcb_contents = pcb_contents.replace("DATE", today_date)
            pcb_contents = pcb_contents.replace("REV", project_rev)
            pcb_contents = pcb_contents.replace("COMPANY", project_company)
            pcb_contents = pcb_contents.replace("COMMENT1", project_comment1)
            pcb_contents = pcb_contents.replace("COMMENT2", project_comment2)
            pcb_contents = pcb_contents.replace("COMMENT3", project_comment3)
            pcb_contents = pcb_contents.replace("COMMENT4", project_comment4)
            
            pcb.seek(0)
            pcb.truncate(0)
            pcb.write(pcb_contents)
            pcb.close()
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

        print("Renaming .pretty")
        try:
            newPrettyDir = pretty_dir.replace("temp.pretty", f"{project_name}.pretty")
            os.rename(pretty_dir, newPrettyDir)
            print("Renamed:\nOLD:", pretty_dir, "\nNEW:", newPrettyDir)
        except Exception as e:
            print("Exception:", e)
        print("Done")
    
        # Update sym_lib_table
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
        
        # Update fp_lib_table
        if os.path.exists(kicad_proj_fp_lib_table):
            print(f"Updating footprint library table with project name {project_name}...")
            with open(kicad_proj_fp_lib_table, 'r+') as flt:
                flt_contents = flt.read()
                flt_contents = flt_contents.replace("PROJECT_NAME", project_name)
                flt_contents = flt_contents.replace("descr \"\"", f"descr \"{project_title} Footprint Library\"")
                flt.seek(0)
                flt.truncate(0)
                flt.write(flt_contents)
                flt.close()
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
    print("Please provide the following project parameters:\nProject ID, Title, Subtitle, Revision, and Company\n")
    project_id = input("Project ID: ")
    title = input("Title: ")
    subtitle1 = input("Subtitle: ")
    rev = input("Revision: ")
    company = input("Company Name: ")
    print("\n")

    with open(config_file, 'w') as cfg:
        cfg.write(f"PROJECT_NAME='{project_id}'\n")
        cfg.write(f"TITLE='{title}'\n")
        cfg.write(f"REV='{rev}'\n")
        cfg.write(f"COMPANY='{company}'\n")
        cfg.write(f"COMMENT1='{title}'\n")
        cfg.write(f"COMMENT2='{subtitle1}'\n")
        cfg.write("COMMENT3=''\n")
        cfg.write("COMMENT4=''\n")
        cfg.write(f"DATE='{today_date}'")
        
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