flairstats
==========

This project started as a simple script fetching the latest comments
on a subreddit and compiling their authors' flairs into a bar chart.

Version 2 of flairstats will implement more features, in particular :

* getting the statistics for a given period of time or number of comments
* getting statistics about unique users posting
* getting statistics about the activity during the day of flair or a user
* have a ranking of the most used flairs overall and in function of the time
* taking snapshots of the current data
* data backup in a dbm file
* unlike v1, also take in account new posts

Project status
--------------

The development branch can be fount 
[here](https://github.com/dopsi/flairstats/tree/v2-dev).

Features are :

- [x] Comments flairs presence statistics (as in V1)
- [x] Comments unique users flairs statistics
- [x] Post authors flairs presence statistics
- [x] Post flairs presence statistics
- [x] Posts unique users flairs statistics
- [ ] Provide graphs
- [ ] Pretty HTML output

Versionning
-----------

this project follows the semantic versionning guidelines provided at
[semver.org](http://semver.org/) with versions numbered as 
`major.minor.revision` :

* `major` is increased after a backwards incompatible api change.
* `minor` is increased after a backwards compatible api change.
* `revision` is increased after a change with no effect on the api.

any version with `major` being 0 *should* not be considered stable nor
should its api.

Versions history can be found in the file ChangeLog.md

Licence
=======

This software and all related documents are licenced under the
MIT licence (see `LICENCE` file for more informations).

Author
======

Copyright 2016 Simon Doppler <dopsi.dev@gmail.com>
