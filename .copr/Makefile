
PACKAGE := edgetx-companion

outdir := $(CURDIR)
spec := $(PACKAGE).spec

VERSION := $(shell rpm -q --qf '%{version}\n' --specfile $(PACKAGE).spec 2> /dev/null | head -1)
spec_out = $(PACKAGE)-$(VERSION).spec

spec_dir := ./
ifeq ($(shell test -d $(spec) && echo true),true)
	spec_dir = $(spec)/
	spec_file = $(PACKAGE).spec
else
	spec_dir = $(dir $(spec))
	spec_file = $(spec)
endif

srpm:
	for i in /usr/bin/rpmautospec /usr/bin/spectool ; do rpm -qf $$i || dnf install -y $$i ; done
	mkdir -p $(outdir)/.sources
	rpmautospec process-distgit $(spec_dir)$(spec_file) $(outdir)/.sources/$(spec_out)
	touch -r $(spec_dir)$(spec_file) $(outdir)/.sources/$(spec_out)
	cp -p $(spec_dir)*.patch $(outdir)/.sources/
	cd $(outdir)/.sources && spectool -g $(spec_out)
	cd $(outdir)/.sources && rpmbuild -D '_srcrpmdir $(outdir)' -D '_sourcedir $(outdir)/.sources' -bs $(outdir)/.sources/$(spec_out)
	rm -rf $(outdir)/.sources

