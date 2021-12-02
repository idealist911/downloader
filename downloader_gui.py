#!/usr/bin/env python3
# Filename: downloader_gui.py

"""A GUI for downloader.py"""

from functools import partial
import os
import sys

import PyQt5.QtWidgets as qtWid
import PyQt5.QtGui as qtGUI

import helpers

# Path to the Python file
FILE_PATH = os.path.dirname(__file__)
# Path to where the past year papers will be stored
ROOT_DIR = FILE_PATH

# Create the View 
class DloaderUI(qtWid.QMainWindow):
    """Downloader_GUI's View (GUI)"""
    def __init__(self):
        super().__init__()

        # Set window properties
        title = "Downloader GUI"
        self.setWindowTitle(title)
        self.setFixedSize(800, 350) # Disable re-sizing
    
        self._centralWidget = qtWid.QWidget(self)
        self.setCentralWidget(self._centralWidget)
        bigLayout = qtWid.QVBoxLayout()
        mainLayout = qtWid.QHBoxLayout()
        titleLayout = qtWid.QHBoxLayout()
        titleWidget = qtWid.QWidget()
        titleWidget.setLayout(titleLayout)
        titleLayout.addWidget(qtWid.QLabel('Download IB PYP'))
        bigLayout.addWidget(titleWidget)
        titleWidget.setStyleSheet('background-color:#3333FF; color:#FFFFFF')
        bigLayout.addLayout(mainLayout)

        # Arrange the layout in a left-right then top-down fashion
        self.leftLayout = qtWid.QVBoxLayout()
        self.rightLayout = qtWid.QVBoxLayout()
        self.widgets = {}

        # Create a layout for each search parameter
        self._createLevelLayout()
        self._createYearLayout()
        self._createKindLayout()
        self._createTZLayout()
        self._createNumLayout()
        self.widgets['submit'] = qtWid.QPushButton('submit')
        
        # Merge the smaller layouts into the main layout
        self.rightLayout.addWidget(self.widgets['submit'])
        mainLayout.addLayout(self.leftLayout)
        mainLayout.addLayout(self.rightLayout)
        self._centralWidget.setLayout(bigLayout)
        

    def _createKindLayout(self):
        self.kindLayout = qtWid.QGridLayout()
        self.kindLayout.addWidget(qtWid.QLabel("Paper kind"), 0, 0, 1, 2)
        kindLabels = ["Question Paper", "Mark Scheme"]
        for i, label in enumerate(kindLabels):
            self.widgets[label] = [qtWid.QCheckBox(label), 'kind']
            self.kindLayout.addWidget(self.widgets[label][0], 1, i)
        self.leftLayout.addLayout(self.kindLayout)


    def _createLevelLayout(self):
        self.levelLayout = qtWid.QGridLayout()
        self.levelLayout.addWidget(qtWid.QLabel("Level"), 0, 0, 1, 2) 
        levelLabels = ["HL", "SL"]
        for i, label in enumerate(levelLabels):
            self.widgets[label] = [qtWid.QCheckBox(label), 'level']
            self.levelLayout.addWidget(self.widgets[label][0], 1, i)    
        self.leftLayout.addLayout(self.levelLayout)

    
    def _createNumLayout(self):
        self.numLayout = qtWid.QGridLayout()
        self.numLayout.addWidget(qtWid.QLabel("Paper number"), 0, 0, 1, 2)
        numLabels = ["P1", "P2", "P3"]
        for i, label in enumerate(numLabels):
            self.widgets[label] = [qtWid.QCheckBox(label), 'num']
            self.numLayout.addWidget(self.widgets[label][0], 1, i)
        self.rightLayout.addLayout(self.numLayout)


    def _createTZLayout(self):
        self.tzLayout =  qtWid.QGridLayout()
        self.tzLayout.addWidget(qtWid.QLabel("Timezone"), 0, 0, 1, 2)
        tzLabels = ["Nov TZ0", "May TZ1", "May TZ2"]
        for i, label in enumerate(tzLabels):
            self.widgets[label] = [qtWid.QCheckBox(label), 'tz']
            self.tzLayout.addWidget(self.widgets[label][0], 1, i)
        self.rightLayout.addLayout(self.tzLayout)


    def _createYearLayout(self):
        self.yearLayout = qtWid.QFormLayout()
        self.yearLayout.addRow(qtWid.QLabel("Year"))
        yearLabels = ["From", "To"]
        for i, label in enumerate(yearLabels):
            self.widgets[label] = [qtWid.QComboBox(), 'year'+label]
            for year in range(2016, 2022, 1):
                self.widgets[label][0].addItem(str(year))
            self.yearLayout.addRow(qtWid.QLabel(label), self.widgets[label][0])
        self.leftLayout.addLayout(self.yearLayout)


class DloaderCtrller:
    """Downloader_GUI's controller"""
    def __init__(self, model, view):
        self._view = view
        self._model = model
        self._connectSignals()
        self.params = {'yearFrom':'2016', 'yearTo':'2016'}


    def _addParam(self, widget, key):
        if isinstance(widget, qtWid.QCheckBox):
            if widget.isChecked():
                if self.params.get(key) == None:
                    self.params[key] = [widget.text()]
                else:
                    self.params[key].append(widget.text())        
            else:
                self.params[key].remove(widget.text())
        
        if isinstance(widget, qtWid.QComboBox):
            self.params[key] = widget.currentText()

    
    def _connectSignals(self):
        for label, widget in self._view.widgets.items():
            if label not in ['submit']:
                if isinstance(widget[0], qtWid.QCheckBox):
                    widget[0].stateChanged.connect(partial(self._addParam, widget[0], widget[1]))

                if isinstance(widget[0], qtWid.QComboBox):
                    widget[0].currentTextChanged.connect(partial(self._addParam, widget[0], widget[1]))

        self._view.widgets['submit'].clicked.connect(self.on_submit)

    
    def on_submit(self):
        # Check for valid input
        message = None
        if self.params.get("yearFrom") > self.params.get("yearTo"):
            message = "From Year must be earlier than To Year"
        elif self.params.get("num") == None:
            message = "Please select a paper number."
        elif self.params.get("level") == None:
            message = "Please select a paper level."
        elif self.params.get("tz") == None:
            message = "Please select a paper timezone."
        elif self.params.get("kind") == None:
            message = "Please select a paper kind."

        if message is not None:
            alert = qtWid.QMessageBox()
            alert.setText(message)
            alert.exec()
            return 1

        # Generate a list of dictionaries
        # Each dictionary contains the details of each paper requested
        papers = []
        yearFrom = int(self.params.get("yearFrom"))
        yearTo = int(self.params.get("yearTo"))
        yearList = range(yearFrom, yearTo+1, 1)

        for year in yearList:
            year = str(year)

            for TZ in self.params["tz"]:
                if TZ == "May TZ1":
                    month = "May"
                    tz = "1"
                elif TZ == "May TZ2":
                    month = "May"
                    tz = "2"
                else:
                    month = "Nov"
                    tz = "0"
                
                for level in self.params["level"]:
                    
                    for num in self.params["num"]:
                        number = num[-1]

                        for Kind in self.params['kind']:
                            if Kind == "Question Paper":
                                kind = "qp"
                            else:
                                kind = "ms"

                            paper = {
                                "year":year,
                                "month":month,
                                "tz":tz,
                                "level":level,
                                "number":number,
                                "kind":kind
                            }
                            
                            papers.append(paper)
        
        self._model(papers)


def downloadPaper(papers):
    """Downloader_GUI's Model"""
    # Iterate over list of papers to download and rename them
    for paper in papers:
        r,pname = helpers.getPYP(paper)
        error = helpers.downloadPYP(r, pname, paper)
        papername = helpers.paperNameGen(paper)
        if error:
            message = "Not found:"
            
        else: 
            helpers.renamePYP(paper, ROOT_DIR)
            message = "Downloaded:"

        message = message + ' ' + papername
        alert = qtWid.QMessageBox()
        alert.setText(message)
        alert.exec_()


def main():
    """Main function"""
    app = qtWid.QApplication(sys.argv)
    app.setStyle('windowsvista')
    custom_font = qtGUI.QFont('Arial font')
    custom_font.setWeight(20)
    widgets = ["QCheckBox", "QComboBox", "QPushButton"]
    for widget in widgets:
        app.setFont(custom_font, widget)
    custom_font.setWeight(40)
    app.setFont(custom_font, "QLabel")

    # Create and show GUI
    view = DloaderUI()
    view.show()
    # Create model and controller
    model = downloadPaper
    DloaderCtrller(model=model, view=view)
    # Execute main loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()