Name:   fatinstall
Version:    8.3.7
Release:    1
Summary:    Software Manager for flatpaks - A fork of mintinstall

Source0:    https://github.com/horizonlinux/FatInstall/archive/refs/tags/latest.tar.gz
Licence:    GPL-3.0
BuildArch:  noarch

Requires:   html2text
Requires:   python3

%description
FatInstall is a Software Manager designed for any Linux Distribution.
It comes with fast installing speeds, and clean UI. Its only packaging
format are flatpaks. FatInstall is a fork of Linux Mint mintinstall.

%files
/usr/share/*
/usr/lib/*
/usr/bin/*

%changelog
* Tue Apr 15 2025 Microwave <github.com/Micro856> - 8.3.7
- Create RPM for fatinstall
