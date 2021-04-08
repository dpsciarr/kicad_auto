import os

# Working Directory
pwd = os.path.dirname(os.path.realpath(__file__))

# Configuration File
config_file = os.path.join(pwd, "config.txt")

# KiCAD-specific folders
kicad_dir = os.path.join(pwd, "kicad_proj/")



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
                cnt+=1
                if len(lines)!=cnt:
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
                        sch_contents=sch_contents.replace("comp", val)
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
