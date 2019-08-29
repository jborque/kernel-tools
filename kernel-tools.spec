# Much of this is borrowed from the original kernel.spec
# It needs a bunch of the macros for rawhide vs. not-rawhide builds.

# For a stable, released kernel, released_kernel should be 1. For rawhide
# and/or a kernel built from an rc or git snapshot, released_kernel should
# be 0.
%global released_kernel 1
%global baserelease 200
%global fedora_build %{baserelease}

# base_sublevel is the kernel version we're starting with and patching
# on top of -- for example, 3.1-rc7-git1 starts with a 3.0 base,
# which yields a base_sublevel of 0.
%global base_sublevel 2

## If this is a released kernel ##
%if 0%{?released_kernel}

# Do we have a -stable update to apply?
%global stable_update 11
# Set rpm version accordingly
%if 0%{?stable_update}
%global stablerev %{stable_update}
%global stable_base %{stable_update}
%endif
%global rpmversion 5.%{base_sublevel}.%{stable_update}

## The not-released-kernel case ##
%else
# The next upstream release sublevel (base_sublevel+1)
%global upstream_sublevel %(echo $((%{base_sublevel} + 1)))

# The rc snapshot level
%global rcrev 0
# Set rpm version accordingly
%global rpmversion 5.%{upstream_sublevel}.0
%endif
# Nb: The above rcrev values automagically define Patch00 and Patch01 below.

# pkg_release is what we'll fill in for the rpm Release: field
%if 0%{?released_kernel}

%global pkg_release %{fedora_build}%{?buildid}%{?dist}

%else

# non-released_kernel
%if 0%{?rcrev}
%global rctag .rc%rcrev
%else
%global rctag .rc0
%endif
%global gittag .git0
%global pkg_release 0%{?rctag}%{?gittag}.%{fedora_build}%{?buildid}%{?dist}

%endif

# The kernel tarball/base version
%global kversion 5.%{base_sublevel}
%global KVERREL %{version}-%{release}.%{_target_cpu}

%global _debuginfo_subpackages 1
%undefine _include_gdb_index
%undefine _include_minidebuginfo

# perf needs this
%undefine _strict_symbol_defs_build

BuildRequires: kmod, patch, bash, tar, git
BuildRequires: bzip2, xz, findutils, gzip, m4, perl-interpreter, perl(Carp), perl-devel, perl-generators, make, diffutils, gawk
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc
BuildRequires: net-tools, hostname, bc, elfutils-devel
BuildRequires: zlib-devel binutils-devel newt-devel python3-docutils perl(ExtUtils::Embed) bison flex xz-devel
BuildRequires: audit-libs-devel glibc-devel glibc-static python3-devel
BuildRequires: asciidoc xmlto
# Used to mangle unversioned shebangs to be Python 3
BuildRequires: /usr/bin/pathfix.py
%ifnarch s390x %{arm}
BuildRequires: numactl-devel
%endif
BuildRequires: pciutils-devel gettext ncurses-devel
BuildConflicts: rhbuildsys(DiskFree) < 500Mb
BuildRequires: rpm-build, elfutils
%{?systemd_requires}
BuildRequires: systemd

Source0: https://www.kernel.org/pub/linux/kernel/v5.x/linux-%{kversion}.tar.xz

# Sources for kernel-tools
Source2000: cpupower.service
Source2001: cpupower.config

# Here should be only the patches up to the upstream canonical Linus tree.

# For a stable release kernel
%if 0%{?stable_base}
Source5000: patch-5.%{base_sublevel}.%{stable_base}.xz
%else
# non-released_kernel case
# These are automagically defined by the rcrev value set up
# near the top of this spec file.
%if 0%{?rcrev}
Source5000: patch-5.%{upstream_sublevel}-rc%{rcrev}.xz
%endif
%endif

# ongoing complaint, full discussion delayed until ksummit/plumbers
Patch0: 0001-iio-Use-event-header-from-kernel-tree.patch

# rpmlint cleanup
Patch6: 0002-perf-Don-t-make-sourced-script-executable.patch
Name: kernel-tools
Summary: Assortment of tools for the Linux kernel
License: GPLv2
URL: http://www.kernel.org/
Version: %{rpmversion}
Release: %{pkg_release}
Provides:  cpupowerutils = 1:009-0.6.p1
Obsoletes: cpupowerutils < 1:009-0.6.p1
Provides:  cpufreq-utils = 1:009-0.6.p1
Provides:  cpufrequtils = 1:009-0.6.p1
Obsoletes: cpufreq-utils < 1:009-0.6.p1
Obsoletes: cpufrequtils < 1:009-0.6.p1
Obsoletes: cpuspeed < 1:1.5-16
Requires: kernel-tools-libs = %{version}-%{release}
%description -n kernel-tools
This package contains the tools/ directory from the kernel source
and the supporting documentation.


%package -n perf
Summary: Performance monitoring for the Linux kernel
Requires: bzip2
License: GPLv2
%description -n perf
This package contains the perf tool, which enables performance monitoring
of the Linux kernel.

%global pythonperfsum Python bindings for apps which will manipulate perf events
%global pythonperfdesc A Python module that permits applications \
written in the Python programming language to use the interface \
to manipulate perf events.

%package -n python3-perf
Summary: %{pythonperfsum}
%{?python_provide:%python_provide python3-perf}
%description -n python3-perf
%{pythonperfdesc}

%package -n kernel-tools-libs
Summary: Libraries for the kernels-tools
License: GPLv2
%description -n kernel-tools-libs
This package contains the libraries built from the tools/ directory
from the kernel source.

%package -n kernel-tools-libs-devel
Summary: Assortment of tools for the Linux kernel
License: GPLv2
Requires: kernel-tools = %{version}-%{release}
Provides:  cpupowerutils-devel = 1:009-0.6.p1
Obsoletes: cpupowerutils-devel < 1:009-0.6.p1
Requires: kernel-tools-libs = %{version}-%{release}
Provides: kernel-tools-devel
%description -n kernel-tools-libs-devel
This package contains the development files for the tools/ directory from
the kernel source.

%package -n bpftool
Summary: Inspection and simple manipulation of eBPF programs and maps
License: GPLv2
%description -n bpftool
This package contains the bpftool, which allows inspection and simple
manipulation of eBPF programs and maps.

%package -n libbpf
Summary: The bpf library from kernel source
License: GPLv2
%description -n libbpf
This package contains the kernel source bpf library.

%package -n libbpf-devel
Summary: Developement files for the bpf library from kernel source
License: GPLv2
%description -n libbpf-devel
This package includes libraries and header files needed for development
of applications which use bpf library from kernel source.

%prep
%setup -q -n kernel-%{kversion}%{?dist} -c

cd linux-%{kversion}

# This is for patching either an -rc or stable
%if 0%{?rcrev}
    xzcat %{SOURCE5000} | patch -p1 -F1 -s
%endif

%if 0%{?stable_base}
    xzcat %{SOURCE5000} | patch -p1 -F1 -s
%endif

%patch0 -p1
%patch6 -p1

# END OF PATCH APPLICATIONS

# Mangle /usr/bin/python shebangs to /usr/bin/python3
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" tools/ tools/perf/scripts/python/*.py scripts/gen_compile_commands.py

###
### build
###
%build

cd linux-%{kversion}

%global perf_make \
  make EXTRA_CFLAGS="${RPM_OPT_FLAGS}" LDFLAGS="%{__global_ldflags}" %{?cross_opts} V=1 NO_PERF_READ_VDSO32=1 NO_PERF_READ_VDSOX32=1 WERROR=0 NO_LIBUNWIND=1 HAVE_CPLUS_DEMANGLE=1 NO_GTK2=1 NO_STRLCPY=1 NO_BIONIC=1 NO_JVMTI=1 prefix=%{_prefix}
%global perf_python3 -C tools/perf PYTHON=%{__python3}
# perf
# make sure check-headers.sh is executable
chmod +x tools/perf/check-headers.sh
%{perf_make} %{perf_python3} all

# cpupower
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
make %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false
%ifarch %{ix86}
    pushd tools/power/cpupower/debug/i386
    make %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    make %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch %{ix86} x86_64
   pushd tools/power/x86/x86_energy_perf_policy/
   make
   popd
   pushd tools/power/x86/turbostat
   make
   popd
%endif #turbostat/x86_energy_perf_policy
pushd tools/thermal/tmon/
make
popd
pushd tools/iio/
make
popd
pushd tools/gpio/
make
popd
pushd tools/bpf/bpftool
make
popd
pushd tools/lib/bpf
make V=1
popd

# Build the docs
pushd tools/kvm/kvm_stat/
make %{?_smp_mflags} man
popd
pushd tools/perf/Documentation/
make %{?_smp_mflags} man
popd

###
### install
###

%install

cd linux-%{kversion}

# perf tool binary and supporting scripts/binaries
%{perf_make} %{perf_python3} DESTDIR=%{buildroot} lib=%{_lib} install-bin install-traceevent-plugins
# remove the 'trace' symlink.
rm -f %{buildroot}%{_bindir}/trace
# remove the perf-tips
rm -rf %{buildroot}%{_docdir}/perf-tip

# For both of the below, yes, this should be using a macro but right now
# it's hard coded and we don't actually want it anyway right now.
# Whoever wants examples can fix it up!

# remove examples
rm -rf %{buildroot}/usr/lib/perf/examples
# remove the stray header file that somehow got packaged in examples
rm -rf %{buildroot}/usr/lib/perf/include/bpf/

# python-perf extension
%{perf_make} %{perf_python3} DESTDIR=%{buildroot} install-python_ext

# perf man pages (note: implicit rpm magic compresses them later)
install -d %{buildroot}/%{_mandir}/man1
install -pm0644 tools/kvm/kvm_stat/kvm_stat.1 %{buildroot}/%{_mandir}/man1/
install -pm0644 tools/perf/Documentation/*.1 %{buildroot}/%{_mandir}/man1/

make -C tools/power/cpupower DESTDIR=%{buildroot} libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
rm -f %{buildroot}%{_libdir}/*.{a,la}
%find_lang cpupower
mv cpupower.lang ../
%ifarch %{ix86}
    pushd tools/power/cpupower/debug/i386
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
chmod 0755 %{buildroot}%{_libdir}/libcpupower.so*
mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
install -m644 %{SOURCE2000} %{buildroot}%{_unitdir}/cpupower.service
install -m644 %{SOURCE2001} %{buildroot}%{_sysconfdir}/sysconfig/cpupower
%ifarch %{ix86} x86_64
   mkdir -p %{buildroot}%{_mandir}/man8
   pushd tools/power/x86/x86_energy_perf_policy
   make DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/turbostat
   make DESTDIR=%{buildroot} install
   popd
%endif #turbostat/x86_energy_perf_policy
pushd tools/thermal/tmon
make INSTALL_ROOT=%{buildroot} install
popd
pushd tools/iio
make DESTDIR=%{buildroot} install
popd
pushd tools/gpio
make DESTDIR=%{buildroot} install
popd
pushd tools/kvm/kvm_stat
make INSTALL_ROOT=%{buildroot} install-tools
popd
pushd tools/bpf/bpftool
make DESTDIR=%{buildroot} prefix=%{_prefix} bash_compdir=%{_sysconfdir}/bash_completion.d/ mandir=%{_mandir} install doc-install
# man-pages packages this (rhbz #1686954)
rm %{buildroot}%{_mandir}/man7/bpf-helpers.7
popd
pushd tools/lib/bpf
make DESTDIR=%{buildroot} prefix=%{_prefix} libdir=%{_libdir} V=1 install install_headers
popd

###
### scripts
###

%ldconfig_scriptlets -n kernel-tools-libs

%post -n kernel-tools
%systemd_post cpupower.service

%preun -n kernel-tools
%systemd_preun cpupower.service

%postun
%systemd_postun cpupower.service

%files -n perf
%{_bindir}/perf
%dir %{_libdir}/traceevent
%{_libdir}/traceevent/plugins/
%{_libexecdir}/perf-core
%{_datadir}/perf-core/
%{_mandir}/man[1-8]/perf*
%{_sysconfdir}/bash_completion.d/perf
%doc linux-%{kversion}/tools/perf/Documentation/examples.txt
%license linux-%{kversion}/COPYING

%files -n python3-perf
%license linux-%{kversion}/COPYING
%{python3_sitearch}/*

%files -n kernel-tools -f cpupower.lang
%{_bindir}/cpupower
%{_datadir}/bash-completion/completions/cpupower
%ifarch %{ix86} x86_64
%{_bindir}/centrino-decode
%{_bindir}/powernow-k8-decode
%endif
%{_unitdir}/cpupower.service
%{_mandir}/man[1-8]/cpupower*
%config(noreplace) %{_sysconfdir}/sysconfig/cpupower
%ifarch %{ix86} x86_64
%{_bindir}/x86_energy_perf_policy
%{_mandir}/man8/x86_energy_perf_policy*
%{_bindir}/turbostat
%{_mandir}/man8/turbostat*
%endif
%{_bindir}/tmon
%{_bindir}/iio_event_monitor
%{_bindir}/iio_generic_buffer
%{_bindir}/lsiio
%{_bindir}/lsgpio
%{_bindir}/gpio-hammer
%{_bindir}/gpio-event-mon
%{_mandir}/man1/kvm_stat*
%{_bindir}/kvm_stat
%license linux-%{kversion}/COPYING

%files -n kernel-tools-libs
%{_libdir}/libcpupower.so.0
%{_libdir}/libcpupower.so.0.0.1
%license linux-%{kversion}/COPYING

%files -n kernel-tools-libs-devel
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h

%files -n bpftool
%{_sbindir}/bpftool
%{_sysconfdir}/bash_completion.d/bpftool
%{_mandir}/man8/bpftool-btf.8.gz
%{_mandir}/man8/bpftool-cgroup.8.gz
%{_mandir}/man8/bpftool-map.8.gz
%{_mandir}/man8/bpftool-net.8.gz
%{_mandir}/man8/bpftool-prog.8.gz
%{_mandir}/man8/bpftool-perf.8.gz
%{_mandir}/man8/bpftool-feature.8.gz
%{_mandir}/man8/bpftool.8.gz
%license linux-%{kversion}/COPYING

%files -n libbpf
%{_libdir}/libbpf.so.0
%{_libdir}/libbpf.so.0.0.3
%license linux-%{kversion}/COPYING

%files -n libbpf-devel
%{_libdir}/libbpf.a
%{_libdir}/libbpf.so
%{_libdir}/pkgconfig/libbpf.pc
%{_includedir}/bpf/bpf.h
%{_includedir}/bpf/btf.h
%{_includedir}/bpf/libbpf.h
%{_includedir}/bpf/libbpf_util.h
%{_includedir}/bpf/xsk.h
%license linux-%{kversion}/COPYING

%changelog
* Thu Aug 29 2019 Justin M. Forbes <jforbes@fedoraproject.org> - 5.2.11-200
- Linux v5.2.11

* Mon Aug 26 2019 Justin M. Forbes <jforbes@fedoraproject.org> - 5.2.10-200
- Linux v5.2.10

* Fri Aug 16 2019 Justin M. Forbes <jforbes@fedoraproject.org> - 5.2.9-200
- Linux v5.2.9

* Thu Aug 08 2019 Justin M. Forbes <jforbes@fedoraproject.org> - 5.2.7-200
- Linux v5.2.7

* Mon Aug 05 2019 Justin M. Forbes <jforbes@fedoraproject.org> - 5.2.6-200
- Linux v5.2.6

* Wed Jul 31 2019 Justin M. Forbes <jforbes@fedoraproject.org> - 5.2.5-200
- Linux v5.2.5

* Mon Jul 29 2019 Justin M. Forbes <jforbes@fedoraproject.org> - 5.2.4-200
- Linux v5.2.4

* Wed Jun 19 2019 Jeremy Cline <jcline@redhat.com> - 5.1.12-300
- Linux v5.1.12

* Mon Jun 03 2019 Jeremy Cline <jcline@redhat.com> - 5.1.6-300
- Linux v5.1.6

* Mon May 06 2019 Jeremy Cline <jcline@redhat.com> - 5.1.4-300
- Linux v5.1.4

* Sat May 04 2019 Laura Abbott <labbott@redhat.com> - 5.0.12-300
- Linux v5.0.12

* Mon Apr 22 2019 Laura Abbott <labbott@redhat.com> - 5.0.9-300
- Linux v5.0.9

* Mon Apr 08 2019 Laura Abbott <labbott@redhat.com> - 5.0.7-300
- Linux v5.0.7

* Wed Apr 03 2019 Laura Abbott <labbott@redhat.com> - 5.0.6-300
- Linux v5.0.6

* Wed Mar 27 2019 Laura Abbott <labbott@redhat.com> - 5.0.5-300
- Linux v5.0.5

* Tue Mar 19 2019 Laura Abbott <labbott@redhat.com> - 5.0.4-300
- Linux v5.0.4

* Tue Mar 19 2019 Laura Abbott <labbott@redhat.com> - 5.0.3-300
- Linux v5.0.3

* Mon Mar 18 2019 Jeremy Cline <jcline@fedoraproject.org>
- Drop the bpf-helpers manual page as man-pages packages it

* Mon Mar 04 2019 Laura Abbott <labbott@redhat.com> - 5.0.0-1
- Linux v5.0.0

* Mon Feb 25 2019 Laura Abbott <labbott@redhat.com> - 5.0.0-0.rc8.git0.1
- Linux v5.0-rc8

* Sun Feb 17 2019 Laura Abbott <labbott@redhat.com> - 5.0.0-0.rc7.git0.1
- Linux v5.0-rc7

* Mon Feb 11 2019 Laura Abbott <labbott@redhat.com> - 5.0.0-0.rc6.git0.1
- Linux v5.0-rc6

* Mon Feb 04 2019 Laura Abbott <labbott@redhat.com> - 5.0.0-0.rc5.git0.1
- Linux v5.0-rc5

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-0.rc4.git0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Laura Abbott <labbott@redhat.com> - 5.0.0-0.rc4.git0.1
- Linux v5.0-rc4

* Fri Jan 25 2019 Laura Abbott <labbott@redhat.com> - 5.0.0-0.rc3.git0.2
- Rebuild for gcc9

* Mon Jan 14 2019 Laura Abbott <labbott@redhat.com> - 5.0.0-0.rc3.git0.1
- Linux v5.0-rc3

* Mon Jan 14 2019 Laura Abbott <labbott@redhat.com> - 5.0.0-0.rc2.git0.1
- Linux v5.0-rc2

* Thu Jan 10 2019 Miro Hrončok <mhroncok@redhat.com> - 5.0.0-0.rc1.git0.2
- Remove Python 2 subpackage

* Mon Jan 07 2019 Laura Abbott <labbott@redhat.com> - 5.0.0-0.rc1.git0.1
- Linux v5.0-rc1

* Mon Dec 24 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.20.0-1
- Linux v4.20.0

* Mon Dec 17 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.20.0-0.rc7.git0.1
- Linux v4.20-rc7

* Mon Dec 10 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.20.0-0.rc6.git0.1
- Linux v4.20-rc6

* Mon Dec 03 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.20.0-0.rc5.git0.1
- Linux v4.20-rc5

* Mon Nov 26 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.20.0-0.rc4.git0.1
- Linux v4.20-rc4

* Mon Nov 19 2018 Jeremy Cline <jeremy@jcline.org> - 4.20.0-0.rc3.git0.1
- Linux v4.20-rc3

* Sun Nov 11 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.20.0-0.rc2.git0.1
- Linux v4.20-rc2

* Mon Nov 05 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.20.0-0.rc1.git0.1
- Linux v4.20-rc1
