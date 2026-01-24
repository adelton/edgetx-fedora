FROM registry.fedoraproject.org/fedora as localhost/edgetx-deps-builder
RUN dnf install --setopt=install_weak_deps=False -y rpm-build rpmdevtools rpmautospec git-core 'dnf-command(builddep)' make createrepo
RUN mkdir /src
WORKDIR /src

FROM localhost/edgetx-deps-builder
ARG PACKAGE
COPY .copr/Makefile /.copr/Makefile
COPY dependencies/*.spec dependencies/*.patch /src

RUN mkdir -p ~/rpmbuild/RPMS/SRMPS
RUN make -f /.copr/Makefile -C /src spec=${PACKAGE}.spec outdir=$( echo ~/rpmbuild/RPMS/SRPMS ) srpm-pure

WORKDIR /root/rpmbuild/RPMS/SRPMS
RUN rpm -qlp ${PACKAGE}-*.src.rpm
RUN rpm -Uvh ${PACKAGE}-*.src.rpm
RUN if [ -d /root/rpmbuild/RPMS/repodata ] ; then ( echo '[edgetx-build-dependencies]' ; echo 'baseurl=file:/root/rpmbuild/RPMS' ; echo gpgcheck=0 ) > /etc/yum.repos.d/edgetx-build-dependencies.repo ; fi
# Workaround https://bugzilla.redhat.com/show_bug.cgi?id=2432550
RUN sed -i 's/tsflags=.*/tsflags=/' /etc/dnf/dnf.conf
RUN dnf builddep --setopt=install_weak_deps=False -y ~/rpmbuild/SPECS/${PACKAGE}-*.spec
RUN rpmbuild -br ~/rpmbuild/SPECS/${PACKAGE}-*.spec || true
RUN dnf builddep --setopt=install_weak_deps=False -y ~/rpmbuild/SRPMS/${PACKAGE}-*.buildreqs.nosrc.rpm
RUN rpmbuild -bb ~/rpmbuild/SPECS/${PACKAGE}-*.spec
RUN createrepo ~/rpmbuild/RPMS
