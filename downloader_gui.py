#!/usr/bin/env python3
# Filename: downloader_gui.py

"""A GUI for downloader.py"""

from functools import partial
import os
import sys

import PyQt5.QtCore as qtCore
import PyQt5.QtWidgets as qtWid
import PyQt5.QtGui as qtGUI
from PyQt5.sip import delete

import helpers

# Path to the Python file
FILE_PATH = os.path.abspath(".")
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
        self.setFixedSize(800, 450) # Disable re-sizing
    
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
        self.widgets['message'] = qtWid.QLabel('')
        
        # Merge the smaller layouts into the main layout
        self.rightLayout.addWidget(self.widgets['submit'])
        mainLayout.addLayout(self.leftLayout)
        mainLayout.addLayout(self.rightLayout)
        bigLayout.addWidget(self.widgets['message'])
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
            if label not in ['submit', 'message']:
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
        
        self.papers = papers
        self._model(self)

    
    def reportProgress(self, n, N, message):
        message = 'Status: ' + str(n) + '/' + str(N) + ' ' + '(' + message + ')'
        self._view.widgets['message'].setText(message)


    def reportStatus(self,status):
        self._view.widgets['submit'].setEnabled(True)
        self._view.widgets['message'].setText('Status: Completed')
        alert = qtWid.QMessageBox()
        text = 'Summary:\n'
        for i, (key, val) in enumerate(status.items()):
            text = text + key + ' ' + val + '\n'
        alert.setText(text)
        alert.exec()


# The model does not actually download paper but creates another thread.
# Another class is called to then download the paper.
# From: https://realpython.com/python-pyqt-qthread/
def downloadPaper(controller):
    """Downloader_GUI's Model"""

    controller.thread = qtCore.QThread()
    controller.worker = Worker(controller.papers, controller._view)
    controller.worker.moveToThread(controller.thread)
    controller.thread.started.connect(controller.worker.run)
    controller.worker.finished.connect(controller.thread.quit)
    controller.worker.finished.connect(controller.worker.deleteLater)
    controller.thread.finished.connect(controller.thread.deleteLater)
    controller.worker.progress.connect(controller.reportProgress)
    controller.thread.start()

    controller._view.widgets['submit'].setEnabled(False)
    controller.thread.finished.connect(
        lambda: controller._view.widgets['submit'].setEnabled(True)
    )
    controller.thread.finished.connect(
        lambda: controller._view.widgets['message'].setText('Status: Completed')
    )
    controller.worker.finished.connect(controller.reportStatus)


# Create a Worker class to handle the downloading of past year papers.
# It is working on a different thread from the main GUI.
# This ensures that the GUI does not freeze even when downloading.
# Only the Submit button is deactivated during downloading.
class Worker(qtCore.QObject):
    """A QObject to download papers on a separate thread from the GUI."""

    finished = qtCore.pyqtSignal(dict)
    progress = qtCore.pyqtSignal(int, int, str)

    def __init__(self, papers, view):
        super().__init__()
        self.papers = papers
        self.view = view

    def run(self):
        self.downloadPaper(self.papers, self.view)

    def downloadPaper(self,papers, view):
        """Downloader_GUI's Model"""
        status = {}
        
        # Iterate over list of papers to download and rename them
        for i, paper in enumerate(papers):
            N = len(papers)
            r,pname = helpers.getPYP(paper)
            error = helpers.downloadPYP(r, pname, paper)
            papername = helpers.paperNameGen(paper)
            if error:
                status_message = "Not found"
                
            else: 
                error = helpers.renamePYP(paper, ROOT_DIR)
                if error:
                    status_message = "File already exists"
                else:
                    status_message = "Downloaded"

            message = status_message + ': ' + papername

            self.progress.emit(i+1, N, message)
            status[papername] = status_message
            

        self.finished.emit(status)


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