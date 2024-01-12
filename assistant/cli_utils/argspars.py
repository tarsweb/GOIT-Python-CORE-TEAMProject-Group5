import argparse

parser = argparse.ArgumentParser(prog='assistant')

parser.add_argument('command', nargs='*', help='description help')
parser.add_argument('--foo', type=str, nargs='*', default="", help='FOO!')