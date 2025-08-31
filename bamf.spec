# TODO: libunity-webapps support?
#
# Conditional build:
%bcond_without	apidocs		# API documentation

Summary:	Application matching framework
Summary(pl.UTF-8):	Szkielet do dopasowywania aplikacji
Name:		bamf
Version:	0.3.6
Release:	1
# Library bits are LGPLv2 or LGPLv3 (but not open-ended LGPLv2+);
# non-lib bits are GPLv3.
# pbrobinson points out that three files in the lib are actually
# marked GPL in headers, making library GPL, though we think this
# may not be upstream's intention. For now, marking library as
# GPL.
# License:	LGPL v2.1 or LGPL v3
License:	GPL v2 or GPL v3
Group:		Libraries
Source0:	https://launchpad.net/bamf/0.3/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	56b0b0ac2d3f2a0401db268c78cc8527
Patch0:		%{name}-gir.patch
URL:		https://launchpad.net/bamf
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	glib2-devel >= 1:2.30.0
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.10.2
BuildRequires:	gtk+2-devel >= 1:2.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	libgtop-devel >= 2.0
BuildRequires:	libwnck2-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.043
BuildRequires:	vala
BuildRequires:	xorg-lib-libX11-devel
Requires:	glib2 >= 1:2.30.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BAMF removes the headache of applications matching into a simple DBus
daemon and C wrapper library. Currently features application matching
at amazing levels of accuracy (covering nearly every corner case).
This package contains the bamf library built against GTK+ 2.

%description -l pl.UTF-8
BAMF rozwiązuje problem dopasowywania aplikacji za pomocą prostego
demona DBus i biblioteki obudowującej w C. Aktualne możliwości to
dopasowywanie aplikacji z zaskakującym poziomem dokładności
(obejmującym prawie każdy przypadek brzegowy). Ten pakiet zawiera
bibliotekę bamf zbudowaną dla GTK+ 2.

%package devel
Summary:	Development files for BAMF library (GTK+ 2 build)
Summary(pl.UTF-8):	Pliki programistyczne biblioteki BAMF (dla GTK+ 2)
License:	GPL v2 or GPL v3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.30.0
Requires:	libwnck2-devel >= 2.0

%description devel
This package contains header files for developing applications that
use BAMF with GTK+ 2.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących BAMF z GTK+ 2.

%package -n vala-libbamf
Summary:	Vala API for BAMF library (GTK+ 2 build)
Summary(pl.UTF-8):	API języka Vala do biblioteki BAMF (dla GTK+ 2)
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description -n vala-libbamf
Vala API for BAMF library (GTK+ 2 build).

%description -n vala-libbamf -l pl.UTF-8
API języka Vala do biblioteki BAMF (dla GTK+ 2).

%package apidocs
Summary:	BAMF API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki BAMF
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for BAMF library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki BAMF.

%package daemon
Summary:	Application matching framework
Summary(pl.UTF-8):	Szkielet do dopasowywania aplikacji
License:	GPL v3
Group:		Daemons
Requires:	dbus-glib >= 0.76
Requires:	glib2 >= 1:2.30.0

%description daemon
BAMF removes the headache of applications matching into a simple DBus
daemon and C wrapper library. Currently features application matching
at amazing levels of accuracy (covering nearly every corner case).
This package contains the bamf daemon and supporting data.

%description daemon -l pl.UTF-8
BAMF rozwiązuje problem dopasowywania aplikacji za pomocą prostego
demona DBus i biblioteki obudowującej w C. Aktualne możliwości to
dopasowywanie aplikacji z zaskakującym poziomem dokładności
(obejmującym prawie każdy przypadek brzegowy). Ten pakiet zawiera
demona bamf i dane pomocnicze.

%prep
%setup -q
%patch -P0 -p1

# ../.././src/bamf-legacy-window.c: In function 'bamf_legacy_window_get_class_name':
# ../.././src/bamf-legacy-window.c:144:3: error: 'wnck_class_group_get_res_class' is deprecated (declared at /usr/include/libwnck-3.0/libwnck/class-group.h:89): Use 'wnck_class_group_get_id' instead [-Werror=deprecated-declarations]
%{__sed} -i -e 's/-Werror //' configure.in

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-webapps \
	--with-gtk=2 \
	--with-html-dir=%{_gtkdocdir} \
	--enable-gtk-doc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbamf.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc TODO
%attr(755,root,root) %{_libdir}/libbamf.so.*.*.*
%ghost %{_libdir}/libbamf.so.0
%{_libdir}/girepository-1.0/Bamf-0.2.typelib

%files devel
%defattr(644,root,root,755)
%{_libdir}/libbamf.so
%{_includedir}/libbamf
%{_pkgconfigdir}/libbamf.pc
%{_datadir}/gir-1.0/Bamf-0.2.gir

%files -n vala-libbamf
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libbamf.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libbamf
%endif

%files daemon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/bamfdaemon
%{_datadir}/dbus-1/services/org.ayatana.bamf.service
