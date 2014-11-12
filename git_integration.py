__author__ = 'kevin'

import argparse
import subprocess
import os
import re

def main():
    args = parse_args()

    # git show --pretty="format:" --name-only <COMMIT SHA1>
    os.chdir(args.repo_root)
    proc = subprocess.Popen(['git',
                             'show',
                             '--pretty=format:',
                             '--name-only',
                             args.commit],
                            stdout=subprocess.PIPE)

    changed_files = proc.stdout.read().decode(encoding='UTF-8')
    changed_files = changed_files.strip().split('\n')

    for changed_file in changed_files:
        #git show <COMMIT SHA1> -- <FILE NAME>
        proc = subprocess.Popen(['git',
                                 'show',
                                 args.commit,
                                 '--',
                                 changed_file],
                                stdout=subprocess.PIPE)

        changed_file_diff = proc.stdout.read().decode(encoding='UTF-8')

        diff_lines = changed_file_diff.splitlines()

        modified_functions = list()
        reached_diff = False

        for diff_line in diff_lines:
            if not reached_diff:
                if diff_line.startswith('@@'):
                    reached_diff = True
                    idx = 0

                    # @@ -12,35 +12,4 @@ void greet(int);
                    # @@ from-file-line-numbers to-file-line-numbers @@
                    # @@ start,count start,count @@
                    # >>> re.search(r"(@@ )([-+]{1}\d+,\d+)( )([-+]{1}(\d+),(\d+))( @@)(.*)", text).group(4)
                    # '+12,4'
                    # >>> re.search(r"(@@ )([-+]{1}\d+,\d+)( )([-+]{1}(\d+),(\d+))( @@)(.*)", text).group(5)
                    # '12'
                    # >>> re.search(r"(@@ )([-+]{1}\d+,\d+)( )([-+]{1}(\d+),(\d+))( @@)(.*)", text).group(6)
                    # '4'
                    match = re.search(r"(@@ )([-+]\d+,\d+)( )([-+](\d+),(\d+))( @@)(.*)", diff_line)
                    diff_start_line = int(match.group(5))
                    diff_count_line = int(match.group(6))

            else:
                if diff_line.startswith('+') or diff_line.startswith('-'):
                    function_for_line = find_function(diff_start_line + idx, changed_file)

                    if function_for_line:
                        if function_for_line not in modified_functions:
                            modified_functions.append(function_for_line)

                idx += 1

    for function_name in modified_functions:
        print(function_name)


def find_function(line_number, file):
    with open(file) as f:
        file_lines = f.readlines()

    file_lines = file_lines[:line_number]

    file_fragment = "\n".join(file_lines)

    # find all the function definitions
    functions = re.findall(r"\w+\s+\w+\s*\(\s*\w+\s+\w+\s*\)", file_fragment)

    last_function = functions[-1]

    return last_function


def parse_args():

    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-c", "--commit", help="")
    parser.add_argument("-d", "--diff", help="")
    parser.add_argument("-rr", "--repo_root", help="")

    return parser.parse_args()


if __name__ == "__main__":
    main()