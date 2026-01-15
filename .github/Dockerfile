FROM registry.fedoraproject.org/fedora
RUN dnf install --setopt=install_weak_deps=False -y rpm-build rpmdevtools rpmautospec git-core 'dnf-command(builddep)' make
RUN mkdir -p /src
WORKDIR /src
RUN if [ -d /src/dependencies/RPMS/repodata ] ; then ( echo '[edgetx-build-dependencies]' ; echo 'baseurl=file:/src/dependencies/RPMS' ; echo gpgcheck=0 ) > /etc/yum.repos.d/edgetx-build-dependencies.repo ; fi
COPY edgetx-companion.spec *.patch .copr/Makefile /src
COPY .git /src/.git
RUN git reset --hard HEAD
RUN make spec=edgetx-companion.spec srpm-pure
RUN dnf builddep --setopt=install_weak_deps=False -y edgetx-companion-*.src.rpm
