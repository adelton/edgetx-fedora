FROM registry.fedoraproject.org/fedora:41
RUN dnf install -y rpm-build 'dnf-command(builddep)' make
RUN mkdir /src
WORKDIR /src
COPY * .copr/Makefile /src
RUN dnf builddep -y opentx-companion.spec
RUN make srpm
