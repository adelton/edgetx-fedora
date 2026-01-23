
spec := $(shell ls *.spec | head -1)
outdir := $(CURDIR)

PACKAGE := $(shell rpm -q --qf '%{name}\n' --specfile $(spec) 2> /dev/null | head -1)
VERSION := $(shell rpm -q --qf '%{version}\n' --specfile $(spec) 2> /dev/null | head -1)
spec_out := $(PACKAGE)-$(VERSION).spec

srpm-common:
	for i in /usr/bin/rpmautospec /usr/bin/spectool ; do rpm -qf $$i || dnf install --setopt=install_weak_deps=False -y $$i ; done
	mkdir -p $(outdir)/.sources
	rpmautospec process-distgit $(spec) $(outdir)/.sources/$(spec_out)
	touch -r $(spec) $(outdir)/.sources/$(spec_out)
	cp -p *.patch $(outdir)/.sources/
	cd $(outdir)/.sources && spectool -g $(spec_out)

srpm-pure: srpm-common
	cd $(outdir)/.sources && rpmbuild -D '_srcrpmdir $(outdir)' -D '_sourcedir $(outdir)/.sources' -bs $(outdir)/.sources/$(spec_out)
	rm -rf $(outdir)/.sources

srpm: srpm-pure
