"""Helper functions for downloader.py"""


# Standard library modules
import csv
import os
import os.path

# Third party modules
import requests


def csv2dict(filename):
    """Converts contents in a CSV file to a list of dictionaries.

    The dictionary will have the following keys:
    1. level -- for the level of the paper, i.e. HL or SL
    2. year -- for the year the exam was conducted
    3. month -- for the month of exam was conducted
    4. tz -- for the timezone. In May, two papers are held, 
             one for each timezone.
             - May papers have 2 timezones (TZ1 and TZ2)
             - Nov papers have 1 timezone (TZ0)
    5. kind -- for the kind of document to be extracted,
               i.e. question paper (qp) or mark scheme (ms)

    Args:
        filename(csv)

    Returns:
        list
    """

    # import csv

    # Read csv file
    with open(filename, newline='') as csvfile:
        rows = csv.DictReader(csvfile)

        # Create a list of papers.
        # Each paper is a dictionary of paper details.
        papers = []

        # Create a dictionary of paper details 
        # for each row extracted from the csvreader 
        for row in rows:
            paper = {}

            paper["level"] = row["level"]  # i.e. HL or SL
            paper["year"] = row["year"]
            paper["month"] = row["month"].lower()  # i.e. May or Nov
            paper["tz"] = row["tz"]  # timezone, e.g. 1 or 2 (for papers in May)
            paper["number"] = row["number"]  # i.e. paper 1, 2, or 3
            paper["kind"] = row["kind"].lower()  # e.g. ms (for mark scheme)

            papers.append(paper)
            
    return papers


def downloadPYP(r, pname, paper, path=None):
    """Download past year paper from web request
    
    Args:
        r(web request)
        pname(str): the name of the paper downloaded from the website
        paper(dict): this is necessary as the pname does not include much details
        path: the filepath to save the paper
        
    Returns:
        error code(int)
    
    """

    # import os
    
    # Download if page can be found
    if r.text.find('Error 404 - Page Not Found') == -1:
        if path == None:
            # If path to store the paper is not specified,
            # use current working directory as the path
            path = os.getcwd()

        path = os.path.join(path, pname)
        open(pname, "wb").write(r.content)
    
    # Raise error if page cannot be found.
    # Perhaps there is no such paper, or an error in the name
    else:
        # newname = paperNameGen(paper)
        # raise Exception("No such paper: {}".format(newname))
        return 1

    return 0


def getPYP(paper):
    """Extracts past year papers from ibdocuments.com

    Args:
        paper(dict): paper details
            level(str): HL or SL
            number(str): Paper 1, 2, or 3
            year(str): the year of the paper
            month(str): the month in e.g. May
            tz(str): the timezone
            kind(str): the kind of paper e.g. qp for question paper

    Returns:
        web request, str
    """

    # import requests
    
    # Change all strings to lowercase to standardize for easier checking
    paper["level"] = paper["level"].lower()
    paper["month"] = paper["month"].lower()
    paper["kind"] = paper["kind"].lower()

    # Check that inputs comply to standards, e.g. there is no paper held in Jan
    check_value = sanity_check(paper)

    # Exit if input does not comply to standards
    if check_value > 0:
        return None

    # Generate name of paper used by the website.
    # This will be used in the url and also in the name of the paper downloaded
    pname = webNameGen(paper)

    # First letter of month must be capitalized when used in url
    paper["month"] = paper["month"].capitalize()

    year = paper["year"]
    month = paper["month"]

    if paper['month'] == 'Nov':
        month = 'November'

    # Set up url
    url0 = "https://www.ibdocuments.com/IB%20PAST%20PAPERS%20-%20YEAR/"
    url = (url0 + year + "%20Examination%20Session/" + month + "%20"
           + year + "%20Examination%20Session/Experimental%20sciences/"
           + pname)

    # For now, this year and month has an anomaly in the naming
    if (month == 'May' and year == '2016'):
        url = (url0 + year + "%20Examination%20Session/" + month + "%20"
           + year + "%20Examination%20Session/Group%204%20-%20Experimental%20Sciences/"
           + pname)

    # Generate get-request to the website
    try:
        r=requests.get(url)
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return None
        else:
            raise
    return r, pname


def paperNameGen(paper):
    """Generates pdf name
    
    Args:
        paper(dict): paper details
            level(str): HL or SL
            number(str): Paper 1, 2, or 3
            year(str): the year of the paper
            month(str): the month in e.g. May
            tz(str): the timezone
            kind(str): the kind of paper e.g. qp for question paper
    
    Returns:
        string
        
    """

    year = paper["year"]  # in full e.g. 2019
    month = paper["month"].capitalize()  # May or Nov (First char uppercase)
    tz = paper["tz"]  # 1 or 2 (May) or 0 (Nov)
    level = paper["level"].upper()  # HL or SL (all char uppercase)
    kind = paper["kind"].lower()  # qp or ms (all char lowercase)
    number = paper["number"]  # 1 or 2 or 3

    # Shortened month and year
    smonth=month[0]
    syear=year[-2:]
    
    # No need to specify TZ for Nov papers and May 2016 papers
    if (month == 'Nov' or (month == 'May' and year == '2016')):
        name = ('Physics_' + level + '_' + smonth + syear + '_' + kind
                   + number + '.pdf')
    else:
        name = ('Physics_' + level + '_' + smonth + syear + '_' + 'TZ' + tz
                   + '_' + kind + number + '.pdf')
    
    return name


def renamePYP(paper, path=None):
    """Rename downloaded past year paper
    
    Args:
        paper(dict): paper details
            level(str): HL or SL
            number(str): Paper 1, 2, or 3
            year(str): the year of the paper
            month(str): the month in e.g. May
            tz(str): the timezone
            kind(str): the kind of paper e.g. qp for question paper

        path: the filepath to save the paper
        
    Returns:
        int
        
    """

    # import os
    # import os.path

    # If path to store the file is not specified,
    # store it in root directory, one level above where code is stored
    if path == None:
        path = os.path.dirname(__file__)
    
    year = paper["year"]  # in full e.g. 2019
    month = paper["month"].capitalize()  # May or Nov (First char uppercase)
    tz = paper["tz"]  # 1 or 2 (May) or 0 (Nov)
    level = paper["level"].upper()  # HL or SL (all char uppercase)
    kind = paper["kind"].lower()  # qp or ms (all char lowercase)
    number = paper["number"]  # 1 or 2 or 3
    
    oldname = webNameGen(paper)
    
    newpath = os.path.join(path, level, year, month.upper())

    # If newpath does not exist, create it
    if not os.path.isdir(newpath):
        try:
            os.makedirs(newpath)
        except OSError as error:
            print(error)
    
    # Generate new name for the paper.
    # No need to specify TZ for Nov papers and May 2016 papers
    newname = paperNameGen(paper)
    if not os.path.isfile(os.path.join(newpath, newname)):
        os.rename(os.path.join(path, oldname),os.path.join(newpath, newname))
        return 0
    else:
        # File exists. Cannot override
        return 1


def sanity_check(paper):
    """Checks the paper details for any inconsistencies

    Args:
        paper(dict): paper details
            level(str): HL or SL
            number(str): Paper 1, 2, or 3
            year(str): the year of the paper
            month(str): the month in e.g. May
            tz(str): the timezone
            kind(str): the kind of paper e.g. qp for question paper
        
    Returns:
        int
    
    
    """

    # Initialize valid month and level inputs
    month = ["may", "nov"]
    level = ["hl", "sl"]

    # Check if year input can be changed to integer
    try:
        year = int(paper["year"])
    except ValueError:
        raise Exception("Format error: year input must be integer string")

    # Check if year input falls within range
    if year < 2016:
        raise Exception("Format error: year input no earlier than 2016")
        return 1

    if paper["level"] not in level:
        raise Exception("Format error: check level input")
        return 2

    if paper["month"] not in month:
        raise Exception("Format error: check month input")
        return 3

    if paper["month"] == "may":
        tz = ["1", "2"]
        if paper["tz"] not in tz:
            raise Exception("Format error: check tz input")
            return 4
    return 0

    # Don't have to check for tz for Nov,
    # since there is only one timezone


def webNameGen(paper):
    """Generates pdf name given by website from past year paper details
    
    Args:
        paper(dict): paper details
            level(str): HL or SL
            number(str): Paper 1, 2, or 3
            year(str): the year of the paper
            month(str): the month in e.g. May
            tz(str): the timezone
            kind(str): the kind of paper e.g. qp for question paper
    
    Returns:
        string
        
    """

    year = paper["year"]
    month = paper["month"].lower() # May or Nov
    tz = paper["tz"] # 1 or 2 (May) or 0 (Nov)
    level = paper["level"].upper() # HL or SL
    kind = paper["kind"].lower() # qp or ms
    number = paper["number"] # 1 or 2 or 3
    
    # For Nov papers, there is no need to specify TZ as there is only one
    # timezone (TZ0).
    # There is only one timezone for May 2016 papers as it is the Specimen
    # paper
    if (month == 'nov' or (month == 'may' and year == '2016')):
        name = 'Physics_paper_' + number + '__' + level
    else:
        name = 'Physics_paper_' + number + '__' + 'TZ' + tz +'_' + level
        
    if kind == 'ms':
        name = name + '_markscheme'
        
    name = name + '.pdf'
    
    return name