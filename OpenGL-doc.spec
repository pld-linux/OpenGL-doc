# NOTE: more up-to-date docs in PDF format can be found at
#	http://opengl.org/documentation/specs/
#	but they are non-distributable
Summary:	OpenGL Programmers Documentation - manuals
Summary(pl.UTF-8):	Dokumentacja dla programistów OpenGL - podręczniki man
Name:		OpenGL-doc
Version:	1.2.1
Release:	1
Epoch:		1
License:	freely distributable (SGI)
Group:		Documentation
Source0:	ftp://oss.sgi.com/projects/ogl-sample/download/ogl-sample.20000807.tgz
# Source0-md5:	2427a75a3c4345ac248119405f85e447
Source1:	http://www.opengl.org/resources/libraries/glut/glut-3.7.tar.gz
# Source1-md5:	dc932666e2a1c8a0b148a4c32d111ef3
Patch0:		%{name}-macros.patch
URL:		http://opengl.org/
# headers for man generation
BuildRequires:	OpenGL-devel >= 1.2.1
BuildRequires:	OpenGL-GLU-devel >= 1.3
BuildRequires:	OpenGL-GLX-devel >= 1.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenGL API documentation.

%description -l pl.UTF-8
Dokumentacja API OpenGL.

%package man
Summary:	OpenGL API documentation in man format
Summary(pl.UTF-8):	Dokumentacja API OpenGL w formacie man
Group:		Documentation
Obsoletes:	XFree86-OpenGL-doc
Conflicts:	glut-devel < 3.7-19

%description man
OpenGL API documentation from Siligon Graphics. This package contains
man pages for OpenGL 1.2.1 API, GLU 1.3 API (GL Utility Library) and
GLX 1.3 API (OpenGL extensions to the X Server).

%description man -l pl.UTF-8
Pakiet zawiera opracowaną przez firmę Silicon Graphics dokumentację
biblioteki graficznej OpenGL. Strony podręcznika man opisują
podstawowe funkcje OpenGL 1.2.1, GLU 1.3 (GL Utility Library) oraz GLX
1.3 (rozszerzenia 3D dla serwera X).

%package html
Summary:	OpenGL Programmers Documentation - HTML version
Summary(pl.UTF-8):	Dokumentacja dla programistów OpenGL - wersja HTML
Group:		X11/XFree86
Obsoletes:	XFree86-OpenGL-doc-html

%description html
OpenGL API documentation from Siligon Graphics. This set contains HTML
documentation for OpenGL 1.2.1 API, GLU 1.3 API (GL Utility Library)
and GLX 1.3 API (OpenGL extensions to the X Server).

%description html -l pl.UTF-8
Pakiet zawiera opracowaną przez firmę Silicon Graphics dokumentację
biblioteki graficznej OpenGL. Dokumentacja HTML opisuje podstawowe
funkcje OpenGL 1.2.1, GLU 1.3 (GL Utility Library) oraz GLX 1.3
(rozszerzenia 3D dla serwera X).

%prep
%setup -q -c -a1
%patch0 -p0

# hack
install -d usr/include
ln -s ../../main/tools/include usr/include/make
ln -s /usr/include/GL usr/include/GL

%build
%{__make} -C main/doc/man \
	ROOT=`pwd`

install -d html/{gl,glu,glx}
cp main/doc/man/mangl/html/*.html html/gl
cp main/doc/man/manglu/html/*.html html/glu
cp main/doc/man/manglx/html/*.html html/glx

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man3

installman() {
	awk '/^\.SH NAME/ { getline; sub(/^(\.B \"|\\fB)/, ""); sub(/\\\(em.*/, ""); gsub(/,/, ""); print; }' $1 | ( read bname names
		install $1 $RPM_BUILD_ROOT%{_mandir}/man3/${bname}.3gl
		for f in $names ; do
			echo ".so ${bname}.3gl" > $RPM_BUILD_ROOT%{_mandir}/man3/${f}.3gl
		done
	)
}
for f in main/doc/man/{mangl,manglu,manglx}/standard/*.3gl main/doc/man/manglw/*.3gl ; do
	installman $f
done

%{__make} -C glut-3.7/man/glut install.man \
	DESTDIR=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}/man3

%clean
rm -rf $RPM_BUILD_ROOT

%files man
%defattr(644,root,root,755)
%{_mandir}/man3/gl[A-Z]*.3gl*
%{_mandir}/man3/glu[A-Z]*.3gl*
%{_mandir}/man3/GLw*.3gl*
%{_mandir}/man3/glut*.3xglut*
%{_mandir}/man3/intro.3xglut*

%files html
%defattr(644,root,root,755)
%doc html/*
