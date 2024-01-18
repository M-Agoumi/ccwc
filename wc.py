#!/usr/bin/env python3
import sys

def print_help():
    print("Usage: wc.py [OPTION]... [FILE]...")

def count_all(file_name=None):
    # Read input line by line from standard input (pipeline)
    lines = 0
    words = 0
    bytes = 0
    if file_name:
        with open(file_name) as f:
            for line in f:
                # Process each line
                lines += line.count("\n")
                words += len(line.split())
                bytes += len(line)
    else:
        for line in sys.stdin:
            # Process each line
            lines += line.count("\n")
            words += len(line.split())
            bytes += len(line)
    
    return lines, words, bytes


def main():
    # lines, words, chars = count_all()
    # Check for command line arguments
    print_lines = print_words = print_bytes = False
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == '-h' or arg == '--help':
                print_help()
            elif arg == '-l':
                print_lines = True
            elif arg == '-w':
                print_words = True
            elif arg == '-c':
                print_bytes = True
            else:
                count_all(arg)
    else:
        print_lines = print_words = print_bytes = True
    # Print result
    if print_lines:
        print(f"      {lines}", end="")
    if print_words:
        print(f"      {words}", end="")
    if print_bytes:
        print(f"      {chars}", end="")
    print()


if __name__ == "__main__":
    main()
