import argparse
import sys


def echo_precompiler():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-file', help='Output file')
    parser.add_argument('-i', '--input-file', help='Input file')
    parser.add_argument('-V', '--version', help='Show version', action='store_true')
    args = parser.parse_args()
    if args.version:
        print('Echo preparser v1.0.0')
        print('Waow, such a great program! ^^')
        sys.exit()

    with open(args.input_file, 'r') as fin, open(args.output_file, 'w') as fout:
        fout.write(fin.read())


if __name__ == '__main__':
    echo_precompiler()
