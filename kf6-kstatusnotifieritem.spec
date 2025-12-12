#
# Conditional build:
%bcond_with	tests		# build with tests
#
# TODO:
# - runtime Requires if any

%define		kdeframever	6.21
%define		qtver		6.7.0
%define		kfname		kstatusnotifieritem
Summary:	Status notifier item
Name:		kf6-%{kfname}
Version:	6.21.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	80966140965ca6ccc60cc1b228111d54
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kwindowsystem-devel >= %{kdeframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
%requires_eq_to Qt6Core Qt6Core-devel
Requires:	kf6-kwindowsystem >= %{kdeframever}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kstatus notifier item.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DBUILD_PYTHON_BINDINGS=OFF \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}6 --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}6.lang
%defattr(644,root,root,755)
%{_libdir}/libKF6StatusNotifierItem.so.*.*
%ghost %{_libdir}/libKF6StatusNotifierItem.so.6
%{_datadir}/dbus-1/interfaces/kf6_org.kde.StatusNotifierItem.xml
%{_datadir}/dbus-1/interfaces/kf6_org.kde.StatusNotifierWatcher.xml
%{_datadir}/qlogging-categories6/kstatusnotifieritem.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KStatusNotifierItem
%{_libdir}/cmake/KF6StatusNotifierItem
%{_libdir}/libKF6StatusNotifierItem.so
