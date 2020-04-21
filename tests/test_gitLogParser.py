import pytest
import copy
import json
import subprocess

from gitlogparser import parser
from gitlogparser import models


@pytest.fixture
def gitParser():
    gitParser = parser.GitLogParser()
    return gitParser

@pytest.fixture
def commit():
    commit = models.CommitData()
    return commit

def test_empty_starting_list(gitParser):
    assert gitParser.commits == list()

def test_parse_commit_hash_firstCall(gitParser, commit):
    raw_hash = 'commit a88f72c7d2437e9cf16d0f076889419157e2c31b'
    parsed_hash = 'a88f72c7d2437e9cf16d0f076889419157e2c31b'
    assert commit.commit_hash is None
    gitParser.parse_commit_hash(raw_hash, commit)
    assert commit.commit_hash == parsed_hash
    assert gitParser.commits == list()

def test_parse_commit_hash_multipleCalls(gitParser, commit):
    raw_hash1 = 'commit 9f6debef550a3a30e5c6b422115f869733bc9431'
    raw_hash2 = 'commit 86345b932949ffa466e41f763414da41cd8f6563'
    processed_hash2 = '86345b932949ffa466e41f763414da41cd8f6563'
    assert commit.commit_hash is None
    gitParser.parse_commit_hash(raw_hash1, commit)
    prev_commit = models.CommitData()
    prev_commit = copy.deepcopy(commit)
    commit = gitParser.parse_commit_hash(raw_hash2, commit)
    assert not (commit == prev_commit)
    assert gitParser.commits[0] == prev_commit
    assert commit.commit_hash == processed_hash2

def test_parse_author(gitParser, commit):
    assert commit.author == models.Author()
    raw_author = 'Author: Győri György <Gygy$@email.test>'
    parsed_author = models.Author('Győri György', 'Gygy$@email.test')
    commit.author = gitParser.parse_author(raw_author)
    assert commit.author == parsed_author

def test_parse_date(gitParser, commit):
    assert commit.commit_date is None
    raw_date = 'Date:   Sat Apr 13 9:8:7 2000 +0500'
    parsed_date = '2000-04-13 09:08:07+05:00'
    gitParser.parse_date(raw_date, commit)
    assert str(commit.commit_date) == parsed_date

def test_parse_commit_msg(gitParser, commit):
    assert commit.message is None
    raw_message = 'Updated travis'
    parsed_message = 'Updated travis'
    gitParser.parse_commit_msg(raw_message, commit)
    assert commit.message == parsed_message

def test_change_id(gitParser, commit):
    assert commit.change_id is None
    raw_change_id = '    Change-Id:135456(.84515)'
    parsed_change_id = '135456(.84515)'
    gitParser.parse_change_id(raw_change_id, commit)
    assert commit.change_id == parsed_change_id

def test_prase_lines_correct_input(gitParser, commit):
    raw_lines ="""commit 50fa0692b0e33c420c712cec72c9eb09cd060505
Author: ßäŁámØn Pista <testerererererer@stuff.hu>
Date:   Fri Aug 28 19:20:01 2002 +0400

    Did some funky stuff

                """
    parsed_commit = models.CommitData(
        '50fa0692b0e33c420c712cec72c9eb09cd060505',
        models.Author('ßäŁámØn Pista', 'testerererererer@stuff.hu'),
        'Did some funky stuff',
        '2002-08-28 19:20:01+04:00',
        )
    commit = gitParser.parse_lines(raw_lines)
    assert commit == parsed_commit

# the parser doesn't raise the exception anymore, but it still might later
"""def test_prase_lines_unexpected_input(gitParser):
    with pytest.raises(models.UnexpectedLineError):
        gitParser.parse_lines('Suprise!')"""

def test_dummy_commit_singleDir():
    class dummyArgs(object):
        def __init__(self, dir):
            self.directory = dir
    subprocess.run('git clone https://github.com/gaborantal/git-log-parser.git', cwd='./tests', shell=True)
    subprocess.run('git checkout 86e684ddfb16f98f09211bb8087b6d321b25c145', cwd='./tests/git-log-parser', shell=True)
    args = dummyArgs('./tests/git-log-parser')
    parser.get_log(args)
    with open('./tests/correct_result.json', 'r', encoding='utf-8') as f:
        with open('./logdata_new.json', 'r', encoding='utf-8') as f2:
            correct_result = json.load(f)
            current_result = json.load(f2)
            assert correct_result == current_result
    
def test_dummmy_commit_mDir():
    class dummyArgs(object):
        def __init__(self, dir):
            self.directory = None
            self.multiple_directories = dir
    args = dummyArgs('./tests')
    parser.get_log(args)
    print(subprocess.run('ls'))
    with open('./tests/correct_result.json', 'r', encoding='utf-8') as f:
        with open('./logdata_git-log-parser.json', 'r', encoding='utf-8') as f2:
            correct_result = json.load(f)
            current_result = json.load(f2)
            assert correct_result == current_result