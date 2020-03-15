import copy
import datetime
import re
import subprocess
import os
import json
import concurrent.futures

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
#both types of directory mining happens here, the bool variable decides which will be choosen
def mine_logs(dir):
    #saves the home directory
    base_dir = os.getcwd()

    #preps the input to be of correct format
    if dir[0] == '.' and dir[1] !='.':
        dir.replace('.', base_dir, 1)
    elif dir[0] =='.' and dir[1] =='.':
        dir = base_dir + '/' +dir
    #opens the target dir, mines it then returns the result
    os.chdir(dir)

    git_result = subprocess.getoutput('git log')

    os.chdir(base_dir)

    return git_result

def mine_stats(before_commit, after_commit):
    return subprocess.getoutput('git diff ' + before_commit + ' ' + after_commit + ' --shortstat')

def get_log(args):
    # attempt to read the git log from the user specified directory, if it fails, notify them and leave the function
    if args.directory:
        try:
            create_json(mine_logs(args.directory), args.directory)
            return
        except Exception as ex:
            print(ex)
            print('The specified directory could not be opened.')
            return

    else:
        try:
            # only the top level directories are needed, so if the inner for finishes the function returns
            for walkResults in os.walk(args.multiple_directories):
                # call the csv function for every subdirectory
                for dir in walkResults[1]:
                    # no exception is handeled here, since only the previously extracted directories are being opened
                    # hidden directories are ignored
                    if dir[0] != '.':
                        create_json(mine_logs(args.multiple_directories + '/' + dir), args.multiple_directories + '/' + dir, dir)
                return

        except Exception as ex:
            print(ex)
            print('The specified directory could not be opened.')
            return


# process the mined data and store it in JSON
def create_json(git_log_result, current_path, attempted_directory=None):
    logParser = GitLogParser()
    try:
        logParser.parse_lines(git_log_result)
        #the update data extraction is a separate function, since it assumes that every commit has aleady been mined
        logParser.get_update_data(current_path)
    except models.UnexpectedLineError as ex:
        if 'fatal: not a git repository' in str(ex):
            if attempted_directory:
                print(attempted_directory + ' is not a git repository, no json file will be created for it!')
            else:
                print('The directory given is not a git repository, no json file will be created!')
        else:
            print(ex)
    # print commits
    """print('Date'.ljust(14) + ' ' + 'Author'.ljust(15) + '  ' + 'Email'.ljust(20) + '  ' + 'Hash'.ljust(
        8) + '  ' + 'Message'.ljust(20))
    print("=================================================================================")
    for commit in logParser.commits:
        if commit.message is None:
            commit.message = 'No message provided'
        print(str(commit.commit_date) + '  ' + commit.author.name.ljust(15) + '  ' + commit.author.email.ljust(
            20) + '  ' + commit.commit_hash[:7].ljust(8) + '  ' + commit.message)"""
    # specify which directory has been mined, only if there were multiple options
    if logParser.commits:
        print('creating json ' + ('for ' + attempted_directory if attempted_directory else '' ))
        with open('logdata_' + (attempted_directory if attempted_directory else 'new' )+ '.json', 'w',
            encoding='utf-8') as f:
            json.dump(logParser, f, indent=4, cls=CommitEncoder, sort_keys=True)
            

class GitLogParser(object):

    def __init__(self):
        self.commits = []

    def get_update_data(self, location):
        
        #saves the home directory
        base_dir = os.getcwd()

        #preps the input to be of correct format
        if location[0] == '.' and location[1] !='.':
            location.replace('.', base_dir, 1)
        elif location[0] =='.' and location[1] =='.':
            location = base_dir + '/' +location
        #opens the target dir, mines it then returns the result
        os.chdir(location)
        
        
        #get the stats on multple threads to increase performance
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list()
            for i in range(len(self.commits)-2, -1, -1):
                results.append(executor.submit(mine_stats, self.commits[i+1].commit_hash, self.commits[i].commit_hash))
        #wait for every stat    
            concurrent.futures.wait(results)
        #this is needed since the commits are in a different order then the results
            current_commit = len(self.commits)-2
            for r in results:
                stat_dict = dict()
                stats = r.result().split()
                #since all 3 stats can be 0 n which case they are not displayed, this loop creates a dict based on the existing ones
                for j in range(1, len(stats)):
                    if stats[j-1].isdigit():
                        stat_dict[stats[j]] = int(stats[j-1])
                #if a part of a statistic is missing the keys vary, but they always start the same way
                for key in stat_dict:
                    if key.startswith('file'):
                        self.commits[current_commit].files_changed = stat_dict[key]
                
                    if key.startswith('insertion'):
                        self.commits[current_commit].insertions = stat_dict[key]

                    if key.startswith('deletion'):
                        self.commits[current_commit].deletions = stat_dict[key]
                current_commit = current_commit - 1

        os.chdir(base_dir)

            
    def parse_commit_hash(self, nextLine, commit):
        # commit xxxx
        if commit.commit_hash is not None:
            # new commit, reset object
            self.commits.append(copy.deepcopy(commit))
            commit = models.CommitData()
        commit.commit_hash = re.match('commit (.*)',
                                      nextLine, re.IGNORECASE).group(1)

        return commit
                

    def parse_author(self, nextLine):
        # Author: xxxx <xxxx@xxxx.com>
        m = re.compile('Author: (.*) <(.*)>').match(nextLine)
        return models.Author(m.group(1), m.group(2))

    def parse_date(self, nextLine, commit):
        # Date: xxx
        m = re.compile(r'Date:\s+(.*)$').match(nextLine)
        commit.commit_date = parse_datetime(m.group(1))

    def parse_commit_msg(self, nextLine, commit):
        # (4 empty spaces)
        if commit.message is None:
            commit.message = nextLine.strip()
        else:
            commit.message = commit.message + os.linesep + nextLine.strip()
        
        if 'merge' in commit.message or 'Merge' in commit.message:
            commit.isMerge = True

    def parse_change_id(self, nextLine, commit):
        commit.change_id = re.compile(r'    Change-Id:\s*(.*)').match(
                nextLine).group(1)

    def parse_lines(self, raw_lines, commit = None):
        if commit is None:
            commit = models.CommitData()
        # iterate lines and save
        for nextLine in raw_lines.splitlines():
            #print(nextLine)
            if len(nextLine.strip()) == 0:
                # ignore empty lines
                pass

            elif bool(re.match('commit', nextLine, re.IGNORECASE)):
                commit = copy.deepcopy(self.parse_commit_hash(nextLine, commit))

            elif bool(re.match('merge:', nextLine, re.IGNORECASE)):
                # Merge: xxxx xxxx
                pass

            elif bool(re.match('author:', nextLine, re.IGNORECASE)):
                commit.author = self.parse_author(nextLine)

            elif bool(re.match('date:', nextLine, re.IGNORECASE)):
                self.parse_date(nextLine, commit)

            elif bool(re.match('    ', nextLine, re.IGNORECASE)):
                self.parse_commit_msg(nextLine, commit)

            elif bool(re.match('    change-id: ', nextLine, re.IGNORECASE)):
                self.parse_change_id(nextLine, commit)
            
            else:
                raise models.UnexpectedLineError(nextLine)
            
        if len(self.commits) != 0:
            self.commits.append(commit)


            
        return commit

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

