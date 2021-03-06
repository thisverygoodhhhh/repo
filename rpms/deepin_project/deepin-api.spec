%global project dde-api
%global repo %{project}

%global _commit f93dbd7db26ff2bc312f86659c5cf089a522129e
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-api
Version:        3.1.2
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Go-lang bingding for dde-daemon
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-api
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  bzr
BuildRequires:  git
BuildRequires:  gcc-go
BuildRequires:  gtk3-devel
BuildRequires:  gdk-pixbuf2-xlib-devel
BuildRequires:  cairo-devel
BuildRequires:  libXi-devel
BuildRequires:  libcroco-devel
BuildRequires:  libcanberra-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libgudev-devel
BuildRequires:  poppler-glib-devel
BuildRequires:  deepin-gir-generator
BuildRequires:  deepin-go-lib
BuildRequires:  deepin-go-dbus-factory
BuildRequires:  golang-github-BurntSushi-xgb-devel
BuildRequires:  golang-github-BurntSushi-xgbutil-devel
BuildRequires:  golang-github-go-fsnotify-fsnotify-devel
BuildRequires:  golang-github-alecthomas-kingpin-devel
Requires:       deepin-desktop-base
Requires:       rfkill
Provides:       %{repo}%{?_isa} = %{version}-%{release}
Obsoletes:      %{repo}%{?_isa} < %{version}-%{release}

%description
Go-lang bingding for dde-daemon

%package devel
Summary:        Development package for %{name}

%description devel
Header files and libraries for %{name}

%prep
%setup -q -n %{repo}-%{_commit}

sed -i 's|/usr/lib|%{_libexecdir}|' misc/*services/*.service \
    misc/systemd/system/deepin-shutdown-sound.service \
    thumbnails/gtk/gtk.go

sed -i 's|libdir|LIBDIR|g' Makefile

install -d %{buildroot}%{gopath}/src/pkg.deepin.io/dde/api
cp -r * %{buildroot}%{gopath}/src/pkg.deepin.io/dde/api/

%build
export GOPATH="$(pwd)/build:%{gopath}"
#make build-dep
go get github.com/disintegration/imaging \
    github.com/howeyc/fsnotify \
    launchpad.net/gocheck \
    gopkg.in/alecthomas/kingpin.v2
make

%install
export GOPATH="$(pwd)/build:%{gopath}"
%make_install SYSTEMD_LIB_DIR="/usr/lib" LIBDIR="/libexec"

%files
%{_libexecdir}/%{name}/
%{_unitdir}/*.service
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/icons/hicolor/*/actions/*

%files devel
%{gopath}/src/pkg.deepin.io/dde/api/

%changelog
* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 3.1.2-1.gitf93dbd7
- Update to 3.1.2
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.0.16.1-1.gitcfdb295
- Update to 3.0.16.1
* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.16-1
- Update to version 3.0.16
* Sun Dec 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.15-1
- Update to version 3.0.15
* Wed Dec 07 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.14-2
- Changed compilation procedure
* Wed Sep 28 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.14-1
- Initial package build
