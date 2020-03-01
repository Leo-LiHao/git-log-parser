import pytest
import copy

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
    rawHash = 'commit a88f72c7d2437e9cf16d0f076889419157e2c31b'
    parsedHash = 'a88f72c7d2437e9cf16d0f076889419157e2c31b'
    assert commit.commit_hash is None
    gitParser.parse_commit_hash(rawHash, commit)
    assert commit.commit_hash == parsedHash
    assert gitParser.commits == list()

def test_parse_commit_hash_multipleCalls(gitParser, commit):
    rawHash1 = 'commit 9f6debef550a3a30e5c6b422115f869733bc9431'
    rawHash2 = 'commit 86345b932949ffa466e41f763414da41cd8f6563'
    processedHash2 = '86345b932949ffa466e41f763414da41cd8f6563'
    assert commit.commit_hash is None
    gitParser.parse_commit_hash(rawHash1, commit)
    prev_commit = models.CommitData()
    prev_commit = copy.deepcopy(commit)
    commit = gitParser.parse_commit_hash(rawHash2, commit)
    assert not (commit == prev_commit)
    assert gitParser.commits[0] == prev_commit
    assert commit.commit_hash == processedHash2

def test_parse_author(gitParser, commit):
    assert commit.author == models.Author()
    rawAuthor = 'Author: Győri György <Gygy$@email.test>'
    parsedAuthor = models.Author('Győri György', 'Gygy$@email.test')
    gitParser.parse_author(rawAuthor, commit)
    assert commit.author == parsedAuthor

def test_parse_date(gitParser, commit):
    assert commit.commit_date is None
    rawDate = 'Date:   Sat Apr 13 9:8:7 2000 +0500'
    parsedDate = '2000-04-13 09:08:07+05:00'
    gitParser.parse_date(rawDate, commit)
    assert str(commit.commit_date) == parsedDate

def test_parse_commit_msg(gitParser, commit):
    assert commit.message is None
    rawMessage = 'Updated travis'
    parsedMessage = 'Updated travis'
    gitParser.parse_commit_msg(rawMessage, commit)
    assert commit.message == parsedMessage

def test_change_id(gitParser, commit):
    assert commit.change_id is None
    rawChangeId = '    Change-Id:135456(.84515)'
    parsedChangeId = '135456(.84515)'
    gitParser.parse_change_id(rawChangeId, commit)
    assert commit.change_id == parsedChangeId

def test_prase_lines_correct_input(gitParser, commit):
    #TODO
    pass

def test_prase_lines_unexpected_input(gitParser):
    with pytest.raises(models.UnexpectedLineError):
        gitParser.parse_lines('Suprise!')