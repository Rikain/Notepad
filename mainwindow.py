# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtGui import QTextDocumentWriter, QKeySequence, QIcon
from PyQt5.QtCore import QFileInfo
import resources


app_name = "Notepad"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("MainWindow.ui", self)

        centralWigedt = uic.loadUi("CentralWidget.ui")
        self.setCentralWidget(centralWigedt)

        # catToolbar
        # Actions
        self.actionEditToolbar.triggered.connect(self.show_edit_toolbar)
        self.actionFileToolbar.triggered.connect(self.show_file_toolbar)
        # File toolbar
        # Actions
        self.actionNew.triggered.connect(self.file_new)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSaveAs.triggered.connect(self.save_file_as)
        self.actionPrint.triggered.connect(self.print_file)
        self.actionExit.triggered.connect(self.exit)
        self.actionExportPdf.triggered.connect(self.export_pdf)
        self.actionPrintPreview.triggered.connect(self.print_preview)
        # Shortcuts
        self.actionNew.setShortcut(QKeySequence.New)
        self.actionOpen.setShortcut(QKeySequence.Open)
        self.actionSave.setShortcut(QKeySequence.Save)
        self.actionSaveAs.setShortcut(QKeySequence.SaveAs)
        self.actionPrint.setShortcut(QKeySequence.Print)
        self.actionExit.setShortcut(QKeySequence("Ctrl+W"))
        self.actionExportPdf.setShortcut(QKeySequence("Ctrl+Shift+P"))
        self.actionPrintPreview.setShortcut(QKeySequence("Ctrl+Shift+O"))
        # Edit toolbar
        # Actions
        self.actionCopy.triggered.connect(centralWigedt.textEdit.copy)
        self.actionPaste.triggered.connect(centralWigedt.textEdit.paste)
        self.actionCut.triggered.connect(centralWigedt.textEdit.cut)
        self.actionRedo.triggered.connect(centralWigedt.textEdit.redo)
        self.actionUndo.triggered.connect(centralWigedt.textEdit.undo)
        self.actionSelect_All.triggered.connect(centralWigedt.textEdit.selectAll)
        # Shortcuts
        #
        self.show_file_toolbar()

        self.filename = None
        self._default_open_dir = None
        self.file_new()
        pass

    @QtCore.pyqtSlot()
    def closeEvent(self, event):
        if self.check_if_saved():
            event.accept()
        else:
            event.ignore()

    def hide_all_cat_toolbars(self):
        self.editToolbar.hide()
        self.fileToolbar.hide()
        pass

    @QtCore.pyqtSlot()
    def show_file_toolbar(self):
        self.hide_all_cat_toolbars()
        self.fileToolbar.show()
        pass

    @QtCore.pyqtSlot()
    def show_edit_toolbar(self):
        self.hide_all_cat_toolbars()
        self.editToolbar.show()
        pass

    @QtCore.pyqtSlot()
    def file_new(self):
        ret = self.check_if_saved()
        if ret:
            self.centralWidget().textEdit.clear()
            self.filename = None
            self.setWindowName()
        pass

    @QtCore.pyqtSlot()
    def open_file(self):
        ret = self.check_if_saved()
        if ret:
            dir = ""
            if self._default_open_dir is not None:
                dir = self._default_open_dir
            file_dialog = QFileDialog.getOpenFileName(self, 'Open File', dir, "Text Files (*.txt)")
            # change it to pop up message box that asks if save changes
            _filename = file_dialog[0]
            if _filename:
                f = open(_filename, 'r')
                self.filename = _filename
                self.setWindowName()
                with f:
                    data = f.read()
                    self.centralWidget().textEdit.setText(data)
                self.centralWidget().textEdit.document().setModified(False)
        pass

    @QtCore.pyqtSlot()
    def save_file(self):
        if self.filename is None:
            ret = self.save_file_as()
            if ret is False:
                return False
            self.setWindowName()
        else:
            writer = QTextDocumentWriter(self.filename)
            success = writer.write(self.centralWidget().textEdit.document())
            if success:
                self.centralWidget().textEdit.document().setModified(False)
        return True

    @QtCore.pyqtSlot()
    def save_file_as(self):
        dir = ""
        if self._default_open_dir is not None:
            dir = self._default_open_dir
        file_dialog = QFileDialog.getSaveFileName(self, 'Save File', dir, "Text Files (*.txt) ;; All Files (*.*)")
        # change it to pop up message box that asks if save changes
        filename = file_dialog[0]
        if filename:
            self.filename = filename
            self.save_file()
            return True
        else:
            return False


    @QtCore.pyqtSlot()
    def print_file(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.Accepted:
            self.centralWidget().textEdit.print_(printer)
        pass

    def setWindowName(self):
        if self.filename is not None:
            self.setWindowTitle(self.filename + " - " + app_name)
        else:
            self.setWindowTitle(app_name)

    @QtCore.pyqtSlot()
    def exit(self):
        self.close()
        pass

    def check_if_saved(self):
        if self.centralWidget().textEdit.document().isModified():
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Unsaved changes")
            msgBox.setWindowIcon(QIcon("images/iconfinder_13_-_Question_1815562"))
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText("The document has been modified.")
            msgBox.setInformativeText("Do you want to save changes?")
            msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Save)
            ret = msgBox.exec()
            if ret == QMessageBox.Cancel:
                return False
            elif ret == QMessageBox.Save:
                return self.save_file()
            return True
        else:
            return True

    @QtCore.pyqtSlot()
    def export_pdf(self):
        str = ""
        if self._default_open_dir is not None:
            str += self._default_open_dir
        if self.filename is not None:
            str += QFileInfo(self.filename).baseName()
            str += ".pdf"
        fn, _ = QFileDialog.getSaveFileName(self, "Export PDF", str, "PDF Files (*.pdf) ;; All Files (*.*)")
        if fn != "":
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            if QFileInfo(fn).suffix() == "pdf":
                printer.setOutputFileName(fn)
            else:
                fn = QFileInfo(fn).baseName()
                printer.setOutputFileName(fn+".pdf")
            self.centralWidget().textEdit.document().print_(printer)
        pass

    @QtCore.pyqtSlot()
    def print_preview(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.printPreview)
        previewDialog.exec_()
        pass

    def printPreview(self, printer):
        self.centralWidget().textEdit.print_(printer)
        pass
