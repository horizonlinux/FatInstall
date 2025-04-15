Name:   fatinstall
Version:    8.3.7
Release:    1
Summary:    Software Manager for flatpaks - A fork of mintinstall

Source0:    https://github.com/horizonlinux/FatInstall/archive/refs/tags/latest.tar.gz
License:    GPL-3.0-only
BuildArch:  noarch

Requires:   html2text
Requires:   python3

%description
FatInstall is a Software Manager designed for any Linux Distribution.
It comes with fast installing speeds, and clean UI. Its only packaging
format are flatpaks. FatInstall is a fork of Linux Mint mintinstall.

%prep
%setup -q

%build
make

%files
/usr/share/*
/usr/lib/*
/usr/bin/*

%changelog
* Tue Apr 15 2025 Microwave <github.com/Micro856> - 8.3.7
- Create RPM for fatinstall
