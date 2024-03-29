Name:       libsoup

Summary:    Soup, an HTTP library implementation
Version:    2.74.3
Release:    1
License:    LGPLv2
URL:        https://github.com/sailfishos/libsoup
Source0:    %{name}-%{version}.tar.xz
Patch0:     0001-fix-canonicalize-filename.patch
Requires:   glib-networking
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0) >= 2.38.0
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(libpsl)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  gobject-introspection-devel
BuildRequires:  glib-networking
BuildRequires:  gettext
BuildRequires:  meson

%description
Libsoup is an HTTP library implementation in C. It was originally part
of a SOAP (Simple Object Access Protocol) implementation called Soup, but
the SOAP and non-SOAP parts have now been split into separate packages.

libsoup uses the Glib main loop and is designed to work well with GTK
applications. This enables GNOME applications to access HTTP servers
on the network in a completely asynchronous fashion, very similar to
the Gtk+ programming model (a synchronous operation mode is also
supported for those who want it).

%package devel
Summary:    Header files for the Soup library
Requires:   %{name} = %{version}-%{release}

%description devel
Libsoup is an HTTP library implementation in C. This package allows
you to develop applications that use the libsoup library.

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}

%description doc
%{summary}.

%prep
%setup -q -n %{name}-%{version}/libsoup
%patch0 -p1

%build
%meson -Dgssapi=disabled \
       -Dntlm=disabled \
       -Dbrotli=disabled \
       -Dgnome=false \
       -Dsysprof=disabled \
       -Dvapi=disabled

%meson_build

%install
%meson_install

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} \
        README NEWS AUTHORS

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%{_datarootdir}/locale/*/LC_MESSAGES/*.mo
%{_libdir}/lib*.so.*
%{_libdir}/girepository-1.0/Soup*2.4.typelib

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/libsoup-2.4
%{_includedir}/libsoup-2.4/libsoup
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/Soup*2.4.gir

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}
