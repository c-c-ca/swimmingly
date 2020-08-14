import os
import re
import pandas as pd

FIRST_NAME_COL = 2
EVENT_COL = 5
MALES = {"Michael", "David", "Josh"}  # names found exclusively in men's events

sq_field = '(".*?").*?'
dq_field = '(""".*"""|".*?").*?'
regex = sq_field * 8 + dq_field + sq_field * 7


def rename():
    '''
    Provide more descriptive names for .csv files provided from top rank event search.
    '''
    requested = []

    for entry in os.scandir("./raw_data"):
        with open(entry.path, 'r') as f:
            lines = f.readlines()
            names = set(line.split(",")[FIRST_NAME_COL]
                        .strip(' "') for line in lines)
            gender = "men" if names.intersection(MALES) else "women"
            event = lines[1].split(",")[EVENT_COL]
            distance, stroke, course = event.strip('="').lower().split()
            new_name = "_".join([gender, distance, stroke, course]) + ".csv"
            os.rename(entry.path, "./raw_data/" + new_name)
            requested.append([gender, distance, stroke, course])
    with open('requested.txt', 'w') as f:
        f.write(str(requested))


def trim(col):
    return col.strip('="\n')


def reformat_header(row):
    return "\t".join([trim(col) for col in row.split(",")] + ["gender"]) + "\n"


def reformat_row(row, gender):
    return "\t".join([col.strip('"') for col in re.search(f'.*?{regex}', row).groups()] + [gender]) + "\n"


def clean():
    '''
    Reformat .csv files for data analysis.
    '''
    for entry in os.scandir("./raw_data"):
        gender = "m" if entry.name.split("_")[0] == "men" else "f"
        out = ""
        with open(entry.path, 'r') as f:
            out += reformat_header(f.readline())
            for line in f:
                row = reformat_row(line, gender)
                if len(row.split('\t')) != 17:
                    continue
                out += row
        with open(f"./data/{entry.name}", 'w') as outf:
            outf.write(out)


def combine():
    dfs = []
    for entry in os.scandir("./data"):
        dfs.append(pd.read_csv(entry.path, sep="\t"))

    pd.concat(dfs).to_csv("top_times.csv", sep="\t", index=False)


def main():
    rename()
    clean()
    combine()


main()
