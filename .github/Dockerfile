FROM registry.fedoraproject.org/fedora
RUN dnf install -y rpm-build rpmdevtools rpmautospec 'dnf-command(builddep)' make
RUN mkdir /src
WORKDIR /src
COPY edgetx-companion.spec *.patch .copr/Makefile /src
COPY .git /src/.git
RUN make srpm
RUN dnf builddep -y edgetx-companion.spec
