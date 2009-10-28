%define lib_major 0
%define libname %mklibname %{name}-private %{lib_major}
%define libnamedev %mklibname -d %{name}-private
%define startup_notification_version 0.4

%define oname mutter
%define olibname %mklibname %{oname}-private %{lib_major}
%define olibnamedev %mklibname -d %{oname}-private

%define name moblin-%{oname}
%define version 2.27.5
%define moblin_version 0.0
%define sversion %{version}_%{moblin_version}
%define rel 1
%define release %mkrel %{moblin_version}.%{rel}

Summary: Mutter window manager
Name: %{name}
Version: %{version}
Release: %{release}
URL: http://www.moblin.org
Source0: http://git.moblin.org/cgit.cgi/%{oname}/snapshot/%{oname}-%{sversion}.tar.bz2
Patch0: metacity-glib-log-handler.patch
License: GPLv2+
Group: Graphical desktop/GNOME
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: zenity
BuildRequires: libglade2.0-devel
BuildRequires: libGConf2-devel >= 1.1.9
BuildRequires: startup-notification-devel >= %{startup_notification_version}
BuildRequires: libcanberra-devel
BuildRequires: libgtop2.0-devel
BuildRequires: libxinerama-devel
BuildRequires: libxcomposite-devel
BuildRequires: libxdamage-devel
BuildRequires: libxtst-devel
BuildRequires: libmesaglu-devel
BuildRequires: GConf2
BuildRequires: zenity
BuildRequires: intltool
BuildRequires: gnome-doc-utils
BuildRequires: libcanberra-devel
BuildRequires: gobject-introspection-devel gir-repository
BuildRequires: clutter-devel >= 1.0

Conflicts: %{oname}
Requires: %{libname}


%description
Mutter is a simple window manager that integrates nicely with 
GNOME 2.

%package -n %{libname}
Summary:        Libraries for Mutter
Group:          System/Libraries
Conflicts:	%{olibname}

%description -n %{libname}
This package contains libraries used by Mutter.

%package -n %{libnamedev}
Summary:        Libraries and include files with Mutter
Group:          Development/GNOME and GTK+
Requires:       %name = %{version}
Requires:		%{libname} = %{version}
Provides:		%{name}-devel = %{version}-%{release}
Provides:		lib%{name}-private-devel = %{version}-%{release}
Conflicts:		%{olibnamedev}

%description -n %{libnamedev}
This package provides the necessary development libraries and include 
files to allow you to develop with Mutter.


%prep
%setup -q -n %{oname}-%{sversion}
%patch0 -p1 -b .metacity-glib-log-handler

%build
NOCONFIGURE=nil ./autogen.sh
%configure2_5x --with-clutter --disable-xinerama --without-introspection --disable-static
%make

%install
rm -rf $RPM_BUILD_ROOT %oname.lang
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

%find_lang %{oname} 

%clean
rm -rf $RPM_BUILD_ROOT

%define schemas %oname

%preun
%preun_uninstall_gconf_schemas %{schemas}

%files -f %{oname}.lang
%defattr(-,root,root)
%doc README COPYING NEWS HACKING 
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%{_datadir}/applications/%oname.desktop
%{_datadir}/gnome/wm-properties/%oname-wm.desktop
%{_datadir}/%oname
%dir %_libdir/%oname
%dir %_libdir/%oname/plugins
%_libdir/%oname/plugins/default.so
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{lib_major}*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc ChangeLog
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_libdir}/pkgconfig/*

