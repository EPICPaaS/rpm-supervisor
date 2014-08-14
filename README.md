rpm-supervisor
==============

The rpm spec for building supervisor 3.x on centos 6 or centos 7

#How to build:

(clone me to /opt/rpm-supervisor)

mv /root/rpmbuild /root/rpmbuild_backup

ln -s /opt/rpm-supervisor/rpmbuild /root/rpmbuild

cd /root/rpmbuild

rpmbuild -ba SPECS/supervisor.spec
