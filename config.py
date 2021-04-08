import os

# Working Directory
pwd = os.path.dirname(os.path.realpath(__file__))

# Configuration File
config_file = os.path.join(pwd, "config.txt")

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


