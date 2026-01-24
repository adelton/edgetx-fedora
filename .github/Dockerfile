FROM registry.fedoraproject.org/fedora
RUN dnf install --setopt=install_weak_deps=False -y rpm-build rpmdevtools rpmautospec git-core 'dnf-command(builddep)' make
RUN mkdir /src
WORKDIR /src
COPY edgetx-companion.spec *.patch .copr/Makefile /src
COPY .git /src/.git
RUN git reset --hard HEAD
RUN make srpm-pure
RUN dnf builddep --setopt=install_weak_deps=False -y edgetx-companion.spec
