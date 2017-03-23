ADIR = ansible
SDIR = assembler
ODIR = Emu86/templates
UDIR = utils
TDIR = tests
SRCS = $(SDIR)/arithmetic.py $(SDIR)/control_flow.py $(SDIR)/data_mov.py $(SDIR)/interrupts.py 
INTER1 = $(ODIR)/arithmetic.txt $(ODIR)/control_flow.txt $(ODIR)/data_mov.txt $(ODIR)/interrupts.txt
INTER2 = $(ODIR)/help.ptml
OBJ = $(ODIR)/help.html

help:
	extract_doc.awk <$(SDIR)/arithmetic.py | $(UDIR)/doc2html.awk >arithmetic.txt
	extract_doc.awk <$(SDIR)/control_flow.py | $(UDIR)/doc2html.awk >control_flow.txt
	extract_doc.awk <$(SDIR)/data_mov.py | $(UDIR)/doc2html.awk >data_mov.txt
	extract_doc.awk <$(SDIR)/interrupts.py | $(UDIR)/doc2html.awk >interrupts.txt
	html_include.awk <$(ODIR)/help.ptml >$(ODIR)/help.html

dev: $(SRCS) $(OBJ)
	git checkout dev
	$(TDIR)/test_assemble.py
	git commit -a -m "Building development."
	git push origin dev
	ssh emu86@ssh.pythonanywhere.com 'cd /home/emu86/Emu86; /home/emu86/Emu86/utils/dev.sh'

prod: $(SRCS) $(OBJ)
	git checkout master
	git merge dev
	$(TDIR)/test_assemble.py
	git push origin master
	ssh gcallah@ssh.pythonanywhere.com 'cd /home/gcallah/Emu86; /home/gcallah/Emu86/utils/prod.sh'
	git checkout dev

# for future use:
#	ansible-playbook -i $(ADIR)/inventories/hosts $(ADIR)/dev.yml
