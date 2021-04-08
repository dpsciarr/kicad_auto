PYTHON = python3

.PHONY = setup clean

setup:
	mkdir assembly_outputs
	mkdir bom
	mkdir datasheets
	mkdir docs
	mkdir fab_outputs
	mkdir freecad_proj
	mkdir images
	mkdir pdf_outputs
	mkdir software

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


