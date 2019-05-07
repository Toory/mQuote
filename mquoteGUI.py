import trade
import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QWidget, QPushButton, QHBoxLayout,QLabel, QApplication, QVBoxLayout, QCalendarWidget, QTabWidget
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QPixmap

class TradeMainWindow(QMainWindow):

	def __init__(self, parent=None):
		super(TradeMainWindow, self).__init__(parent)
		self.form_widget = TradeWidget(self)
		self.initUI()
		self.setCentralWidget(self.form_widget)

	def initUI(self):
		self.title = 'mQuote'
		self.setWindowTitle(self.title)
		self.setGeometry(100,100,400,500)
		#Icon from Freepik
		self.setWindowIcon(QIcon(QPixmap('stock.png')))
		self.show()

class TradeWidget(QWidget):

	def __init__(self, parent):
		super(TradeWidget,self).__init__(parent)
		self.layout = QVBoxLayout(self)
		self.tabs = QTabWidget()
		self.tab1 = QWidget()
		self.tab2 = QWidget()
		self.tabs.addTab(self.tab1,"Daily Stocks")
		self.tabs.addTab(self.tab2,"History")

		# Add tab1 and tab2 UI
		self.tab1UI()
		self.tab2UI()

		# Add tabs to widget
		self.layout.addWidget(self.tabs)
		self.setLayout(self.layout)
		self.show()

	def tab1UI(self):
		self.button1 = QPushButton('Get Daily Stocks!')
		self.text = QTextEdit()

		self.tab1.v_layout = QVBoxLayout()
		self.tab1.h_layout = QHBoxLayout()

		self.tab1.h_layout.addWidget(self.button1)

		self.tab1.v_layout.addWidget(self.text)
		self.tab1.v_layout.addLayout(self.tab1.h_layout)

		self.tab1.setLayout(self.tab1.v_layout)

		self.button1.clicked.connect(self.btn_clicked)

	def tab2UI(self):
		#super(MyTableWidget, self).__init__()
		self.button3 = QPushButton('Select Start Date')
		self.button4 = QPushButton('Select End Date')
		self.button5 = QPushButton('Get Stocks!')
		self.text2 = QTextEdit()
		self.label1 = QLabel('Start Date')
		self.label2 = QLabel('End Date')
		self.label1.setAlignment(Qt.AlignCenter)
		self.label2.setAlignment(Qt.AlignCenter)

		self.tab2.v_layout = QVBoxLayout()
		self.tab2.h_layout = QHBoxLayout()
		self.tab2.h2_layout = QHBoxLayout()
		self.tab2.h3_layout = QHBoxLayout()

		self.tab2.h_layout.addWidget(self.label1)
		self.tab2.h_layout.addWidget(self.label2)
		self.tab2.v_layout.addLayout(self.tab2.h_layout)

		self.tab2.h2_layout.addWidget(self.button3)
		self.tab2.h2_layout.addWidget(self.button4)
		self.tab2.v_layout.addLayout(self.tab2.h2_layout)


		self.tab2.v_layout.addWidget(self.text2)
		self.tab2.h3_layout.addWidget(self.button5)
		self.tab2.v_layout.addLayout(self.tab2.h3_layout)

		self.tab2.setLayout(self.tab2.v_layout)

		self.button3.clicked.connect(self.Calendar)
		self.button4.clicked.connect(self.Calendar)
		self.button5.clicked.connect(self.btn_clicked)

		self.label1.installEventFilter(self)
		self.label2.installEventFilter(self)

	def btn_clicked(self):
		self.text.clear()
		self.text2.clear()
		sender = self.sender()

		if sender.text() == 'Get Daily Stocks!':
			trade.Trade(1,self.text)
			self.text.append('[+] Done!')
		elif sender.text() == 'Get Stocks!':
			StartDate = self.label1.text()
			EndDate = self.label2.text()
			trade.Trade(2,self.text2,StartDate,EndDate)
			self.text2.append('[+] Done!')
		else:
			pass

	def Calendar(self):
		sender = self.sender()
		self.cal = QCalendarWidget(self)
		self.cal.setGridVisible(True)
		if sender.text() == 'Select Start Date':
			self.cal.clicked[QDate].connect(self.startDate)
		elif sender.text() == 'Select End Date':
			self.cal.clicked[QDate].connect(self.endDate)
		# create a new window that contains the calendar
		self.calendarWindow = QWidget()
		hbox = QHBoxLayout()
		hbox.addWidget(self.cal)
		self.calendarWindow.setLayout(hbox)
		self.calendarWindow.setGeometry(250, 250, 250, 250)
		self.calendarWindow.setWindowTitle('Calendar')
		# open this new window
		self.cal.clicked.connect(self.closeCal)
		self.calendarWindow.show()

	def closeCal(self):
		self.calendarWindow.hide()

	def startDate(self,date):
		self.label1.setText(date.toString('dd/MM/yyyy'))
		return

	def endDate(self,date):
		self.label2.setText(date.toString('dd/MM/yyyy'))
		return

if __name__ == '__main__':
	app = QApplication(sys.argv)
	trade_ = TradeMainWindow()
	sys.exit(app.exec_())
