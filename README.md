# DOWNLOADER
Description:
A project to download IB physics past year papers from a website and organize those papers into respective folders.
It includes:
1. *downloader.py*: A group of scripts (including a helper script of functions) to download. Users download using a csv file listing the past year papers.
2. *downloader_gui.py*: A GUI to download using the helper script. Users download by selecting parameters using checkboxes.

Instructions (/*downloader.py*/):
1. Create a csv file named "input.csv" in the same folder,
    - with headings ordered as follows,
    - and the paper details below
    ----------------------------------------------------------------
    |level,year,month,tz,number,kind                                |
    |SL,2021,May,1,1,ms                                             |
    |SL,2021,May,1,1,qp                                             |
    
2. Double-click on the python file (or run it in the terminal) to download the papers.


Instructions (/*downloader_gui.py*/):
1. Double-click on the python file (or run it in the terminal) to open the GUI.
2. Select the checkboxes that describes the papers.
3. Click on the submit button to download the papers.
