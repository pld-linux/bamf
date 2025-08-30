#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	gtk2		# GTK+ 2 library
%bcond_without	gtk3		# GTK+ 3 library

Summary:	Application matching framework
Summary(pl.UTF-8):	Szkielet do dopasowywania aplikacji
Name:		bamf
Version:	0.2.104
Release:	6
# Library bits are LGPLv2 or LGPLv3 (but not open-ended LGPLv2+);
# non-lib bits are GPLv3.
# pbrobinson points out that three files in the lib are actually
# marked GPL in headers, making library GPL, though we think this
# may not be upstream's intention. For now, marking library as
# GPL.
# License:	LGPLv2 or LGPLv3
License:	GPL v2 or GPL v3
Group:		Libraries
Source0:	https://launchpad.net/bamf/0.2/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	4271cd5979483f7e3a9bffc42fed6383
Patch0:		%{name}-build.patch
URL:		https://launchpad.net/bamf
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gobject-introspection-devel >= 0.6.7
%{?with_gtk2:BuildRequires:	gtk+2-devel >= 1:2.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0}
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	libgtop-devel >= 2.0
%{?with_gtk3:BuildRequires:	libwnck-devel >= 3}
%{?with_gtk2:BuildRequires:	libwnck2-devel >= 2.0}
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	vala
BuildRequires:	xorg-lib-libX11-devel
Requires:	glib2 >= 1:2.16.0
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
Requires:	glib2-devel >= 1:2.16.0
Requires:	libwnck2-devel >= 2.0

%description devel
This package contains header files for developing applications that
use BAMF with GTK+ 2.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących BAMF z GTK+ 2.

%package -n bamf3
Summary:	Application matching framework (GTK+ 3 library)
Summary(pl.UTF-8):	Szkielet do dopasowywania aplikacji (biblioteka GTK+ 3)
Group:		Libraries
Requires:	glib2 >= 1:2.16.0

%description -n bamf3
BAMF removes the headache of applications matching into a simple DBus
daemon and C wrapper library. Currently features application matching
at amazing levels of accuracy (covering nearly every corner case).
This package contains the bamf library built against GTK+ 3.

%description -n bamf3 -l pl.UTF-8
BAMF rozwiązuje problem dopasowywania aplikacji za pomocą prostego
demona DBus i biblioteki obudowującej w C. Aktualne możliwości to
dopasowywanie aplikacji z zaskakującym poziomem dokładności
(obejmującym prawie każdy przypadek brzegowy). Ten pakiet zawiera
bibliotekę bamf zbudowaną dla GTK+ 3.

%package -n bamf3-devel
Summary:	Development files for BAMF library (GTK+ 3 build)
Summary(pl.UTF-8):	Pliki programistyczne biblioteki BAMF (dla GTK+ 3)
License:	GPL v2 or GPL v3
Group:		Development/Libraries
Requires:	bamf3 = %{version}-%{release}
Requires:	glib2-devel >= 1:2.16.0
Requires:	libwnck-devel >= 3.0

%description -n bamf3-devel
This package contains libraries and header files for developing
applications that use BAMF with GTK+ 3.

%description -n bamf3-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących BAMF z GTK+ 3.

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
Requires:	glib2 >= 1:2.16.0

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

%build
# ../.././src/bamf-legacy-window.c: In function 'bamf_legacy_window_get_class_name':
# ../.././src/bamf-legacy-window.c:144:3: error: 'wnck_class_group_get_res_class' is deprecated (declared at /usr/include/libwnck-3.0/libwnck/class-group.h:89): Use 'wnck_class_group_get_id' instead [-Werror=deprecated-declarations]
CFLAGS="%{rpmcflags} -Wno-error=deprecated-declarations"

%define configuredir ..

%if %{with gtk2}
install -d build-gtk2
cd build-gtk2
%configure \
	--with-gtk=2 \
	--with-html-dir=%{_gtkdocdir} \
	--enable-gtk-doc
%{__make}
cd ..
%endif

%if %{with gtk3}
install -d build-gtk3
cd build-gtk3
%configure \
	--with-gtk=3 \
%if %{without gtk2}
	--with-html-dir=%{_gtkdocdir} \
	--enable-gtk-doc
%endif

%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with gtk2}
%{__make} install -C build-gtk2 \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbamf.la
%endif

%if %{with gtk3}
%{__make} install -C build-gtk3 \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbamf3.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n bamf3 -p /sbin/ldconfig
%postun	-n bamf3 -p /sbin/ldconfig

%if %{with gtk2}
%files
%defattr(644,root,root,755)
%doc TODO
%attr(755,root,root) %{_libdir}/libbamf.so.*.*.*
%ghost %{_libdir}/libbamf.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libbamf.so
%{_includedir}/libbamf
%{_pkgconfigdir}/libbamf.pc
# Installation of these was disabled in the 0.2.72 release commit,
# with no explanation - http://bazaar.launchpad.net/~unity-team/bamf/trunk/revision/374
#%{_libdir}/girepository-1.0/Bamf*.typelib
#%{_datadir}/gir-1.0/Bamf*.gir
#%{_datadir}/vala/vapi/Bamf*.vapi
%endif

%if %{with gtk3}
%files -n bamf3
%defattr(644,root,root,755)
%doc TODO
%attr(755,root,root) %{_libdir}/libbamf3.so.*.*.*
%ghost %{_libdir}/libbamf3.so.0

%files -n bamf3-devel
%defattr(644,root,root,755)
%{_libdir}/libbamf3.so
%{_includedir}/libbamf3
%{_pkgconfigdir}/libbamf3.pc
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libbamf
%endif

%files daemon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/bamfdaemon
%{_datadir}/dbus-1/services/org.ayatana.bamf.service
