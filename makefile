SDIR = assembler
ODIR = Emu86/templates
UDIR = utils
SRCS = $(SDIR)/arithmetic.py $(SDIR)/control_flow.py $(SDIR)/data_mov.py $(SDIR)/interrupts.py 
INTER1 = $(ODIR)/arithmetic.txt $(ODIR)/control_flow.txt $(ODIR)/data_mov.txt $(ODIR)/interrupts.txt
INTER2 = $(ODIR)/help.ptml
OBJ = $(ODIR)/help.html

%.txt: %.py $(INCS)
	$(UDIR)/extract_doc.awk <$< | $(UDIR)/doc2html.awk >$@

dev: $(SRCS) $(OBJ)
	git checkout dev
	git commit -a -m "HTML rebuild."
	git push origin dev

prod: $(SRCS) $(OBJ)
	git checkout master
	git commit -a -m "HTML rebuild."
	git push origin master
