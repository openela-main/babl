# skip tests known to be problematic in a specific version
%global skip_checks_version 0.1.50
%ifarch ppc64 ppc64le
%global skip_checks chromaticities srgb_to_lab_u8 models float-to-8bit
%else
%global skip_checks %nil
%endif

%if ! 0%{?fedora}%{?rhel} || 0%{?fedora} >= 20 || 0%{?rhel} > 7
%global develdocdir %{_docdir}/%{name}-devel/html
%else
%global develdocdir %{_docdir}/%{name}-devel-%{version}/html
%endif

Summary:	A dynamic, any to any, pixel format conversion library
Name:		babl
Version:	0.1.52
Release:	1%{?dist}

# Compute some version related macros
# Ugly hack, you need to get your quoting backslashes/percent signs straight
%global major %(ver=%version; echo ${ver%%%%.*})
%global minor %(ver=%version; ver=${ver#%major.}; echo ${ver%%%%.*})
%global micro %(ver=%version; ver=${ver#%major.%minor.}; echo ${ver%%%%.*})
%global apiver %major.%minor

# The gggl codes contained in this package are under the GPL, with exceptions allowing their use under libraries covered under the LGPL
License:	LGPLv3+ and GPLv3+
URL:		http://www.gegl.org/babl/
Source0:	https://download.gimp.org/pub/babl/%{apiver}/%{name}-%{version}.tar.bz2

BuildRequires:	librsvg2
BuildRequires:  automake, autoconf
BuildRequires:  gcc

%description
Babl is a dynamic, any to any, pixel format conversion library. It
provides conversions between the myriad of buffer types images can be
stored in. Babl doesn't only help with existing pixel formats, but also
facilitates creation of new and uncommon ones.

%package devel
Summary:	Headers for developing programs that will use %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig
%if ! (0%{?fedora} >= 22 || 0%{?rhel} > 7)
# Split off devel docs from 0.1.2-2 on
Obsoletes:	%{name}-devel < 0.1.2-2%{?dist}
Conflicts:	%{name}-devel < 0.1.2-2%{?dist}
%endif

%description devel
This package contains the libraries and header files needed for
developing with %{name}.

%package devel-docs
Summary:	Documentation for developing programs that will use %{name}
BuildArch:	noarch
Requires:	%{name}-devel = %{version}-%{release}
# Split off devel docs from 0.1.2-2 on
Obsoletes:	%{name}-devel < 0.1.2-2%{?dist}
Conflicts:	%{name}-devel < 0.1.2-2%{?dist}

%description devel-docs
This package contains documentation needed for developing with %{name}.

%prep
%autosetup -p1

%build
# use PIC/PIE because babl is likely to deal with data coming from untrusted
# sources
CFLAGS="-fPIC %optflags -fno-strict-aliasing"
LDFLAGS="-pie"
%configure --disable-static

make V=1 %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install INSTALL='install -p'

mkdir -p "%{buildroot}/%{develdocdir}"
cp -pr docs/graphics docs/*.html docs/babl.css "%{buildroot}/%{develdocdir}"
rm -rf "%{buildroot}/%{develdocdir}"/graphics/Makefile*

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%check
# skip tests known to be problematic in a specific version
%if "%version" == "%skip_checks_version"
pushd tests
for problematic in %skip_checks; do
    rm -f "$problematic"
    cat << EOF > "$problematic"
#!/bin/sh
echo Skipping test "$problematic"
EOF
    chmod +x "$problematic"
done
popd
%endif
make check

%ldconfig_scriptlets

%files
%doc AUTHORS COPYING README NEWS
%{_libdir}/*.so.*
%{_libdir}/babl-%{apiver}/

%files devel
%{_includedir}/babl-%{apiver}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%files devel-docs
%doc %{develdocdir}

%changelog
* Thu Jul 05 2018 Nils Philippsen <nils@tiptoe.de> - 0.1.51-1
- version 0.1.52

* Mon May 21 2018 Nils Philippsen <nils@tiptoe.de> - 0.1.50-3
- et tu, ppc64?

* Mon May 21 2018 Nils Philippsen <nils@tiptoe.de> - 0.1.50-2
- skip more problematic tests on ppc64le

* Mon May 21 2018 Josef Ridky <jridky@redhat.com> - 0.1.50-1
- New upstream release 0.1.50

* Thu May 17 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.1.48-1
- version 0.1.48

* Wed Apr 25 2018 Josef Ridky <jridky@redhat.com> - 0.1.46-1
- New upstream release 0.1.46

* Tue Mar 27 2018 Nils Philippsen <nils@tiptoe.de> - 0.1.44-1
- version 0.1.44

* Tue Feb 20 2018 Josef Ridky <jridky@redhat.com> - 0.1.42-4
- add gcc requirement

* Wed Feb 14 2018 Josef Ridky <jridky@redhat.com> - 0.1.42-3
- cleanup spec file (remove Group tag, apply new scriptlets)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.1.42-1
- version 0.1.42

* Wed Jan 17 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.1.40-1
- version 0.1.40

* Thu Nov 16 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.1.38-1
- version 0.1.38

* Sat Nov 11 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.1.36-1
- version 0.1.36

* Tue Oct 17 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.1.34-1
- version 0.1.34

* Tue Oct 03 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.1.32-1
- version 0.1.32

* Fri Aug 25 2017 Nils Philippsen <nils@tiptoe.de> - 0.1.30-1
- version 0.1.30

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.1.28-1
- version 0.1.28

* Mon May 15 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.1.26-1
- version 0.1.26

* Tue Feb 07 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.1.24-1
- version 0.1.24

* Thu Jan 26 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.1.22-1
- version 0.1.22

* Thu Jan 12 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.1.20-1
- version 0.1.20

* Fri Jun 17 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.1.18-1
- version 0.1.18

* Sun Feb 14 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.1.16-1
- version 0.1.16

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 23 2015 Nils Philippsen <nils@redhat.com> - 0.1.14-1
- version 0.1.14

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 Nils Philippsen <nils@redhat.com> - 0.1.12-2
- fix failing (crashing) concurrency stress test

* Thu Feb 05 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.1.12-1
- version 0.1.12

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Nils Philippsen <nils@redhat.com> - 0.1.10-11
- update source URL

* Tue Jul 29 2014 Nils Philippsen <nils@redhat.com> - 0.1.10-10
- drop obsoletes in future Fedora and EL versions (#1002080)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 07 2013 Nils Philippsen <nils@redhat.com> - 0.1.10-8
- use unversioned docdir from Fedora 20 on (#993679)

* Tue Jul 30 2013 Nils Philippsen <nils@redhat.com> - 0.1.10-7
- don't require w3m for building

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct 20 2012 Nils Philippsen <nils@redhat.com> - 0.1.10-5
- report problematic checks being skipped

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 03 2012 Nils Philippsen <nils@redhat.com> - 0.1.10-3
- prevent problematic check from being rebuilt

* Tue Apr 03 2012 Nils Philippsen <nils@redhat.com> - 0.1.10-2
- fix typo which caused problematic check not to be skipped

* Tue Apr 03 2012 Nils Philippsen <nils@redhat.com> - 0.1.10-1
- version 0.1.10
- skip check known to be problematic: concurrency-stress-test

* Tue Jan 10 2012 Nils Philippsen <nils@redhat.com> - 0.1.6-2
- rebuild for gcc 4.7

* Tue Dec 13 2011 Nils Philippsen <nils@redhat.com> - 0.1.6-1
- version 0.1.6

* Tue Feb 22 2011 Nils Philippsen <nils@redhat.com> - 0.1.4-1
- version 0.1.4
- correct source URL

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 23 2010 Nils Philippsen <nils@redhat.com> - 0.1.2-4
- use PIC/PIE because babl is likely to deal with data coming from untrusted
  sources

* Wed Jun 23 2010 Nils Philippsen <nils@redhat.com> - 0.1.2-3
- build with -fno-strict-aliasing

* Mon Jun 14 2010 Nils Philippsen <nils@redhat.com> - 0.1.2-2
- split off devel-docs subpackage to make package multi-lib compliant (#477807)
- let devel package require correct arch of base package

* Thu Jan 21 2010 Deji Akingunola <dakingun@gmail.com> - 0.1.2-1
- Update to 0.1.2

* Fri Dec 18 2009 Deji Akingunola <dakingun@gmail.com> - 0.1.0-5
- Remove the *.la files

* Thu Aug 13 2009 Nils Philippsen <nils@redhat.com>
- explain patch status

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Nils Philippsen <nils@redhat.com> - 0.1.0-3
- revert using "--disable-gtk-doc" as this doesn't work with babl (#477807)

* Thu Jul 02 2009 Nils Philippsen <nils@redhat.com>
- use "--disable-gtk-doc" to avoid rebuilding documentation (#477807)
- fix source URL

* Thu Jun 25 2009 Nils Philippsen <nils@redhat.com> - 0.1.0-2
- fix timestamps of built documentation for multilib (#477807)

* Fri May 22 2009 Deji Akingunola <dakingun@gmail.com> - 0.1.0-1
- Update to latest release (0.1.0)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep  2 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.0.22-2
- Include /usr/include/babl-0.0 directory

* Thu Jul 10 2008 Deji Akingunola <dakingun@gmail.com> - 0.0.22-1
- Update to latest release

* Thu Feb 28 2008 Deji Akingunola <dakingun@gmail.com> - 0.0.20-1
- New release

* Thu Jan 17 2008 Deji Akingunola <dakingun@gmail.com> - 0.0.18-2
- Apply patch to fix extensions loading on 64bit systems

* Thu Jan 10 2008 Deji Akingunola <dakingun@gmail.com> - 0.0.18-1
- Update to 0.0.18

* Mon Nov 26 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.16-1
- Update to 0.0.16 release 
- License change from GPLv2+ to GPLv3+

* Mon Oct 22 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.15-0.5.20071011svn
- Update the License field 

* Fri Oct 12 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.15-0.4.20071011svn
- Package the extension libraries in the main package
- Run 'make check' 

* Fri Oct 12 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.15-0.3.20071011svn
- Ensure timestamps are kept during install

* Fri Oct 12 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.15-0.2.20071011svn
- Remove the use of inexistent source url (Package reviews)
- Package the html docs

* Thu Oct 11 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.15-0.1.20071011svn
- Initial packaging for Fedora
