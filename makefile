# Need to export as ENV var
export TEMPLATE_DIR = templates
export QUIZ_DIR = templates

PTML_DIR = html_src
ADIR = ansible
SDIR = assembler
INTEL_DIR = $(SDIR)/Intel
MIPS_DIR = $(SDIR)/MIPS
RISCV_DIR = $(SDIR)/RISCV
WASM_DIR = $(SDIR)/WASM
EMUDIR = Emu86
REPO = emu86
ODIR = $(EMUDIR)/templates
MUDIR = myutils
MODELS_DIR = models
UDIR = utils
TDIR = tests
SRCS = $(INTEL_DIR)/arithmetic.py $(INTEL_DIR)/control_flow.py $(INTEL_DIR)/data_mov.py $(INTEL_DIR)/interrupts.py 
MIPS_SRCS = $(MIPS_DIR)/arithmetic.py $(MIPS_DIR)/control_flow.py $(MIPS_DIR)/data_mov.py $(MIPS_DIR)/interrupts.py 
INTER2 = $(ODIR)/help.ptml
OBJS = $(ODIR)/help.html
EXTR = $(UDIR)/extract_doc.awk
D2HTML = $(UDIR)/doc2html.awk
INCS = $(TEMPLATE_DIR)/head.txt $(TEMPLATE_DIR)/navbar.txt
DOCKER_DIR = docker
REQ_DIR = $(DOCKER_DIR)
PYLINT = flake8
PYLINTFLAGS = 
PYTHONFILES = $(shell find . -type f -name "*.py" -not -path "./utils/*" -not -path "./Emu86/migrations/*" -not -path "./mysite/*")
PYTESTFILES = pytests

ESLINT = npx eslint
JSFILES = $(shell ls mysite/static/Emu86/*.js)

HTML_FILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

ASM_FILES = $(shell ls $(TDIR)/*/*.asm)
ASM_PTMLS = $(shell find ./$(TDIR)/tests_Intel -type f -name "*.asm" -not -path "./$(TDIR)/tests_Intel/fp*" -not -path "./$(TDIR)/tests_Intel/sieve*" | sed -e 's/.asm/.ptml/' | sed -e 's/tests\/tests_Intel\//html_src\//')

FORCE:

# update our submodules:
submods: FORCE
	git submodule foreach --recursive git pull origin master

# this rule builds the menu for the static server:
navbar: submods
	$(UDIR)/html_include.awk <$(TEMPLATE_DIR)/navbar.pre >$(TEMPLATE_DIR)/navbar.txt
	python3 write_sample_programs.py

# rule for making html files from ptml files:
%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UDIR)/html_checker.py $<
	$(UDIR)/html_include.awk <$< >$@
	git add $@

local: $(HTML_FILES)

# build sample asm web pages for project web site:
$(PTML_DIR)/%.ptml: $(TDIR)/Intel/%.asm
	$(MUDIR)/asm2ptml.awk $< >$@

samples: $(ASM_PTMLS) $(TDIR)
	
# build the static website describing the project:
website: $(INCS) $(HTML_FILES) help
	-git commit -a 
	git pull --recurse-submodules origin master
	git push origin master

# setup a server
prod_env:
	pip install -r $(REQ_DIR)/requirements.txt

# setup developer
dev_env:
	pip install -r $(REQ_DIR)/requirements-dev.txt

# dev container has dev tools
dev_container: $(DOCKER_DIR)/Dockerfile $(REQ_DIR)/requirements-dev.txt
	docker build -t gcallah/$(REPO)-dev docker

# prod container has only what's needed to run
prod_container: $(DOCKER_DIR)/Deployable $(REQ_DIR)/requirements.txt
	docker system prune -f
	docker build -t gcallah/$(REPO) docker --no-cache --build-arg repo=$(REPO) -f $(DOCKER_DIR)/Deployable

# deploy prod container
deploy_container:
	docker push gcallah/$(REPO):latest

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES)) $(patsubst %.js,%.eslint,$(JSFILES))

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

%.eslint:
	$(ESLINT) $*.js

help_mips: $(MIPS_SRCS)
	$(EXTR) <$(MIPS_DIR)/arithmetic.py | $(D2HTML) >$(TEMPLATE_DIR)/mips_arithmetic.txt
	$(EXTR) <$(MIPS_DIR)/control_flow.py | $(D2HTML) >$(TEMPLATE_DIR)/mips_control_flow.txt
	$(EXTR) <$(MIPS_DIR)/data_mov.py | $(D2HTML) >$(TEMPLATE_DIR)/mips_data_mov.txt
	$(EXTR) <$(MIPS_DIR)/interrupts.py | $(D2HTML) >$(TEMPLATE_DIR)/mips_interrupts.txt

# build instruction help material from python source:
help: $(SRCS) samples help_mips
	python3 write_sample_programs.py
	git add $(TEMPLATE_DIR)/sample_programs_*.txt -f
	-git commit -m "Updating sample files"
	$(EXTR) <$(SDIR)/parse.py | $(D2HTML) >$(TEMPLATE_DIR)/data.txt
	$(EXTR) <$(INTEL_DIR)/arithmetic.py | $(D2HTML) >$(TEMPLATE_DIR)/arithmetic.txt
	$(EXTR) <$(INTEL_DIR)/control_flow.py | $(D2HTML) >$(TEMPLATE_DIR)/control_flow.txt
	$(EXTR) <$(INTEL_DIR)/data_mov.py | $(D2HTML) >$(TEMPLATE_DIR)/data_mov.txt
	$(EXTR) <$(INTEL_DIR)/interrupts.py | $(D2HTML) >$(TEMPLATE_DIR)/interrupts.txt
	$(UDIR)/html_include.awk <$(ODIR)/help.ptml >$(ODIR)/help.html
	$(UDIR)/django2ptml.awk <$(ODIR)/help.html title="Language Description" >$(PTML_DIR)/help.ptml
	-git commit $(ODIR)/help.html
	git push origin master

jsfile:
	python3 function_create_js.py
	git add function_create_js.py
	git add mysite/static/Emu86/sample_functions*.js
	git commit -m "Updating js sample files"
	git push origin master

zip: 
	-git rm Haldun.zip
	-git commit -m 'Removing old zip file'
	git push origin master
	git archive --format zip --output Haldun.zip master 
	git add Haldun.zip
	git commit -m 'Updating zip file'
	git push origin master

db:
	python3 manage.py makemigrations
	python3 manage.py migrate
	git add $(EMUDIR)/migrations/*.py
	-git commit $(EMUDIR)/migrations/*.py
	git push origin master

jupyter_kernel:
	pip3 install --upgrade emu86

intel_kernel:
	python3 -m kernels.intel.install

att_kernel:
	python3 -m kernels.att.install

mips_asm_kernel:
	python3 -m kernels.mips_asm.install

mips_mml_kernel:
	python3 -m kernels.mips_mml.install

riscv_kernel:
	python3 -m kernels.riscv.install

all_tests: tests # test_docker

tests: FORCE
	./all_tests.sh

test_docker:
	docker build -t gcallah/$(REPO) docker/

github:
	-git commit -a
	git push origin master

# dev: $(SRCS) $(MIPS_SRCS) $(OBJS) tests
dev: tests
	pytest $(PYTESTFILES)
	python3 manage.py runserver

# prod: $(SRCS) $(MIPS_SRCS) $(OBJS) navbar tests
prod: tests github
