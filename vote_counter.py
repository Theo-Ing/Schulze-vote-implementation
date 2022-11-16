#!/usr/bin/env python

from schulze import *
from numpy import ndarray
import tkinter
from tkinter import filedialog, simpledialog
import os


def _build_report(data: Schulze, res: list, tot: list, ties: list, d: ndarray, p: ndarray, vacancies: int):
    """
    Build string to be used for report
    :param data: Schulze object containing election data
    :param res: Results of election (only vacancies)
    :param tot: Total reports of election
    :param ties: List of ties
    :param d: Pairwise matrix of election
    :param p: Strength matrix of election
    :param vacancies: Number of available vacancies
    :return: String of total report
    """
    report = """ELECTION RESULTS:
-----------------------------------
The algorithms used for calculating the reports of this election are
described in: https://en.wikipedia.org/wiki/Schulze_method

"""
    report += f'Number of vacancies to be filled: {vacancies}\n\n'

    report += f'Winners in order of preference:\n'
    for i, winner in enumerate(res):
        report += f'{i+1}. {winner}\n'
    report += "\n"

    report += f'Total order of preference:\n'
    for i, candidate in enumerate(tot):
        report += f'{i+1}. {candidate}\n'
    report += "\n"

    if ties:
        report += "The following ties were detected:\n"
        for tie in ties:
            report += f'{tie[0]} - {tie[1]}\n'
        report += "\n"
    else:
        report += "No ties were found \n\n"

    report += "-----------------------------------\n"
    report += "Below are in depth reports:\n\n"

    report += "Indexing used for pairwise and strength matrices:\n"
    for index, name in data.index_to_names.items():
        report += f'{index} - {name}\n'
    report += "\n"

    report += "Pairwise matrix:\n"
    report += repr(d)
    report += "\n\n"

    report += "Strength matrix:\n"
    report += repr(p)

    return report


def main():
    # Choose file paths
    root = tkinter.Tk()
    root.withdraw()  # use to hide tkinter window
    currdir = os.getcwd()
    position_name = simpledialog.askstring("Vote Counter", "Name of position:").replace(" ", "_")
    vacancies = simpledialog.askinteger("Vote Counter", "Number of available vacancies:")
    raw_data_file = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Select the raw data file')
    report_dir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Select directory for report file')
    report_file = f'{report_dir}/{position_name}_results.txt'

    data = Schulze(raw_data_file)
    res, tot, d, p, ties = data.get_results(vacancies)

    report = _build_report(data, res, tot, ties, d, p, vacancies)
    with open(report_file, "w") as f:
        f.write(report)


if __name__ == '__main__':
    main()
