Project Changelog
=================

Release 1.1.0 (6 Mar 2019)
--------------------------

New:
* Added ability to return null rates if rate data is missing, rather than throw an exception.

Bug fixes:
* ADF15 parser now handles a greater variation of rate files.
* Beam emission rate methods were reading the stopping rate files, not the emission files.


Release 1.0.1 (1 Oct 2018)
--------------------------

Bug fixes:
* Cherab package would fail if Raysect structures were altered due to using prebuilt c files. Cython is now always used to rebuild against the installed version of raysect. Cython is therefore now a dependency.


Release 1.0.0 (28 Sept 2018)
----------------------------

Initial public release.
