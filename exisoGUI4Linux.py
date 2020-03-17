__author__ = 'bosito7'
__email__ = "bosito7@gmail.com"

from PyQt4 import QtCore, QtGui
import threading, time
import exisoGUI4LinuxUI as E4L_UI
import exisoGUI4Linux_kernel as kernel

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class BarEvent(QtCore.QObject):
    Bar_Value_S = QtCore.pyqtSignal()

class MyThreads(object):
    ConvertThread_stop= threading.Event()
    UpdateBarsThread_stop= threading.Event()
    LogsThread_stop= threading.Event()

    def __init__(self):
        self.ConvertThread = threading.Thread(target=self.ConvertTheadfunc, args=(1, self.ConvertThread_stop))
        self.UpdateBarsThread = threading.Thread(target=self.UpdateBarsThreadfunc, args=(1, self.UpdateBarsThread_stop))
        self.LogsThread = threading.Thread(target=self.LogsThreadfunc, args=(1, self.LogsThread_stop))

    def ConvertTheadfunc(self, arg1, stop_event):
        if(stop_event.is_set()):
            kernel.extract_popen.kill()# se pudiera hacer una funcion para eliminar carpeta con elementos extraidos hasta el momento
            print('Extract process killed')

        while(not stop_event.is_set()):
            if kernel.TaskEnded:
                SU = ui.Skip_Syst_Upd_checkBox.isChecked()
                kernel.ProcManyISOs(kernel.ISOsList, SU)
                stop_event.wait(1)
        pass

    def UpdateBarsThreadfunc(self, arg1, stop_event):
        while(not stop_event.is_set()):
            while not kernel.TaskEnded:
                if(kernel.ActFileInISOCount > 0):

                    value1 = (float(kernel.ActFileInISOCount)/float(kernel.NISOFiles)) * float(100)
                    value2 = ((float(kernel.ActISOFile)/float(kernel.ISOsList.__len__())) + value1/float(kernel.NISOFiles)) * float(100)

                    if (int(value1) != ui.Cur_Value):
                        print 'Progress Bar Courrent Value'
                        print value1
                        ui.Cur_Value = int(value1)
                        ui.barEvent.Bar_Value_S.emit()

                    if (int(value2) != ui.Tot_Value):
                        print 'Progress Bar Total Value'
                        print value2
                        ui.Tot_Value = int(value2)
                        ui.barEvent.Bar_Value_S.emit()

                time.sleep(0.5)

            stop_event.wait(1)
        pass

    def LogsThreadfunc(self, arg1, stop_event):
        while(not stop_event.is_set()):
            print 'Logs'

            stop_event.wait(1)
        pass

class E4L_MainWindow(E4L_UI.Ui_MainWindow):
    barEvent = BarEvent()

    def __init__(self):
        super(E4L_MainWindow, self).__init__()

    def setupUi(self, MainWindow):
        super(E4L_MainWindow, self).setupUi(MainWindow)

        ###Threads###
        self.mythreads = object()
        #self.mythreads = MyThreads()

        self.ConvertThread_stop= threading.Event()
        self.UpdateBarsThread_stop= threading.Event()
        self.LogsThread_stop= threading.Event()
        self.ConvertThread = threading.Thread(target=self.ConvertTheadfunc, args=(1, self.ConvertThread_stop))
        self.UpdateBarsThread = threading.Thread(target=self.UpdateBarsThreadfunc, args=(1, self.UpdateBarsThread_stop))
        self.LogsThread = threading.Thread(target=self.LogsThreadfunc, args=(1, self.LogsThread_stop))

        ###Aux Vars###
        self.Tot_Value = 0
        self.Cur_Value = 0
        self.Converting = False


        ###Methods calls###

        self.Add_ISO_pushButton.clicked.connect(self.AddISOfunction)
        self.Add_ISO_Folder_pushButton.clicked.connect(self.AddISOsinFolder)
        self.Remove_ISO_pushButton.clicked.connect(self.RemoveISOfunc)
        self.Start_pushButton.clicked.connect(self.Starfunc)
        self.barEvent.Bar_Value_S.connect(self.UpdateBarsfunc)


    def AddISOfunction(self):
        FNs = []
        FNs = QtGui.QFileDialog.getOpenFileNames(self.centralwidget, 'Open ISO file', '/home','ISO Images (*.iso)')
        print(FNs)
        if FNs != []:
            for iso in FNs:
                kernel.ISOsList.append(iso.__str__())
                print iso.__str__()
                typeItem = QtGui.QTableWidgetItem("ISO")
                sourceItem = QtGui.QTableWidgetItem(iso)
                destinyItem = QtGui.QTableWidgetItem(iso[0:-4])
                #agrego una fila
                act_row = self.Local_Games_tableWidget.rowCount()
                self.Local_Games_tableWidget.setRowCount(act_row + 1)

                self.Local_Games_tableWidget.setItem(act_row, 0, typeItem)
                self.Local_Games_tableWidget.setItem(act_row, 1, sourceItem)
                self.Local_Games_tableWidget.setItem(act_row, 2, destinyItem)

                #self.Local_Games_tableWidget.resizeRowsToContents()
                self.Local_Games_tableWidget.resizeColumnsToContents()

    def AddISOsinFolder(self):
        FolderN = []
        FolderN = QtGui.QFileDialog.getExistingDirectory(self.centralwidget, 'Open ISOs folder')
        FNs = kernel.GetFolderISOFiles(FolderN)

        print(FNs)
        if FNs != []:
            for iso in FNs:
                #Almacenando en la lista general
                kernel.ISOsList.append(iso.__str__())
                print iso.__str__()
                typeItem = QtGui.QTableWidgetItem("ISO")
                sourceItem = QtGui.QTableWidgetItem(iso)
                destinyItem = QtGui.QTableWidgetItem(iso[0:-4])
                #agrego una fila
                act_row = self.Local_Games_tableWidget.rowCount()
                self.Local_Games_tableWidget.setRowCount(act_row + 1)

                self.Local_Games_tableWidget.setItem(act_row, 0, typeItem)
                self.Local_Games_tableWidget.setItem(act_row, 1, sourceItem)
                self.Local_Games_tableWidget.setItem(act_row, 2, destinyItem)

                #self.Local_Games_tableWidget.resizeRowsToContents()
                self.Local_Games_tableWidget.resizeColumnsToContents()

    def RemoveISOfunc(self):
        if self.Local_Games_tableWidget.currentItem() != None:
            selI = self.Local_Games_tableWidget.currentItem().row()
            print(selI)
            self.Local_Games_tableWidget.removeRow(selI)
            allRows = self.Local_Games_tableWidget.rowCount()

            #Rehacer lista a ser extraida
            kernel.ISOsList = []
            for row in xrange(0,allRows):
                it = self.Local_Games_tableWidget.item(row,1).text().__str__()
                kernel.ISOsList.append(it)
                print it

        print(kernel.ISOsList)

    def Starfunc(self):
        global mythreads

        if (not self.Converting):
            self.Converting = True
            self.Start_pushButton.setText('Stop')

            ###Threads###
            mythreads = MyThreads()
            #self.mythreads.ConvertThread_stop.clear()
            mythreads.ConvertThread.start()
            #self.ConvertThread.start()

            #self.mythreads.LogsThread_stop.clear()
            #self.mythreads.LogsThread.start()

            #self.mythreads.UpdateBarsThread_stop.clear()
            mythreads.UpdateBarsThread.start()
            self.UpdateBarsThread.start()

        else:
            self.Converting = False
            self.Start_pushButton.setText('Start')

            #self.ConvertThread_stop.set()
            mythreads.ConvertThread_stop.set()

            #self.mythreads.LogsThread_stop.set()

            #self.UpdateBarsThread_stop.set()
            mythreads.UpdateBarsThread_stop.set()

            kernel.extract_popen.kill()# se pudiera hacer una funcion para eliminar carpeta con elementos extraidos hasta el momento
            print('Extract process killed')

            #kernel.ActISOFile = kernel.ActISOFile - 1;
            mythreads = object()
            time.sleep(2)
            kernel.TaskEnded = True
            #self.Cur_Value = 0
            #self.Tot_Value = 0
            #self.UpdateBarsfunc()
            self.Tot_proc_progressBar.setValue(0)
            self.Curr_File_progressBar.setValue(0)

    def UpdateBarsfunc(self):
        self.Tot_proc_progressBar.setValue(self.Tot_Value)
        self.Curr_File_progressBar.setValue(self.Cur_Value)

    def ConvertTheadfunc(self, arg1, stop_event):
        while(not stop_event.is_set()):
            if kernel.TaskEnded:
                SU = self.Skip_Syst_Upd_checkBox.isChecked()
                kernel.ProcManyISOs(kernel.ISOsList, SU)
            stop_event.wait(1)
        pass

    def UpdateBarsThreadfunc(self, arg1, stop_event):
        while(not stop_event.is_set()):
            while not kernel.TaskEnded:
                if(kernel.ActFileInISOCount > 0):

                    value1 = (float(kernel.ActFileInISOCount)/float(kernel.NISOFiles)) * float(100)
                    value2 = ((float(kernel.ActISOFile)/float(kernel.ISOsList.__len__())) + value1/float(kernel.NISOFiles)) * float(100)

                    if (int(value1) != ui.Cur_Value):
                        print 'Progress Bar Courrent Value'
                        print value1
                        self.Cur_Value = int(value1)
                        self.barEvent.Bar_Value_S.emit()

                    if (int(value2) != ui.Tot_Value):
                        print 'Progress Bar Total Value'
                        print value2
                        self.Tot_Value = int(value2)
                        self.barEvent.Bar_Value_S.emit()

                time.sleep(0.5)

            stop_event.wait(1)
        pass

    def LogsThreadfunc(self, arg1, stop_event):
        while(not stop_event.is_set()):
            print 'Logs'

            stop_event.wait(1)
        pass

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = E4L_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


