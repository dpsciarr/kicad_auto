README

## KiCAD Project Builder

KiCAD Auto (KiCAD Project Builder) is a semi-automatic build tool for instantiating KiCAD projects. The tool takes in some basic project parameters from command line inputs, configures a title block, and creates a usable directory structure for a KiCAD project.

**NOTE:** *THIS HAS ONLY BEEN TESTED WITH THE FOLLOWING KICAD/OS VERSIONS:*

- KiCad Version: 5.1.5+dfsg1-2build2
- Platform: Linux 5.8.0-48-generic x86_64, 64 bit
    - Ubuntu 20.04.02

### Usage

Clone the repo using `git clone ...`. The directory structure that results looks like the following tree:

```
.
├── kicad_proj
│   ├── fp-lib-table
│   ├── libs
│   │   ├── footprints
│   │   │   └── temp.pretty
│   │   ├── models
│   │   └── symbols
│   │       ├── temp.dcm
│   │       └── temp.lib
│   ├── meta
│   │   └── info.html
│   ├── sym-lib-table
│   ├── temp.kicad_pcb
│   ├── temp.pro
│   ├── temp.sch
│   └── title_block.kicad_wks
├── kiproj.py
├── makefile
└── README.md
```

To build the project, run the command `make project`. You will prompted for some basic configuration parameters. What is entered will populate a file called `config.txt` which is generated after the command finished. The following parameters are needed:

1.  Project ID
    - Give your project a specific ID string or number. This will be what the .pro and other associated files will be called.
2.  Project Title
    - A title for your project. Maps to "Comment1" on title block.
3.  Project Subtitle
    - A brief descriptive subtitle. Maps to "Comment2" on title block.
4.  Project Revision
    - The revision of your project.
5.  Company Name
    - Your organization or company name. Could also be author name.

Once the parameters are populated, the program will build the directory structure and edit the corresponding KiCAD files. A successful run will result in a directory structure similar to below:

```
.
├── assembly_outputs
├── bom
│   └── bom_template.csv
├── config.txt
├── datasheets
├── docs
├── fab_outputs
├── freecad_outputs
├── images
├── kicad_proj
│   ├── fp-lib-table
│   ├── libs
│   │   ├── footprints
│   │   │   └── proj-id.pretty
│   │   ├── models
│   │   └── symbols
│   │       ├── proj-id.dcm
│   │       └── proj-id.lib
│   ├── meta
│   │   └── info.html
│   ├── proj-id.kicad_pcb
│   ├── proj-id.pro
│   ├── proj-id.sch
│   ├── sym-lib-table
│   └── title_block.kicad_wks
├── kiproj.py
├── makefile
├── pdf_outputs
├── README.md
└── software
```

### Cleaning

If you make a mistake entering the wrong information for the configuration you can reset the program to defaults using `make clean`. This will only work right after you create the project, DO NOT RUN `make clean` IF YOU HAVE STARTED WORKING ON THE PROJECT.

* * *

## Features

### Project Specific Libraries

Empty libraries for component symbols and footprints are automatically created and ready to use.

### Directory Structure

A ready-to-use directory structure is generated, able to carry beginner to intermediate (possibly even advanced!) KiCAD projects.

### BOM CSV

A basic CSV file is created with pre-defined headers corresponding to useful BOM fields. Open it with your favorite spreadsheet editor to manually track BOM items.

* * *

## Directory Structure

### Assembly Outputs

Pertinent files for assembly.

### BOM

Anything related to bill of materials.

### Datasheets

For storing datasheets.

### Docs

Documents that are specific to this project. Manuals, Diagrams, etc.

### Fab Outputs

For storing GERBERS and drill files.

### Freecad Outputs

For anything related to FreeCAD (may change in future version).

### Images

Images specific to this project.

### KiCAD Project

The entire KiCAD project sits in this directory (with the exception of global configuration and global library files).

### PDF Outputs

PDF drawings specific to this project, exported from either KiCAD or FreeCAD.

### Software

In case you need to program anything, here's a folder for software.

* * *