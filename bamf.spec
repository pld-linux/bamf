#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Application matching framework
Name:		bamf
Version:	0.2.104
Release:	4
# Library bits are LGPLv2 or LGPLv3 (but not open-ended LGPLv2+);
# non-lib bits are GPLv3.
# pbrobinson points out that three files in the lib are actually
# marked GPL in headers, making library GPL, though we think this
# may not be upstream's intention. For now, marking library as
# GPL.
# License:	LGPLv2 or LGPLv3
License:	GPL v2 or GPL v3
Group:		Libraries
URL:		https://launchpad.net/bamf
Source0:	http://launchpad.net/bamf/0.2/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	4271cd5979483f7e3a9bffc42fed6383
BuildRequires:	dbus-glib-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+2-devel
BuildRequires:	gtk+3-devel
BuildRequires:	gtk-doc
BuildRequires:	libgtop-devel
BuildRequires:	libwnck-devel
BuildRequires:	libwnck2-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BAMF removes the headache of applications matching into a simple DBus
daemon and C wrapper library. Currently features application matching
at amazing levels of accuracy (covering nearly every corner case).
This package contains the bamf library built against GTK+ 2.

%package devel
Summary:	Development files for %{name}
License:	GPL v2 or GPL v3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package daemon
Summary:	Application matching framework
License:	GPL v3
Group:		Libraries

%description daemon
BAMF removes the headache of applications matching into a simple DBus
daemon and C wrapper library. Currently features application matching
at amazing levels of accuracy (covering nearly every corner case).
This package contains the bamf daemon and supporting data.

%package -n %{name}3
Summary:	Application matching framework (GTK+ 3 build)
Group:		Libraries

%description -n %{name}3
BAMF removes the headache of applications matching into a simple DBus
daemon and C wrapper library. Currently features application matching
at amazing levels of accuracy (covering nearly every corner case).
This package contains the bamf library built against GTK+ 3.

%package -n %{name}3-devel
Summary:	Development files for %{name} (GTK+ 3 build)
License:	GPL v2 or GPL v3
Group:		Development/Libraries
Requires:	%{name}3 = %{version}-%{release}

%description -n %{name}3-devel
The %{name}3-devel package contains libraries and header files for
developing applications that use %{name} (GTK+ 3 build).

%package apidocs
Summary:	%{name} API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API and internal documentation for %{name} library.

%prep
%setup -q

%build
# ../.././src/bamf-legacy-window.c: In function 'bamf_legacy_window_get_class_name':
# ../.././src/bamf-legacy-window.c:144:3: error: 'wnck_class_group_get_res_class' is deprecated (declared at /usr/include/libwnck-3.0/libwnck/class-group.h:89): Use 'wnck_class_group_get_id' instead [-Werror=deprecated-declarations]
CFLAGS="%{rpmcflags} -Wno-error=deprecated-declarations"

install -d build-gtk3 build-gtk2
cd build-gtk2
../%configure \
	--disable-static \
	--with-gtk=2 \
	--with-html-dir=%{_gtkdocdir} \
	--enable-gtk-doc
%{__make}

cd ../build-gtk3
../%configure \
	--disable-static \
	--with-gtk=3 \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install -C build-gtk2 \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} install -C build-gtk3 \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbamf.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbamf3.la

#find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n %{name}3 -p /sbin/ldconfig
%postun	-n %{name}3 -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbamf.so.*.*.*
%ghost %{_libdir}/libbamf.so.0

%files -n	%{name}3
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbamf3.so.*.*.*
%ghost %{_libdir}/libbamf3.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/libbamf
%{_libdir}/libbamf.so
%{_pkgconfigdir}/libbamf.pc
# Installation of these was disabled in the 0.2.72 release commit,
# with no explanation - http://bazaar.launchpad.net/~unity-team/bamf/trunk/revision/374
#%{_libdir}/girepository-1.0/Bamf*.typelib
#%{_datadir}/gir-1.0/Bamf*.gir
#%{_datadir}/vala/vapi/Bamf*.vapi

%files -n	%{name}3-devel
%defattr(644,root,root,755)
%{_includedir}/libbamf3
%{_libdir}/libbamf3.so
%{_pkgconfigdir}/libbamf3.pc

%files daemon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/bamfdaemon
%{_datadir}/dbus-1/services/org.ayatana.bamf.service

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libbamf
%endif
