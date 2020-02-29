import copy
import datetime
import re
import subprocess
import os
import json

from . import models


def parse_datetime(date_string):
    """Simple method to parse string into datetime object if possible.

    Parse string into datetime object if possible.
    :param date_string: Date as a string.
    :return: date as a datetime object, if there are no errors.
             if so, original string is returned.
    """
    FORMAT_STRING = "%a %b %d %H:%M:%S %Y %z"
    try:
        return datetime.datetime.strptime(date_string, FORMAT_STRING)
    except ValueError:
        return date_string


def get_log(args):
    # attempt to read the git log from the user specified directory, if it fails, notify them and leave the function
    if args.directory:
        try:
            gitLogResult = subprocess.run(['git', 'log'], capture_output=True, text=True, cwd=args.directory)
            create_json(gitLogResult.stdout)
            return
        except Exception as ex:
            print('The specified directory could not be opened.')
            return

    else:
        try:
            # only the top level directories are needed, so if the inner for finishes the function returns
            for walkResults in os.walk(args.multiple_directories):
                # call the csv function for every subdirectory
                for dir in walkResults[1]:
                    # no exception is handeled here, since only the previously extracted directories are being opened
                    gitLogResult = subprocess.run(['git', 'log'], capture_output=True, text=True,
                                                  cwd=args.multiple_directories + '/' + dir)
                    create_json(gitLogResult.stdout, dir)
                return

        except Exception as ex:
            print('The specified directory could not be opened.')
            return


# process the mined data and store it in JSON
def create_json(git_log_result, attempted_directory=None):
    logParser = GitLogParser()
    logParser.parse_lines(git_log_result)
    # print commits
    print('Date'.ljust(14) + ' ' + 'Author'.ljust(15) + '  ' + 'Email'.ljust(20) + '  ' + 'Hash'.ljust(
        8) + '  ' + 'Message'.ljust(20))
    print("=================================================================================")
    for commit in logParser.commits:
        if commit.message is None:
            commit.message = 'No message provided'
        print(str(commit.commit_date) + '  ' + commit.author.name.ljust(15) + '  ' + commit.author.email.ljust(
            20) + '  ' + commit.commit_hash[:7].ljust(8) + '  ' + commit.message)
    # specify which directory has been mined, only if there were multiple options
    with open('logdata_' + (attempted_directory if attempted_directory else 'new' )+ '.json', 'w',
        encoding='utf-8') as f:
        json.dump(logParser, f, indent=4, cls=CommitEncoder, sort_keys=True)

class GitLogParser(object):

    def __init__(self):
        self.commits = []

    def parse_lines(self, raw_lines):
        commit = models.CommitData()
        # iterate lines and save
        for nextLine in raw_lines.splitlines():
            if len(nextLine.strip()) == 0:
                # ignore empty lines
                pass

            elif bool(re.match('commit', nextLine, re.IGNORECASE)):
                # commit xxxx
                if commit.commit_hash is not None:
                    # new commit, reset object
                    self.commits.append(copy.deepcopy(commit))
                    commit = models.CommitData()
                commit.commit_hash = re.match('commit (.*)',
                                              nextLine, re.IGNORECASE).group(1)

            elif bool(re.match('merge:', nextLine, re.IGNORECASE)):
                # Merge: xxxx xxxx
                pass

            elif bool(re.match('author:', nextLine, re.IGNORECASE)):
                # Author: xxxx <xxxx@xxxx.com>
                m = re.compile('Author: (.*) <(.*)>').match(nextLine)
                commit.author.name = m.group(1)
                commit.author.email = m.group(2)

            elif bool(re.match('date:', nextLine, re.IGNORECASE)):
                # Date: xxx
                m = re.compile(r'Date:\s+(.*)$').match(nextLine)
                commit.commit_date = parse_datetime(m.group(1))

            elif bool(re.match('    ', nextLine, re.IGNORECASE)):
                # (4 empty spaces)
                # Here we just save the header of the commit message
                if commit.message is None:
                    commit.message = nextLine.strip()
                if bool(re.match('    change-id: ', nextLine,
                                 re.IGNORECASE)):
                    commit.change_id = re.compile('    Change-Id:\s*(.*)').match(
                        nextLine).group(1)
            else:
                print('ERROR: Unexpected Line: ' + nextLine)

# a new encoder is necessary to make the json dumb creation clean and readable
class CommitEncoder(json.JSONEncoder):
    def default(self, obj):
        # creates a list out of the mined commits
        if isinstance(obj, GitLogParser):
            encoded_logs = list()
            for commit in obj.commits:
                encoded_logs.append(commit.to_json())
            return encoded_logs
        return super(CommitEncoder, self).default(obj)

