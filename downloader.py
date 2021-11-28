"""This is a script that downloads IB Physics past year papers
from the website ibdocuments.com.

Only past year papers later than 2016 can be downloaded due to
the naming conventions used.
"""

# Standard library modules
import os

# Local modules
import helpers


FILE_PATH = os.path.dirname(__file__)
ROOT_DIR = os.path.realpath(os.path.join(FILE_PATH, '..'))
INPUT_PATH = os.path.join(FILE_PATH, 'input.csv')

# Get list of papers in dict form from csv file
papers = helpers.csv2dict(INPUT_PATH)

# Iterate over list of papers
for paper in papers:
    r,pname = helpers.getPYP(paper)
    error = helpers.downloadPYP(r, pname, paper)
    if error:
        papername = helpers.paperNameGen(paper)
        raise Exception("No such paper: {}".format(papername))
    else:
        helpers.renamePYP(paper, ROOT_DIR)

