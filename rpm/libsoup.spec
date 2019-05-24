Name:       libsoup

Summary:    Soup, an HTTP library implementation
Version:    2.54.1
Release:    1
Group:      System/Libraries
License:    LGPLv2
URL:        https://git.merproject.org/mer-core/libsoup
Source0:    %{name}-%{version}.tar.xz
Patch0:     disable-gtk-doc.patch
Patch1:     revert-constructor-init.patch
Requires:   glib-networking
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0) >= 2.38.0
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  gobject-introspection-devel
BuildRequires:  glib-networking
BuildRequires:  intltool >= 0.25

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
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Libsoup is an HTTP library implementation in C. This package allows
you to develop applications that use the libsoup library.


%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
%{summary}.


%prep
%setup -q -n %{name}-%{version}/libsoup

# disable-gtk-doc.patch
%patch0 -p1
%patch1 -p1

%build
echo "EXTRA_DIST = missing-gtk-doc" > gtk-doc.make
USE_GNOME2_MACROS=1 NOCONFIGURE=1 gnome-autogen.sh

%configure --disable-static \
    --without-gnome \
    --disable-vala

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

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
