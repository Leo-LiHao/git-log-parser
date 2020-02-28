import argparse
from . import parser


def main():
    # create the -dir and -mDir arguments
    arg_parser = argparse.ArgumentParser(description='Parse a git repos log into a csv')
    group = arg_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-dir', '--directory', metavar='', help='Extracts the specified directory as a repo')
    group.add_argument('-mDir', '--multiple_directories', metavar='', help="Extracts every subdirectory as a repo")
    args = arg_parser.parse_args()
    parser.get_log(args)


if __name__ == '__main__':
    main()
