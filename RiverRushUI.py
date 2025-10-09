from PySide6 import QtWidgets, QtGui,QtCore
from shiboken6 import wrapInstance

import maya.OpenMayaUI as omui

import importlib
import os

	#1.ฟังก์ชันเชื่อกับ MAYA
def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

	#2.ห้อง UI หลัก
class RiverRushUI(QtWidgets.QDialog):
	def __init__(self, parent=maya_main_window()):
		super().__init__(parent)
		self.setWindowTitle("RIVER RUSH GAME❤️")#ชื่อหน้าต่างUI
		self.setFixedSize(700, 1200)#ขนาดหน้าต่าง
		self.setup_ui()#สร้างปุ่มในหน้าต่าง

	#3. ฟังก์ชชันสร้างหน้าตา UI
	def setup_ui(self):
		self.main_layout = QtWidgets.QVBoxLayout(self)

		# แสดงชื่อเกมตรงกลางบนหัว
		self.title = QtWidgets.QLabel("🏞️ RIVER RUSH 🛶")
		self.title.setAlignment(QtCore.Qt.AlignCenter)
		self.title.setStyleSheet("font-size: 50px; font-weight: bold; color: #2E8B57;")
		self.main_layout.addWidget(self.title)

		# แสดงค่าพลังชีวิตและคะแนนซ้ายขวา
		# หัวใจ (พลังชีวิต)
		self.info_layout = QtWidgets.QHBoxLayout()
		self.heart_label = QtWidgets.QLabel("❤️: 3")
		self.heart_label.setAlignment(QtCore.Qt.AlignLeft)
		self.heart_label.setStyleSheet(
			"""
				QLabel {
					color: #ff4d4d;
					font-size: 30px;
					font-weight: bold;
					border: 1px solid #ff9999;
					border-radius: 15px;
					padding: 2px 6px;
					background-color: #ffe6e6;
				
				}
			"""
			)

		self.score_label = QtWidgets.QLabel("คะแนน: 0")
		self.score_label.setAlignment(QtCore.Qt.AlignRight)
		self.score_label.setStyleSheet(
			"""
				QLabel {
					color: #0073e6;
					font-size: 30px;
					font-weight: bold;
					border: 1px solid #99ccff;
					border-radius: 15px;
					padding: 2px 6px;
					background-color: #e6f3ff;
				}
			"""
			)

		self.info_layout.addWidget(self.heart_label)
		self.info_layout.addStretch()
		self.info_layout.addWidget(self.score_label)
		self.main_layout.addLayout(self.info_layout)
		# เพิ่มระยะห่างเล็กน้อยจาก title
		self.main_layout.addSpacing(10)
		self.main_layout.addSpacing(10)

		#เพิ่มเรือ(กำลังหาวิธีทำเรืออยู่ค่ะ)
		IMAGE_DIR = "C:/Users/nadia/Documents/maya/2026/scripts/RiverRush/images"
		



		#เพิ่มภาพฉากน้ำ
		IMAGE_DIR = "C:/Users/nadia/Documents/maya/2026/scripts/RiverRush/images"

		self.main_layout.addStretch()
		self.imageLabel = QtWidgets.QLabel()
		self.imagePixmap = QtGui.QPixmap(f'{IMAGE_DIR}/river.png')

		self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
		scaledPixmap = self.imagePixmap.scaled(
				QtCore.QSize(600, 700),
				QtCore.Qt.KeepAspectRatio,
				QtCore.Qt.SmoothTransformation
			)

		self.imageLabel.setPixmap(scaledPixmap)
		self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.main_layout.addWidget(self.imageLabel)

		self.main_layout.addStretch()

		# ปุ่มเริ่มเกม / เล่นใหม่ / ออก
		self.button_layout = QtWidgets.QVBoxLayout()
		self.start_button = QtWidgets.QPushButton("เริ่มเกม")
		self.restart_button = QtWidgets.QPushButton("เล่นใหม่")
		self.quit_button = QtWidgets.QPushButton("ออก")
		self.quit_button.clicked.connect(self.close)

		self.button_layout.addWidget(self.start_button)
		self.button_layout.addWidget(self.restart_button)
		self.button_layout.addWidget(self.quit_button)
		self.main_layout.addLayout(self.button_layout)

		# ปรับสีปุ่ม เริ่มเกม / เล่นใหม่ 



		for btn in [self.start_button,self.restart_button, self.restart_button,]:
			btn.setStyleSheet(
			"""
				QPushButton {
					background-color: #4CAF50;
					color: white;
					font-size: 30px;
					font-weight: bold;
					border-radius: 15px;
					padding: 10px 25px;
            		margin: 10px;                     
				} 
				QPushButton:hover {
					background-color: #45a049;
				}
			"""
			)
		# ปรับสีปุ่ม ออก
		for btn in [self.quit_button]:
			btn.setStyleSheet(
			"""
				QPushButton {
					background-color: #ff4d4d;
					color: white;
					font-size: 30px;
					font-weight: bold;
					border-radius: 15px;
					padding: 10px 25px;
            		margin: 10px;                   
				} 
				QPushButton:hover {
					background-color: #e63946;
				}
			"""
			)



def main():
	ui = RiverRushUI()
	ui.show()
	return ui

