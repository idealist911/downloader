# DOWNLOADER
**Video Demo**: https://youtu.be/eGjzme-spjA

## Description
A project to download IB physics past year papers from a website and organize those papers into respective folders.
It includes:
1. *helpers.py*: A group of functions to help download past year papers. It is a module that is being imported by the other files.
2. *downloader.py*: A group of scripts (including a helper script of functions) to download. Users download using a csv file listing the past year papers.
3. *downloader_gui.py*: A GUI to download using the helper script. Users download by selecting parameters using checkboxes. Requires python to run and certain modules to run.
4. *downloader_gui.exe*: A GUI to download using the helper script. Users download by selecting parameters using checkboxes. Does not require python. For Windows.
5. *downloader_gui_os*: A GUI to download using the helper script. Users download by selecting parameters using checkboxes. Does not require python. For Mac OS.

Features in the GUI:
1. Checkboxes and comboboxes to select details of past year paper to be downloaded. Can download multiple papers at once.
2. Details of papers being downloaded are shown while downloading.
3. A summary page listing papers downloaded or could not be found after the download request has been processed.
4. Papers are organized into respective folders after download.

## Python modules
These are the modules are required to run the python file (not the executables):
1. requests
2. PyQt5

## Instructions
Instructions (**downloader.py**):
1. Create a csv file named "input.csv" in the same folder,
    - with headings ordered as follows,
    - and the paper details below
    ----------------------------------------------------------------
    |level,year,month,tz,number,kind                                |
    |SL,2021,May,1,1,ms                                             |
    |SL,2021,May,1,1,qp                                             |
    
2. Double-click on the python file (or run it in the terminal) to download the papers.

Instructions (**downloader_gui.py**):
1. Double-click on the python file (or run it in the terminal) to open the GUI.
2. Select the checkboxes that describes the papers.
3. Click on the submit button to download the papers.

Instructions (**downloader_gui.exe** or **downloader_gui_os**):
1. Double-click on the executable file to open the GUI.
2. Select the checkboxes that describes the papers.
3. Click on the submit button to download the papers.

## Future work
To be added:
1. A scrollbox for the summary page, especially when a large number of files were downloaded, which would overwhelm the alert box.
2. A reset button to reset all changes to checkboxes and comboboxes.
3. A method to upload csv files listing past year paper details. 
4. A method to create csv files listing past year paper details from the checked checkboxes and comboboxes selections.
5. A method to download papers of other subjects.

## Background
This project is created for the Final Project portion of CS50 course.
I am a tuition teacher for IB physics students and I felt that this saves me time in downloading past year papers on the fly.
Although a python script is enough for me, I thought that a GUI would benefit my colleagues who do not know Python.
Besides, a python script is not much of a challenge for a project submission.

There are mainly two ways to create a GUI in Python -- PyQt or Tkinter.
A quick search on the internet reveals that PyQt is a better choice as the UI looks more modern and it comes with many advanced widgets.
See:
1. https://dev.to/amigosmaker/python-gui-pyqt-vs-tkinter-5hdd#:~:text=Mostly%2C%20Tkinter%20is%20all%20about,Python%20knowledge%20from%20another%20script.
2. https://www.geeksforgeeks.org/python-gui-pyqt-vs-tkinter/

But packaging a PyQt GUI (known as freezing) into an executable is painful.
Pyinstaller is easy to use but it only packages the GUI into an executable for the OS which I package it with.
In my case, that is Windows.
To package it for Mac OS, I had to get a Mac OS virtual machine and package it there.
During packaging, it seems that PyQt is not automatically detected by Pyinstaller so there is a need to make it explicit to Pyinstaller via --hidden-import.
