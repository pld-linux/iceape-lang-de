%define	_lang	de
%define	_reg	AT
%define	_lare	%{_lang}-%{_reg}
Summary:	German resources for Iceape
Summary(pl.UTF-8):	Niemieckie pliki językowe dla Iceape
Name:		iceape-lang-%{_lang}
Version:	1.1.9
Release:	1
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		I18n
Source0:	http://releases.mozilla.org/pub/mozilla.org/seamonkey/releases/%{version}/contrib-localized/seamonkey-%{version}.%{_lare}.langpack.xpi
# Source0-md5:	b4bd83078cbfaa610897c691a5d5e4f4
Source1:	http://www.mozilla-enigmail.org/download/release/0.95/enigmail-de-0.95.xpi
# Source1-md5:	7b363f97e6873f44c835735a7b02620f
Source2:	gen-installed-chrome.sh
URL:		http://www.seamonkey-project.org/
BuildRequires:	unzip
Requires(post,postun):	iceape >= %{version}
Requires(post,postun):	textutils
Requires:	iceape >= %{version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_chromedir	%{_datadir}/iceape/chrome

%description
German resources for Iceape.

%description -l pl.UTF-8
Niemieckie pliki językowe dla Iceape.

%prep
%setup -q -c
%{__unzip} -o -qq %{SOURCE1}
install %{SOURCE2} .
./gen-installed-chrome.sh locale chrome/{%{_reg},%{_lare},%{_lang}-unix,enigmail-DE}.jar \
	> lang-%{_lang}-installed-chrome.txt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_chromedir}

install chrome/{%{_reg},%{_lare},%{_lang}-unix,enigmail-DE}.jar $RPM_BUILD_ROOT%{_chromedir}
install lang-%{_lang}-installed-chrome.txt $RPM_BUILD_ROOT%{_chromedir}
cp -r defaults dictionaries searchplugins $RPM_BUILD_ROOT%{_datadir}/iceape
rm $RPM_BUILD_ROOT%{_datadir}/iceape/dictionaries/LICENSE.TXT

# rebrand locale for iceape
cd $RPM_BUILD_ROOT%{_chromedir}
unzip %{_lare}.jar locale/%{_lare}/branding/brand.dtd locale/%{_lare}/branding/brand.properties \
	locale/%{_lare}/communicator/search/default.htm
sed -i -e 's/SeaMonkey/Iceape/g;' locale/%{_lare}/branding/brand.dtd \
	locale/%{_lare}/branding/brand.properties locale/%{_lare}/communicator/search/default.htm
zip -0 %{_lare}.jar locale/%{_lare}/branding/brand.dtd locale/%{_lare}/branding/brand.properties \
	locale/%{_lare}/communicator/search/default.htm
rm -f locale/%{_lare}/branding/brand.dtd locale/%{_lare}/branding/brand.properties \
	locale/%{_lare}/communicator/search/default.htm

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/iceape-chrome+xpcom-generate

%postun
%{_sbindir}/iceape-chrome+xpcom-generate

%files
%defattr(644,root,root,755)
%{_chromedir}/%{_reg}.jar
%{_chromedir}/%{_lare}.jar
%{_chromedir}/%{_lang}-unix.jar
%{_chromedir}/enigmail-DE.jar
%{_chromedir}/lang-%{_lang}-installed-chrome.txt
%{_datadir}/iceape/searchplugins/*
%{_datadir}/iceape/defaults/messenger/%{_reg}
%{_datadir}/iceape/defaults/profile/%{_reg}
%{_datadir}/iceape/dictionaries/*
