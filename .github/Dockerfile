FROM registry.fedoraproject.org/fedora
RUN dnf install -y rpm-build 'dnf-command(builddep)' make
RUN mkdir /src
WORKDIR /src
COPY * .copr/Makefile /src
RUN dnf builddep -y edgetx-companion.spec
RUN make srpm
