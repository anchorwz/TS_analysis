import sys, os, csv
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import subprocess


class Form(QMainWindow,QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.inputlen = 0
        self.setWindowTitle('SAX Time Series Data')

        self.data = DataHolder()
        self.series_list_model = QStandardItemModel()

        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()

        self.update_ui()
        self.on_show()

    def load_file(self, filename=None):
        filename = QFileDialog.getOpenFileName(self,
            'Open a data file', '.', 'CSV files (*.csv);;All Files (*.*)')

        if filename:
            self.data.load_from_file(filename)
            self.fill_series_list(self.data.series_names())
            self.status_text.setText("Loaded " + filename)
            self.update_ui()

    def update_ui(self):
        if self.data.series_count() > 0 and self.data.series_len() > 0:
            self.from_spin.setValue(0)
            self.to_spin.setValue(self.data.series_len() - 1)

            for w in [self.from_spin, self.to_spin]:
                w.setRange(0, self.data.series_len() - 1)
                w.setEnabled(True)
        else:
            for w in [self.from_spin, self.to_spin]:
                w.setEnabled(False)

    def on_run(self):
        arg = ['python', 'test.py','-n', str(self.timelen.value()), '-w', str(self.wordsize.value()), '-a', str(self.alphasize.value())]
        p=subprocess.Popen(arg)
        p.communicate()
        p_status = p.wait()
        self.load_file('TS.csv')

    def on_show(self):
        self.axes.clear()
        self.axes.grid(True)

        has_series = False
        for row in range(self.series_list_model.rowCount()):
            model_index = self.series_list_model.index(row, 0)
            checked = self.series_list_model.data(model_index,
                Qt.CheckStateRole) == QVariant(Qt.Checked)
            name = str(self.series_list_model.data(model_index).toString())

            if checked:
                has_series = True

                x_from = self.from_spin.value()
                x_to = self.to_spin.value()
                series = self.data.get_series_data(name)[x_from:x_to + 1]
                self.axes.plot(range(len(series)), series, 'o-', label=name)

        if has_series and self.legend_cb.isChecked():
            self.axes.legend()
        self.canvas.draw()
    

    def on_about(self):
        msg = __doc__
        QMessageBox.about(self, "About the demo", msg.strip())

    def fill_series_list(self, names):
        self.series_list_model.clear()

        for name in names:
            item = QStandardItem(name)
            item.setCheckState(Qt.Unchecked)
            item.setCheckable(True)
            self.series_list_model.appendRow(item)

    def create_main_frame(self):
        self.main_frame = QWidget()

        plot_frame = QWidget()

        self.dpi = 100
        self.fig = Figure((6.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.axes = self.fig.add_subplot(111)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        log_label = QLabel("Data series:")
        self.series_list_view = QListView()
        self.series_list_view.setModel(self.series_list_model)

        spin_label1 = QLabel('X from')
        self.from_spin = QSpinBox()
	self.from_spin.setMaximum(1000)
        spin_label2 = QLabel('to')
        self.to_spin = QSpinBox()
	self.to_spin.setMaximum(1000)

        spins_hbox = QHBoxLayout()
        spins_hbox.addWidget(spin_label1)
        spins_hbox.addWidget(self.from_spin)
        spins_hbox.addWidget(spin_label2)
        spins_hbox.addWidget(self.to_spin)
        spins_hbox.addStretch(1)

        self.legend_cb = QCheckBox("Show L&egend")
        self.legend_cb.setChecked(False)


        # Give parameters for SAX
        spin_label5 = QLabel('n')
        self.timelen = QSpinBox()
        self.timelen.setMaximum(10000)
        spin_label3 = QLabel('w')
        self.wordsize = QSpinBox()
        self.wordsize.setMaximum(10000)
        spin_label4 = QLabel('a')
        self.alphasize = QSpinBox()
        self.alphasize.setMaximum(10000)

        spins_hbox2 = QHBoxLayout()
        spins_hbox2.addWidget(spin_label5)
        spins_hbox2.addWidget(self.timelen)
        spins_hbox2.addWidget(spin_label3)
        spins_hbox2.addWidget(self.wordsize)
        spins_hbox2.addWidget(spin_label4)
        spins_hbox2.addWidget(self.alphasize)
        spins_hbox2.addStretch(1)


        self.run_button = QPushButton("&Run")
        self.connect(self.run_button, SIGNAL('clicked()'), self.on_run)

        #right_vbox.addWidget()
        self.btn1 = QPushButton("&Open SAX result")
        self.connect(self.btn1, SIGNAL('clicked()'), self.getfiles)

        self.show_button = QPushButton("&Show Plot")
        self.connect(self.show_button, SIGNAL('clicked()'), self.on_show)

        # Panel to show the SAX letter result
        Symbolicres = QLabel("Symbolic result:")
        self.contents = QTextEdit()
	self.contents.setReadOnly(True)




        left_vbox = QVBoxLayout()
        left_vbox.addWidget(self.canvas)
        left_vbox.addWidget(self.mpl_toolbar)

        right_vbox = QVBoxLayout()
        right_vbox.addWidget(log_label)
        right_vbox.addWidget(self.series_list_view)
        right_vbox.addLayout(spins_hbox)
        right_vbox.addWidget(self.legend_cb)
        right_vbox.addLayout(spins_hbox2)
        right_vbox.addWidget(self.run_button)
        #right_vbox.addWidget(self.textbox)
        #right_vbox.addWidget(self.btn)
        #right_vbox.addWidget(self.text_edit)
        right_vbox.addWidget(self.show_button)
        right_vbox.addWidget(Symbolicres)
        right_vbox.addWidget(self.btn1)
        right_vbox.addWidget(self.contents)
        right_vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addLayout(left_vbox)
        hbox.addLayout(right_vbox)
        self.main_frame.setLayout(hbox)

        self.setCentralWidget(self.main_frame)

    def getfiles(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter("Text files (*.txt)")
        filenames = QStringList()
         	
        if dlg.exec_():
           filenames = dlg.selectedFiles()
           f = open(filenames[0], 'r')
         		
           with f:
              data = f.read()
              self.contents.setText(data)

    # Get input parameter of time series

    def getint(self):
        num, ok = QInputDialog.getInt(self,'Integer input dualog','Enter a ingeter number:')
        self.inputlen = num 
        if ok:
            self.le.setText(str(num))

    def create_status_bar(self):
        self.status_text = QLabel("Please load a data file")
        self.statusBar().addWidget(self.status_text, 1)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")

        load_action = self.create_action("&Load file",
            shortcut="Ctrl+L", slot=self.load_file, tip="Load a file")
        quit_action = self.create_action("&Quit", slot=self.close,
            shortcut="Ctrl+Q", tip="Close the application")

        self.add_actions(self.file_menu,
            (load_action, None, quit_action))

        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About",
            shortcut='F1', slot=self.on_about,
            tip='About the demo')

        self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None,
                        icon=None, tip=None, checkable=False,
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


class DataHolder(object):

    def __init__(self, filename=None):
        self.load_from_file(filename)

    def load_from_file(self, filename=None):
        self.data = {}
        self.names = []

        if filename:
            for line in csv.reader(open(filename, 'rb')):
                self.names.append(line[0])
                self.data[line[0]] = map(float, line[1:])
                self.datalen = len(line[1:])

    def series_names(self):
        """ Names of the data series
        """
        return self.names

    def series_len(self):
        """ Length of a data series
        """
        return self.datalen

    def series_count(self):
        return len(self.data)

    def get_series_data(self, name):
        return self.data[name]


def main():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
    dh = DataHolder('TS.csv')
