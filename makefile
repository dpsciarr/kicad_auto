PYTHON = python3

.PHONY = setup config clean

setup:
	mkdir assembly_outputs
	mkdir bom
	touch bom/bom_template.csv
	mkdir datasheets
	mkdir docs
	mkdir fab_outputs
	mkdir freecad_proj
	mkdir images
	mkdir pdf_outputs
	mkdir software
	$(PYTHON) setup.py

config:
	$(PYTHON) config.py

clean:
	rm -r assembly_outputs
	rm -r bom
	rm -r datasheets
	rm -r docs
	rm -r fab_outputs
	rm -r freecad_proj
	rm -r images
	rm -r pdf_outputs
	rm -r software
	rm config.txt


