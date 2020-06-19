import argparse
from . import parser


def main():
    # create the -dir and -mDir arguments
    arg_parser = argparse.ArgumentParser(description='Parse a git repos log into json')
    group = arg_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-dir', '--directory', metavar='', help='Extracts the specified directory as a repo')
    group.add_argument('-mDir', '--multiple_directories', metavar='', help='Extracts every subdirectory as a repo')
    arg_parser.add_argument('-GHT', '--github_token', default=None ,metavar='', help='Your github access token, if specified, the parser will get the line/file changes of each commit')
    arg_parser.add_argument('-nm', '--no_merge', action='store_true', default=False, help='A value to decide wether to get merge commit data or not')
    args = arg_parser.parse_args()
    parser.get_log(args)


if __name__ == '__main__':
    main()
