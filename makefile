# Need to export as ENV var
export TEMPLATE_DIR = templates
export QUIZ_DIR = templates

PTML_DIR = html_src
ADIR = ansible
SDIR = assembler
ODIR = Emu86/templates
MUDIR = myutils
UDIR = utils
TDIR = tests
SRCS = $(SDIR)/arithmetic.py $(SDIR)/control_flow.py $(SDIR)/data_mov.py $(SDIR)/interrupts.py 
INTER2 = $(ODIR)/help.ptml
OBJS = $(ODIR)/help.html
EXTR = $(UDIR)/extract_doc.awk
D2HTML = $(UDIR)/doc2html.awk
INCS = $(TEMPLATE_DIR)/head.txt $(TEMPLATE_DIR)/navbar.txt

HTML_FILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

ASM_FILES = $(shell ls $(TDIR)/*.asm)
ASM_PTMLS = $(shell ls $(TDIR)/*.asm | sed -e 's/.asm/.ptml/' | sed -e 's/tests/html_src/')

navbar:
	$(UDIR)/html_include.awk <$(TEMPLATE_DIR)/navbar.pre >$(TEMPLATE_DIR)/navbar.txt
	python3 write_sample_programs.py

# rule for making html files from ptml files:
%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UDIR)/html_checker.py $<
	$(UDIR)/html_include.awk <$< >$@
	git add $@

local: $(HTML_FILES)

# build sample asm web pages for project web site:
$(PTML_DIR)/%.ptml: $(TDIR)/%.asm
	$(MUDIR)/asm2ptml.awk $< >$@

samples: $(ASM_PTMLS)
	
# build the static website describing the project:
website: $(INCS) $(HTML_FILES) help
	-git commit -a 
	git pull origin master
	git push origin master

# build instruction help material from python source:
help: $(SRCS) samples
	python3 write_sample_programs.py
	$(EXTR) <$(SDIR)/parse.py | $(D2HTML) >$(TEMPLATE_DIR)/data.txt
	$(EXTR) <$(SDIR)/arithmetic.py | $(D2HTML) >$(TEMPLATE_DIR)/arithmetic.txt
	$(EXTR) <$(SDIR)/control_flow.py | $(D2HTML) >$(TEMPLATE_DIR)/control_flow.txt
	$(EXTR) <$(SDIR)/data_mov.py | $(D2HTML) >$(TEMPLATE_DIR)/data_mov.txt
	$(EXTR) <$(SDIR)/interrupts.py | $(D2HTML) >$(TEMPLATE_DIR)/interrupts.txt
	$(UDIR)/html_include.awk <$(ODIR)/help.ptml >$(ODIR)/help.html
	$(UDIR)/django2ptml.awk <$(ODIR)/help.html title="Language Description" >$(PTML_DIR)/help.ptml
	-git commit $(ODIR)/help.html

dev: $(SRCS) $(OBJS) 
	./all_tests.sh
	-git commit -a
	git push origin master
	ssh emu86@ssh.pythonanywhere.com 'cd /home/emu86/Emu86; /home/emu86/Emu86/myutils/dev.sh'

prod: $(SRCS) $(OBJ)
	./all_tests.sh
	git push origin master
	ssh gcallah@ssh.pythonanywhere.com 'cd /home/gcallah/Emu86; /home/gcallah/Emu86/myutils/prod.sh'
