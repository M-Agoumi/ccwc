#!/usr/bin/env python3

import sys
import argparse
from dataclasses import dataclass

@dataclass
class Flag:
    # Enum class is not needed for this implementation
    word_flag = False
    byte_flag = False
    line_flag = False
    char_flag = False
    max_line_flag = False
    no_flag = False


def print_help():
    print("Usage: ccwc [OPTION]... [FILE]...")
    print("Print newline, word, and byte counts for each FILE, and a total line if")
    print("more than one FILE is specified.  A word is a non-zero-length sequence of")
    print("printable characters delimited by white space.\n")
    print("With no FILE, read standard input.")
    print("the options below may be used to select which counts are printed, always in")
    print("the following order: newline, word, character, byte, maximum line length\n")
    print("Options:")
    print("  -c, --count                print the byte counts")
    print("  -m, --chars                print the character counts")
    print("  -l, --lines                print the newline counts")
    print("  -L, --max-line-length      print the length of the longest line")
    print("  -w, --words                print the word counts")
    print("      --help                 display this help and exit")
    print("      --version              output version information and exit\n")
    print("this is a copy of the GNU coreutils wc command made for practice purposes")
    print("Report bugs in the github repository: <https://www.github.com/m-agoumi/wc>")
    print("original wc command documentation: <https://www.gnu.org/software/coreutils/wc>")
    print("Written by Mohamed AGOUMI.")
    sys.exit(0)

def print_formatting(lines, words, chars, byte, file_name, max_line_length, flags):
    if flags.line_flag:
        print(f"{lines: >6}", end=" ")
    if flags.word_flag:
        print(f"{words: >6}", end=" ")
    if flags.char_flag:
        print(f"{chars: >6}", end=" ")
    if flags.byte_flag:
        print(f"{byte: >6}", end=" ")
    if flags.max_line_flag:
        print(f"{max_line_length: >6}", end=" ")
    
    print(f"{file_name}")


def print_version():
    print("ccwc 0.1")
    print("Copright (C) 2024 Free Software Foundation, Inc.")
    print("License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.")
    print("This is free software: you are free to change and redistribute it.")
    print("There is NO WARRANTY, to the extent permitted by law.")
    print("\nWritten by Mohamed AGOUMI.")
    sys.exit(0)


def process_arguments(arguments):
    parser = argparse.ArgumentParser(
        description="Print newline, word, and byte counts for each FILE, and a total line if more than one FILE is specified.",
        epilog="this is a copy of the GNU coreutils wc command made for practice purposes\n"
               "Report bugs in the github repository: <https://www.github.com/m-agoumi/wc>\n"
               "original wc command documentation: <https://www.gnu.org/software/coreutils/wc>\n"
               "Written by Mohamed AGOUMI."
    )
    parser.add_argument('-c', '--count', action='store_true', help='print the byte counts')
    parser.add_argument('-m', '--chars', action='store_true', help='print the character counts')
    parser.add_argument('-l', '--lines', action='store_true', help='print the newline counts')
    parser.add_argument('-L', '--max-line-length', action='store_true', help='print the length of the longest line')
    parser.add_argument('-w', '--words', action='store_true', help='print the word counts')
    parser.add_argument('--version', action='store_true', help='output version information and exit')
    parser.add_argument('files', nargs='*', help='list of files to read')

    args = parser.parse_args(arguments)

    flags = Flag()
    if args.version:
        print_version()
    elif not any([args.count, args.chars, args.words, args.lines, args.max_line_length]):
        flags.no_flag = True
    else:
        flags.char_flag = args.count
        flags.byte_flag = args.chars
        flags.line_flag = args.lines
        flags.word_flag = args.words

    return args.files, flags

def count_bytes(file_path, chunk_size=1024):
    try:
        with open(file_path, 'rb') as file:
            byte_data = b''
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                byte_data += chunk
        return byte_data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def count_stats(content):
    try:
        line_count = 0
        word_count = 0
        char_count = 0
        max_line_length = 0

        for line in content.splitlines():
            line_count += 1
            words = line.split()
            word_count += len(words)
            char_count += sum(len(word) + 1 for word in words) - 1  # Add 1 for each space between words, except the last one
            max_line_length = max(max_line_length, len(line))

        return line_count, word_count, char_count, max_line_length

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None, None




def process_file(file, flags):
    if file == sys.stdin:
        content = sys.stdin.buffer.read()
        file = ''
    else:
        content = count_bytes(file)

    lines = 0
    words = 0
    chars = 0
    bytes = 0
    max_line_length = 0

    if content:
        if flags.no_flag:
            flags.chars = flags.words = flags.lines = True
        lines, words, chars, max_line_length = count_stats(content)
        if flags.byte_flag:
            bytes = len(content)

        print_formatting(lines, words, chars, bytes, file, max_line_length, flags)
    else:
        print(f"Error: No data in file '{file}'.")

    return lines, words, chars, bytes, max_line_length

def main():
    total_liens = total_words = total_chars = total_bytes = total_max_line_length = 0
    files, flags = process_arguments(sys.argv[1:])

    if files:
        for file in files:
            lines, words, chars, bytes, max_lines = process_file(file, flags)
            total_liens += lines
            total_words += words
            total_chars += chars
            total_bytes += bytes
            if max_lines > total_max_line_length:
                total_max_line_length = max_lines

        if len(files) > 1:
            print_formatting(total_liens, total_words, total_chars, total_bytes, "total", total_max_line_length, flags)
    else:
        print("Error: No files specified.")
        print("Try 'ccwc --help' for more information.")
        sys.exit(1)

if __name__ == "__main__":
    main()
