from PySide6 import QtWidgets, QtGui, QtCore
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui
import random
import os

# 1.ฟังก์ชันเชื่อมต่อกับ MAYA
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

# 2.ห้อง UI หลัก
class RiverRushUI(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super().__init__(parent)

        # ตั้งค่าเรือ
        self.boat_speed = 20
        self.boat_x_start = 300
        self.boat_y_start = 600
        self.boat_x = self.boat_x_start
        self.boat_y = self.boat_y_start

		# ตั้งค่าเของสุ่ม
        self.obstacles = []  
        self.obstacle_speed = 7

        # --- ตั้งค่า Path รูปภาพ (สำคัญมาก!) ---
        # แก้ไข Path ตรงนี้ให้ตรงกับตำแหน่งโฟลเดอร์ images ของคุณ
        self.IMAGE_DIR = "C:/Users/ICT68/Documents/maya/2025/scripts/RiverRush/images"

        # ตั้งค่า Timers 
        self.game_timer = QtCore.QTimer(self)
        self.game_timer.timeout.connect(self.update_game)

        self.spawn_timer = QtCore.QTimer(self)
        self.spawn_timer.timeout.connect(self.spawn_obstacle)

        # สร้าง UI ทั้งหน้าเมนูและหน้าเกม
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("RIVER RUSH GAME ❤️")
        self.setFixedSize(700, 800)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        # สร้าง Layout หลักแบบสลับหน้า 
        self.stacked_layout = QtWidgets.QStackedLayout(self)

        # สร้างหน้าเมนู (หน้าที่ 0) 
        self.menu_widget = self._create_menu_widget()
        self.stacked_layout.addWidget(self.menu_widget)

        # -สร้างหน้าเกม (หน้าที่ 1) 
        self.game_widget = self._create_game_widget()
        self.stacked_layout.addWidget(self.game_widget)

        # เริ่มต้นโดยการแสดงหน้าเมนู
        self.stacked_layout.setCurrentWidget(self.menu_widget)

#--------------------------------------------------------------

    def _create_menu_widget(self):
        """สร้าง Widget สำหรับหน้าเมนู"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # ชื่อเกม
        title = QtWidgets.QLabel("🏞️ RIVER RUSH 🛶")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 50px; font-weight: bold; color: #2E8B57; margin-bottom: 20px;")
        layout.addWidget(title)

        # ปุ่มกดเริ่มเกม ออกเกม
        start_button = QtWidgets.QPushButton("เริ่มเกม")
        quit_button = QtWidgets.QPushButton("ออก")

        start_button.clicked.connect(self.start_game)
        quit_button.clicked.connect(self.close)

        # ตั้งค่าสีปุ่มกดเริ่มเกม ออกเกม
        button_style_green = """
            QPushButton {
                background-color: #4CAF50; color: white; font-size: 30px; font-weight: bold; 
                border-radius: 15px; padding: 10px 25px; margin: 10px;
            }
            QPushButton:hover { background-color: #45a049; }
        """
        button_style_red = """
            QPushButton {
                background-color: #ff4d4d; color: white; font-size: 30px; font-weight: bold;
                border-radius: 15px; padding: 10px 25px; margin: 10px;
            }
            QPushButton:hover { background-color: #e63946; }
        """
        start_button.setStyleSheet(button_style_green)
        quit_button.setStyleSheet(button_style_red)

        layout.addWidget(start_button)
        layout.addWidget(quit_button)
        layout.addStretch()

        return widget

#--------------------------------------------------------------

    def _create_game_widget(self):
        """สร้าง Widget สำหรับหน้าเกม"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # คะแนนและหัวใจซ้ายขวา
        info_layout = QtWidgets.QHBoxLayout()
        info_layout.setContentsMargins(10, 10, 10, 10)
        self.heart_label = QtWidgets.QLabel("❤️: 3")
        self.score_label = QtWidgets.QLabel("คะแนน: 0")
        self.heart_label.setStyleSheet("color: #ff4d4d; font-size: 30px; font-weight: bold; background-color: #ffe6e6; border-radius: 15px; padding: 5px;")
        self.score_label.setStyleSheet("color: #0073e6; font-size: 30px; font-weight: bold; background-color: #e6f3ff; border-radius: 15px; padding: 5px;")
        info_layout.addWidget(self.heart_label)
        info_layout.addStretch()
        info_layout.addWidget(self.score_label)
        layout.addLayout(info_layout)

        # พื้นน้ำ
        self.game_area = QtWidgets.QLabel()
        self.game_area.setFixedSize(700, 700)
        self.game_area.setStyleSheet("background-color: #4f94cb; border: 2px solid #0077cc;")
        layout.addWidget(self.game_area)

        # เรือ
        self.boat = QtWidgets.QLabel(self.game_area)
        self.boat.setPixmap(QtGui.QPixmap("C:/Users/nadia/Documents/maya/2026/scripts/RiverRush/images/ship.PNG").scaled(100, 100, QtCore.Qt.KeepAspectRatio))
        self.boat.setGeometry(self.boat_x, self.boat_y, 100, 100)


        return widget

#--------------------------------------------------------------

    def start_game(self):
        """รีเซ็ตและเริ่มเกม"""
        # รีเซ็ตค่าต่างๆ
        self.reset_game_state()

        # สลับไปหน้าจอเล่นเกม
        self.stacked_layout.setCurrentWidget(self.game_widget)
        self.setFocus() # สำคัญมากเพื่อให้รับการกดปุ่มได้

        # เริ่ม Timer
        self.game_timer.start(30)  # 30 ms update rate
        self.spawn_timer.start(1000) # 1 วินาที spawn 1 ครั้ง

    def reset_game_state(self):
        """ล้างค่าและวัตถุในเกมเพื่อเริ่มใหม่"""
        # หยุด Timer (ถ้าทำงานอยู่)
        self.game_timer.stop()
        self.spawn_timer.stop()

        # ลบสิ่งกีดขวางเก่าทั้งหมด
        for obs in self.obstacles:
            obs.deleteLater()
        self.obstacles.clear()

        # รีเซ็ตตำแหน่งเรือ
        self.boat_x = self.boat_x_start
        self.boat_y = self.boat_y_start
        self.boat.move(self.boat_x, self.boat_y)

        # รีเซ็ตคะแนนและพลังชีวิต
        self.score_label.setText("คะแนน: 0")
        self.heart_label.setText("❤️: 3")


    def spawn_obstacle(self):
        """สุ่มสร้างท่อนไม้หรือหิน"""
        obstacle = QtWidgets.QLabel(self.game_area)
        x = random.randint(0, self.game_area.width() - 80)

        # สุ่มว่าจะสร้างอะไร
        if random.choice([True, False]):
            image_path = os.path.join(self.IMAGE_DIR, "log01.PNG")
        else:
            image_path = os.path.join(self.IMAGE_DIR, "rock01.PNG")

        obstacle.setPixmap(QtGui.QPixmap(image_path).scaled(80, 80, QtCore.Qt.KeepAspectRatio))
        obstacle.setGeometry(x, -80, 80, 80) # เริ่มจากข้างบนนอกจอ
        obstacle.show()
        self.obstacles.append(obstacle)

        #ตำแหน่งของสิ่งกีดขวางและตรวจสอบการชน
    def update_game(self):
        for obs in self.obstacles[:]:
            obs.move(obs.x(), obs.y() + self.obstacle_speed)

            if obs.y() > self.game_area.height():
                self.obstacles.remove(obs)
                obs.deleteLater()

            if self.boat.geometry().intersects(obs.geometry()):
                self.game_over()
                return
        #จบเกม
    def game_over(self):
        self.game_timer.stop()
        self.spawn_timer.stop()

        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("💀เรือชน💀")
        msg.setText(" จบเกมจ้า!")
        msg.exec_()
        
        # กลับไปที่หน้าเมนูเริ่มต้น
        self.stacked_layout.setCurrentWidget(self.menu_widget)


    def keyPressEvent(self, event):
        if not self.game_timer.isActive():
            return 

        if event.key() == QtCore.Qt.Key_Left:
            self.boat_x = max(0, self.boat_x - self.boat_speed)
        elif event.key() == QtCore.Qt.Key_Right:
            max_x = self.game_area.width() - self.boat.width()
            self.boat_x = min(max_x, self.boat_x + self.boat_speed)

        self.boat.move(self.boat_x, self.boat_y)

def main():
    try:
        global river_rush_ui_instance
        river_rush_ui_instance.close()
        river_rush_ui_instance.deleteLater()
    except:
        pass

    river_rush_ui_instance = RiverRushUI()
    river_rush_ui_instance.show()
    return river_rush_ui_instance