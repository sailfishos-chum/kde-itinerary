%global  kde_version 25.04.3
%global  kf6_version 6.18.0
%define _metainfodir /usr/share/metainfo

%bcond_with vulkan

Name:       kde-itinerary
# Newer versions contain commit dd4a6203, which forces KPublicTransport 25.07.71 which we can't compile.
# See the KPublicTransport package for details.
Version:    25.04.3
Release:    1%{?dist}
License:    Apache-2.0 and BSD-3-Clause and CC0-1.0 and LGPL-2.0-or-later
Summary:    Digital travel assistant with a priority on protecting your privacy
Url:        https://apps.kde.org/itinerary/
#Source0:    https://invent.kde.org/pim/%%{name}/-/archive/v%%{version}/%%{name}-v%%{version}.tar.bz2
Source0:    %{name}-%{version}.tar.bz2

Patch0:     0000-build-for-sailfishos.patch

BuildRequires: desktop-file-utils
BuildRequires: kf6-extra-cmake-modules >= %kf6_version
BuildRequires: gcc-c++
BuildRequires: kf6-rpm-macros
#BuildRequires: kf6-qqc2-desktop-style
BuildRequires: kf6-qqc2-breeze-style

BuildRequires: pkgconfig(Qt6Core)
BuildRequires: qt6-qtbase-private-devel

# binaries/tools:
BuildRequires: python3-base
BuildRequires: sailfish-svg2png
BuildRequires: pkgconfig(shared-mime-info)

###
### required dependencies
###
# find_package(Qt6 ${QT_MIN_VERSION} REQUIRED COMPONENTS Test Quick Positioning QuickControls2)
#BuildRequires: qt6-qtdeclarative-devel
#BuildRequires: qt6-qtquickcontrols2-devel
#BuildRequires: qt6-qtpositioning-devel
BuildRequires: pkgconfig(Qt6Quick)
BuildRequires: pkgconfig(Qt6QuickControls2)
BuildRequires: pkgconfig(Qt6Positioning)
Buildrequires: pkgconfig(Qt6PositioningQuick)

# find_package(KF6 ${KF_MIN_VERSION} REQUIRED COMPONENTS I18n CoreAddons Contacts Notifications CalendarCore Holidays UnitConversion)
BuildRequires: kf6-kcoreaddons-devel
BuildRequires: kf6-ki18n-devel
BuildRequires: kf6-kcontacts-devel
BuildRequires: kf6-knotifications-devel
BuildRequires: kf6-kcalendarcore-devel
BuildRequires: kf6-kholidays-devel
BuildRequires: kf6-kunitconversion-devel

# find_package(KF6KirigamiAddons 0.11.40 REQUIRED)
BuildRequires: kf6-kirigami-addons-devel

# Patched for Android/mobile
BuildRequires: kf6-kirigami-devel
BuildRequires: kf6-kcolorscheme-devel

# find_package(KF6 ${KF_MIN_VERSION} REQUIRED COMPONENTS DBusAddons QQC2DesktopStyle WindowSystem)
BuildRequires: kf6-kdbusaddons-devel
#BuildRequires: qqc2-breeze-style
BuildRequires: kf6-kwindowsystem-devel

# find_package(KF6 ${KF_MIN_VERSION} REQUIRED COMPONENTS Archive Kirigami Prison)
BuildRequires: kf6-karchive-devel
BuildRequires: kf6-prison-devel

# find_package(KOSMIndoorMap CONFIG REQUIRED)
BuildRequires: kde-kosmindoormap-devel

# find_package(KPim6Itinerary 5.23.0 CONFIG REQUIRED)
BuildRequires: kde-kitinerary-devel

# find_package(Qt6Keychain CONFIG REQUIRED)
# find_package(LibIcal 3.0)
# find_package(ZLIB REQUIRED)
BuildRequires: qt6-qtkeychain-devel
BuildRequires: pkgconfig(libical)
BuildRequires: pkgconfig(zlib)

###
### optional dependencies
###
BuildRequires: pkgconfig(Qt6Location)
#BuildRequires: qt6-qtmultimedia-devel
BuildRequires: kf6-kfilemetadata-devel
#BuildRequires: kf6-kio-devel
BuildRequires: kf6-kitemmodels-devel

BuildRequires: kde-kpublictransport-devel
BuildRequires: kde-kpkpass-devel
BuildRequires: kde-khealthcertificate-devel
BuildRequires: kde-kopeninghours-devel
BuildRequires: kde-kmime-devel

## Required by KF6Contacts
BuildRequires: kf6-kconfig-devel
## Required by KF6CoreAddons
BuildRequires: kf6-kcodecs-devel

%if %{with vulkan}
BuildRequires: vulkan-headers
Recommends:    vulkan
%endif


# Optional:

#BuildRequires: kf6-kcodecs-devel
#BuildRequires: kf6-kcrash-devel

#BuildRequires: qt6-qtlocation-pos-geoclue
#BuildRequires: qt6-qtlocation-pos-geoclue2
#BuildRequires: qt6-qtlocation-pos-positionpoll

#BuildRequires:  kf6-kcoreaddons-devel
#BuildRequires:  kf6-ki18n-devel
#BuildRequires:  kf6-solid-devel

# Runtime:
# * QML module 'QtLocation' is a runtime dependency.
# * QML module 'QtMultimedia' is a runtime dependency.
# * QML module 'QtPositioning' is a runtime dependency.
# * QML module 'org.kde.kitemmodels' is a runtime dependency.
# * QML module 'org.kde.prison' is a runtime dependency.
# * QML module 'org.kde.prison.scanner' is a runtime dependency.

Requires:   qt-runner-qt6
Requires:   kf6-kirigami
Requires:   kf6-prison
Requires:   kf6-kitemmodels
Requires:   kf6-qqc2-desktop-style
Recommends: qt6-qtlocation
Recommends: qt6-qtpositioning

%description
KDE Itinerary is a digital travel assistant with a priority on protecting
your privacy.

%if "0%{?_chum}"
Title: KDE Itinerary
Type: desktop-application
PackagedBy: nephros
Categories:
  - Maps
  - Utility
Custom:
  Repo: https://invent.kde.org/pim/itinerary
PackageIcon: https://apps.kde.org/app-icons/org.kde.itinerary.svg
Screenshots:
  - https://cdn.kde.org/screenshots/itinerary/kde-itinerary-timeline.png
  - https://cdn.kde.org/screenshots/itinerary/kde-itinerary-boardingpass.png
Links:
  Homepage: %{url}
  Help: https://community.kde.org/KDE_PIM/KDE_Itinerary
%endif


%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%cmake_kf6 \
  -DSAILFISHOS=ON \
  %{nil}

%cmake_build

%install
%cmake_install

%find_lang %{name}

sed -i -e 's@^Exec=itinerary@Exec=qt-runner /usr/bin/itinerary@g' \
   %{buildroot}%{_datadir}/applications/org.kde.itinerary.desktop
printf 'X-Nemo-Single-Instance=no\nX-Nemo-Application-Type=no-invoker\n'
   >> %{buildroot}%{_datadir}/applications/org.kde.itinerary.desktop
printf '\n[X-Sailjail]\nSandboxing=Disabled\n' \
   >> %{buildroot}%{_datadir}/applications/org.kde.itinerary.desktop

desktop-file-install --delete-original       \
  --dir %{buildroot}%{_datadir}/applications             \
   %{buildroot}%{_datadir}/applications/*.desktop

# generate some icons
for size in 86 108 128 172 256 512 1024; do
install -d %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/
sailfish_svg2png -z 1.0 -s 1 1 1 1 1 1 ${size} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/ %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/
done

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/*/apps/*.png

%{_kf6_datadir}/knotifications6/itinerary.notifyrc
%{_kf6_datadir}/qlogging-categories6/*.categories

%{_kf6_qmldir}/org/kde/solidextras/*
%{_kf6_plugindir}/kfilemetadata/kfilemetadata_itineraryextractor.so

# do we need these?
%{_kf6_libdir}/libSolidExtras.so
%exclude %{_kf6_metainfodir}/org.kde.itinerary.appdata.xml
