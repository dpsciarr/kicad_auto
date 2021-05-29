PYTHON = python3

FOLDERS = assembly_outputs bom datasheets docs fab_outputs freecad_outputs images pdf_outputs simulation software

.PHONY = project clean

project:
	$(PYTHON) kiproj.py config
	mkdir $(FOLDERS)
	touch bom/bom_template.csv
	$(PYTHON) kiproj.py setup

clean:
	rm -r $(FOLDERS)
	$(PYTHON) kiproj.py clean
	rm config.txt
