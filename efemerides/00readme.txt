00readme.txt   5-oct-2017 by Alois Treindl TEST

This download area contains the Free Edition of the SWISS EPHEMERIS.

About the Swiss Ephemeris:

Swiss Ephemeris is a software toolbox for programmers of astrological
software. It is of little use for a non-programmer

The test programs SWETEST.EXE and SWEWIN.EXE come
with it as demonstration programs for programmers to show them how
they can call the SE functions.
swetest.exe can be used to compute complete natal horoscopes as textual
output.

Programmers all over the world have started to build SE into their
software. 

SE ist built according to the highest standards of precision available
in astronomical data. It is able to reproduce the ephemeris data in
astronomical standard books up to the last printed digit.

Detailed information is available at http://www.astro.com/swisseph
or in the documentation files included in the distribution.

Description of files:
=====================
While we have made available many single files, so that they can
be viewed directly in a browser, it is much more convenient to
download the files in '.zip' or '.gz' format. Except for the single
asteroid files, all files in this area available in one of the 'zip' or
'gz' archives and should be downloaded in the archived form for higher
speed.

LICENSE.TXT
	The Swiss Ephemeris is published currently under GPL, and
	alternatively under Swiss Ephemeris Professional License,
	You must read and accept the license before you download any files.

swe_unix_src_2.01.00.tar.gz
	The release of the Swiss Ephemeris source code.
	A simple Makefile to create a Unix library is included.
	The unix-readable of the doc directory are also included.
	The release number is sometimes changing frequently when we are in an
	active development phase.
	Sometimes several releases will be available at the same time.
	It is usually best to take the one with the highest release number.

	Release 1.67 was the last with the old IAU precission model 1976
	(Lieske), old nutation model 1980 (Wahr). It is preserved
	in swe_unix_src_1.67.tar.gz and sweph_1.67.zip

sweph.zip
	The complete Swiss Ephemeris package for Windows (32bit),
	except the ephemeris data files.
	See online documentation at http://www.astro.com/swisseph
	or in the doc directory for more details.
	Small sample programs and build-projects are included for
	- Visual C++ .net 2003
	- Visual Basic 5.0 
	- Delphi 32-bit
Note: Visual Basic files may not have been updated and
tested, as we currently do not possess a working copy of VB at Astrodienst.

swephzip.txt
	overview of content of the sweph.zip package

swe_vs2015_project.zip
	contains Visual Studio 2015 solution file sweph.sln and subdirectory 'projects'
	with vcxproj files for the various parts of this solution.
	Should be unpacked after unpacking sweph.zip, within the 'src' directory and
	can be used to build the various dlls and executables on Windows.

src/*
	unpacked source archive, identical to content of archive file above,
	with the highest release number.


doc/*	
	swisseph.doc	Feature Documentation, MS Word format
	swephprg.doc	Programmer's Documentation, MS Word format
	[there are also PDF and HTML versions of these files]
	graphical labels (Corel Draw 7.0 and GIF versions)
	All files are also contained in the swe_src_..gz archive.

ephe	Directory with binary ephemeris files. 

jplfiles	Directory with files in JPL ephemeris format. This directory
	can only be accessed via ftp, not via http.
	MD5 checksums of the files:
	1ef6191b614b2b854adae8675b1b981f  de200.eph
	ec1c8a3fa8e097fcf57d5be4a756da3c  de403.eph
	645ca2e99ba6b9e3d6ef57319f487867  de404.eph
	90fa86dc17c4e8b8874711fa1531a648  de405.eph
	1ef768440cc1617b6c8ad27a9a788135  de406e.eph
	4fa7a6ab035f9d120b6d9684448bd606  de406.eph
	2ea11439e97497b1e1313cbb973eaa41  de414.eph
	d2d10039f285d0ae45a591bcec997df6  de421.eph
	00361541acbb65f0fc8241cfa82091df  de422.eph
	707c4262533d52d59abaaaa5e69c5738  de430.eph
	fad0f432ae18c330f9e14915fbf8960a  de431.eph
	All files except de406e.eph come directly from JPL and have only
	been renamed, but not changed.

programs
	A directory containing sample and utility programs for Windows:
	swewin32.zip 
		zipped archive containing swewin.exe.
		This is a small Windows application which computes complete
		horoscopes, including houses and asteroids. 
		It runs on Windows 95/98/NT/2000/XP

	swetest.exe
		executable Swiss Ephemeris program.
		This is a 32-bit Console mode application.
		To get information about the many features of this program, run
		swetest -? > out.txt
		and print the file out.txt, or view it with your text editor.
		This is just a sample to demonstrate the precision of the
		ephemeris, and to show the typical use of a few cally.

	swetest.zip
		zipped version of swetest.exe for faster download.

	unzip.exe
		A Windows utility to unzip .ZIP files.
		If you have WinZip on your system, just double click on the
		the downloaded ZIP files and Winzip will take care of unzipping.
		Otherwise you can use unzip.exe: open a command (DOS) Windows,
		type the command: unzip sweph.zip
		and the zip-archive will be unpacked in a local directory named 
		'sweph'.

It is possible to use SWEWIN and SWETEST without the ephemeris files.
If the program finds no ephemeris files, it uses the builtin 
analytical ephemeris which provides "only" a precision of 0.1 arc seconds
for the planets and 3" for the Moon.
No asteroids will be available, and no barycentric option can be used.

The SWISS EPHEMERIS can be licensed by programmers to include this 
calculation engine in their software. More information is found at
http://www.astro.com/swisseph/

Depending on your application the free edition under the Public License
may apply, or you may have to acquire a professional license for a fee.

CDROM distribution:
===================
There is no longer any CDROM. All parts of SE are available here in the
download area.


Legal restrictions
==================
Read LICENSE.TXT

Mailing list
============
We maintain a mailing list which we use to send developers information about
updates, bugs etc.
If you want to have your name added to this mailing list, please
visit groups.yahoo.com/swisseph

Feedback
========
We welcome any suggestions and comments you may have about the Swiss Ephemeris.
Please email to swisseph@groups.yahoo.com

If you want your feedback distributed to all members of the swisseph
mailing list, please subscribe to http://groups.yahoo.com/group/swisseph/



Java-Version:
=============
Thomas Mack has ported the Swiss Ephemeris library to Java.
His work can be found at:  http://www.th-mack.de/international/download/
If you use it for commercial or for non-open-source purposes, please
be aware that GNU Public License of Swiss Ephemeris 
also applies for the Java version, besides any additional requirements
which may be defined by Thomas Mack.

Numerical Integrator
====================
the numerical integrator to prepare swisss ephemeris files is not in a state
fit for publication.

There is a file numint.tar.gz which contains all the parts needed for it,
so that those who want to look can have a look at it.
The permission to use it is currently 'read source code' only.

Directory contrib
=================
It contains open source code and applications using the Swiss Ephemeris.
See the reeadme file in directory contrib for more details.
