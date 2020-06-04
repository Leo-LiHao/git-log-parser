[![Build Status](https://travis-ci.org/gaborantal/git-log-parser.svg?branch=master)](https://travis-ci.org/gaborantal/git-log-parser)

GitLogParser
============

Python script to parse 'git log'

## Usage
Script is intented to be used via commandline. Depending on the commandine arguments it can either parse a single directory (-dir), or every repository within the given directory (-mDir).
Each option needs either a full or relative route to the directory. 

	> gitlogparser -dir ./yourRepo
	> gitlogparser -dir /home/something/somewhere/yourRepo
	> gitlogparser -mDir /home/dirWithMultipleRepos
	> gitlogparser -mdir ..

From the mined data a json file will be created. If only a single directory was mined the json's name will be logdata_new.json, but if -mDir was given, each created file will be named after the mined repository in the following manner: logdata_*YourMinedRepo*.json

If the -GHT argument is specified, the commit diff-s (line/file changes) will also be mined. This is optional, since it takes a while, and requires a GitHub access token.

The console will only display errors. In the case of a succesfull execution the files will be created in the same directory where the gitlogparser command was issued.

## Example
### git log output:
	...
	commit 9f6debef550a3a30e5c6b422115f869733bc9431
	Author: Mosolygó <mosolygo.iskolai@gmail.com>
	Date:   Fri Feb 28 15:56:59 2020 +0100

		Added the ability to choose repo directory
		
		argParser in a temporary place
		
		GitLogParser class slightly modified, so it can correctly read the new input

	commit bfffe073ed7d98ae4be7e15968d16fa85e1ead62
	Author: Gábor Antal <antal@inf.u-szeged.hu>
	Date:   Tue Sep 3 17:07:34 2019 +0200

		Reimplemented gitLogParse.py
		
		In this commit, classes are introduced in order to ease parsing
		git commits. Corresponding objects created after parsing the log file.
		These objects are then rewritten into a usable, automatizable structure.

	commit eee66b0b623c2dc3a99485a6d7428ad032a0bc5a
	Author: Keleti Márton <tejes@hac.hu>
	Date:   Wed Nov 15 16:10:32 2017 +0100

		Added newline to file endings
	...

### json's content:
	...
    {
        "author": {
            "email": "mosolygo.iskolai@gmail.com",
            "name": "Mosolygó"
        },
        "change_id": null,
        "commit_date": "2020-02-28 15:56:59+01:00",
        "commit_hash": "9f6debef550a3a30e5c6b422115f869733bc9431",
        "deletions": null,
        "files_changed": null,
        "insertions": null,
        "message": "Added the ability to choose repo directory\nargParser in a temporary place\nGitLogParser class slightly modified, so it can correctly read the new input"
    },
    {
        "author": {
            "email": "antal@inf.u-szeged.hu",
            "name": "Gábor Antal"
        },
        "change_id": null,
        "commit_date": "2019-09-03 17:07:34+02:00",
        "commit_hash": "bfffe073ed7d98ae4be7e15968d16fa85e1ead62",
        "deletions": null,
        "files_changed": null,
        "insertions": null,
        "message": "Reimplemented gitLogParse.py\nIn this commit, classes are introduced in order to ease parsing\ngit commits. Corresponding objects created after parsing the log file.\nThese objects are then rewritten into a usable, automatizable structure."
    },
    {
        "author": {
            "email": "tejes@hac.hu",
            "name": "Keleti Márton"
        },
        "change_id": null,
        "commit_date": "2017-11-15 16:10:32+01:00",
        "commit_hash": "eee66b0b623c2dc3a99485a6d7428ad032a0bc5a",
        "deletions": null,
        "files_changed": null,
        "insertions": null,
        "message": "Added newline to file endings"
    },
	...