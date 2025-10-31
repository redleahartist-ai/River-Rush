from PySide6 import QtWidgets, QtGui, QtCore
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui
import random
import os

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class project_ui(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super().__init__(parent)

        self.boat_speed = 20
        self.boat_x_start = 300
        self.boat_y_start = 600
        self.boat_x = self.boat_x_start
        self.boat_y = self.boat_y_start

        self.obstacles = []  
        self.obstacle_speed = 3

        self.high_score = 0
        self.IMAGE_DIR = "C:/Users/nadia/Documents/maya/2026/scripts/661310088_project/images"

        self.game_timer = QtCore.QTimer(self)
        self.game_timer.timeout.connect(self.update_game)

        self.spawn_timer = QtCore.QTimer(self)
        self.spawn_timer.timeout.connect(self.spawn_obstacle)

        self.setup_ui()

    def setup_ui(self):
        icon_path = os.path.join(self.IMAGE_DIR, "C:/Users/nadia/Documents/maya/2026/scripts/661310088_project/icons", "icons1.PNG")
        self.setWindowIcon(QtGui.QIcon(icon_path))
        
        self.setWindowTitle("RIVER RUSH GAME!!!!")
        self.setFixedSize(700, 800)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.stacked_layout = QtWidgets.QStackedLayout(self)
        self.setLayout(self.stacked_layout) 

        self.menu_widget = self._create_menu_widget()
        self.stacked_layout.addWidget(self.menu_widget)

        self.game_widget = self._create_game_widget()
        self.stacked_layout.addWidget(self.game_widget)
        
        self.game_over_widget = self._create_game_over_widget()
        self.stacked_layout.addWidget(self.game_over_widget)

        self.stacked_layout.setCurrentWidget(self.menu_widget)

    def _create_menu_widget(self):
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background-color: #88daf2;") 

        layout = QtWidgets.QVBoxLayout(widget)
        layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter) 
        layout.setContentsMargins(0, 0, 0, 20) 

        image_label = QtWidgets.QLabel()
        
        image_path = os.path.join(self.IMAGE_DIR, "BG1.PNG") 
        pixmap = QtGui.QPixmap(image_path)
        
        if not pixmap.isNull(): 
            scaled_pixmap = pixmap.scaledToWidth(self.width(), QtCore.Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)

        image_label.setStyleSheet("margin-bottom: 3px;") 
        layout.addWidget(image_label)
        
        start_button = QtWidgets.QPushButton("เริ่มเกม")
        quit_button = QtWidgets.QPushButton("ออก")

        start_button.clicked.connect(self.start_game)
        quit_button.clicked.connect(self.close)

        button_style_green = '''
            QPushButton { 
                background-color: #4CAF50;
                color: white; font-size: 30px;
                font-weight: bold; 
                border-radius: 15px;
                padding: 10px 25px; 
                margin: 10px; 
            }
            QPushButton:hover { 
                background-color: #45a049; 
            }
        '''
        button_style_red = '''
            QPushButton { 
                background-color: #ff4d4d; 
                color: white; font-size: 30px; 
                font-weight: bold;
                border-radius: 15px; 
                padding: 10px 25px; 
                margin: 10px;
            }
            QPushButton:hover { 
                background-color: #e63946; 
                }
        '''
        start_button.setStyleSheet(button_style_green)
        quit_button.setStyleSheet(button_style_red)

        button_layout = QtWidgets.QVBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter) 
        button_layout.addWidget(start_button)
        button_layout.addWidget(quit_button)

        layout.addLayout(button_layout) 
        layout.addStretch() 

        return widget

    def _create_game_widget(self):
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background-color: #C2E2F2;") 
        
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        info_layout = QtWidgets.QHBoxLayout()
        info_layout.setContentsMargins(10, 10, 10, 10)
        self.heart_label = QtWidgets.QLabel("❤️: 3")
        self.high_score_label = QtWidgets.QLabel(f"คะแนนสูงสุด: {self.high_score}")      
        self.score_label = QtWidgets.QLabel("คะแนน: 0")
        
        self.heart_label.setStyleSheet(
            '''
                color: #ff4d4d; 
                font-size: 30px; 
                font-weight: bold; 
                background-color: #ffe6e6; 
                border-radius: 15px; 
                padding: 5px;
            '''
            )

        style_high_score = "color: #28a745; font-size: 30px; font-weight: bold; background-color: #e6ffef; border-radius: 15px; padding: 5px;"
        self.high_score_label.setStyleSheet(style_high_score)
        self.score_label.setStyleSheet("color: #0073e6; font-size: 30px; font-weight: bold; background-color: #e6f3ff; border-radius: 15px; padding: 5px;")
        
        info_layout.addWidget(self.heart_label)
        info_layout.addStretch()
        info_layout.addWidget(self.high_score_label)
        info_layout.addSpacing(15)
        info_layout.addWidget(self.score_label)
        layout.addLayout(info_layout)

        self.game_area = QtWidgets.QLabel()
        self.game_area.setFixedSize(700, 700)
        self.game_area.setStyleSheet("background-color: #7cc8ff; border: 2px solid #7cc8ff;")
        layout.addWidget(self.game_area)

        self.boat = QtWidgets.QLabel(self.game_area)
        self.boat.setFocusPolicy(QtCore.Qt.NoFocus)
        
        ship_image_path = os.path.join(self.IMAGE_DIR, "ship01.PNG") 
        self.boat.setPixmap(QtGui.QPixmap(ship_image_path).scaled(100, 100, QtCore.Qt.KeepAspectRatio))
        self.boat.setGeometry(self.boat_x, self.boat_y, 100, 100)

        self.boat.setStyleSheet("outline: none; border: none;")

        return widget

    
    def _create_game_over_widget(self):
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background-color: #C2E2F2;") 

        layout = QtWidgets.QVBoxLayout(widget)
        layout.setAlignment(QtCore.Qt.AlignCenter) 
        layout.setContentsMargins(50, 50, 50, 50) 

        game_over_label = QtWidgets.QLabel("แพ้แล้ว!")
        game_over_label.setAlignment(QtCore.Qt.AlignCenter)
        game_over_label.setStyleSheet("color: #D9534F; font-size: 60px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(game_over_label)
        
        self.final_score_label = QtWidgets.QLabel("คะแนนของคุณ: 0")
        self.final_score_label.setAlignment(QtCore.Qt.AlignCenter)
        self.final_score_label.setStyleSheet("color: #0073e6; font-size: 40px; font-weight: bold; margin-top: 30px;")
        layout.addWidget(self.final_score_label)

        restart_button = QtWidgets.QPushButton("🔥เล่นอีกครั้ง🔥")
        back_to_menu_button = QtWidgets.QPushButton("กลับเมนูหลัก")

        restart_button.clicked.connect(self.start_game) 
        back_to_menu_button.clicked.connect(self.back_to_menu)

        button_style_green = '''
            QPushButton { 
                    background-color: #4CAF50; 
                    color: white; font-size: 25px; 
                    font-weight: bold; 
                    border-radius: 12px; 
                    padding: 10px 20px; 
                    margin: 8px; 
                }
            QPushButton:hover { 
                    background-color: #45a049; 
                }
        '''
        button_style_red = '''
            QPushButton { 
                    background-color: #ff4d4d; 
                    color: white; font-size: 25px; 
                    font-weight: bold;
                    border-radius: 12px; 
                    padding: 10px 20px; 
                    margin: 8px; 
                }
            QPushButton:hover { 
                    background-color: #e63946; 
                }
        '''
        restart_button.setStyleSheet(button_style_green) 
        back_to_menu_button.setStyleSheet(button_style_red) 

        layout.addSpacing(40) 
        layout.addWidget(restart_button)
        layout.addWidget(back_to_menu_button)
        
        layout.addStretch() 

        return widget

    def start_game(self):
        self.reset_game_state()
        self.stacked_layout.setCurrentWidget(self.game_widget)
        self.setFocus() 
        self.game_timer.start(30)  
        self.spawn_timer.start(1000) 

    def reset_game_state(self):
        self.game_timer.stop()
        self.spawn_timer.stop()

        for obs in self.obstacles:
            obs.deleteLater()
        self.obstacles.clear()

        self.boat_x = self.boat_x_start
        self.boat_y = self.boat_y_start
        self.boat.move(self.boat_x, self.boat_y)

        self.score = 0  
        self.lives = 3
        self.obstacle_speed = 10 

        self.score_label.setText(f"คะแนน: {self.score}")
        self.heart_label.setText(f"❤️: {self.lives}")

    def update_game(self):
        for obs in self.obstacles[:]:
            obs.move(obs.x(), obs.y() + self.obstacle_speed)

            if obs.y() > self.game_area.height():
                self.obstacles.remove(obs)
                obs.deleteLater()
                
                self.score += 1
                self.score_label.setText(f"คะแนน: {self.score}")
                
                if self.score > 0 and self.score % 5 == 0:
                    self.obstacle_speed += 2  
                    print(f"เลเวลอัป!เพิ่มความเร็วแล้วนะ!! คะแนน: {self.score}, ความเร็วเพิ่มขึ้น: {self.obstacle_speed}")
                
            if self.boat.geometry().intersects(obs.geometry()):
                self.obstacles.remove(obs)
                obs.deleteLater()
                
                self.lives -= 1
                self.heart_label.setText(f"❤️: {self.lives}")
                
                if self.lives <= 0:
                    self.game_over() 
                    return 

    def spawn_obstacle(self):
        obstacle = QtWidgets.QLabel(self.game_area)
        obstacle.setFocusPolicy(QtCore.Qt.NoFocus)
        x = random.randint(0, self.game_area.width() - 80)

        if random.choice([True, False]):
            image_path = os.path.join(self.IMAGE_DIR, "log02.PNG")
        else:
            image_path = os.path.join(self.IMAGE_DIR, "rock01.PNG")

        obstacle.setPixmap(QtGui.QPixmap(image_path).scaled(80, 80, QtCore.Qt.KeepAspectRatio))
        obstacle.setGeometry(x, -80, 80, 70) 

        obstacle.setStyleSheet("outline: none; border: none;")

        obstacle.show()
        self.obstacles.append(obstacle)

    def game_over(self):
        self.game_timer.stop()
        self.spawn_timer.stop()

        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.setText(f"คะแนนสูงสุด: {self.high_score}")      
        
        self.final_score_label.setText(f"คะแนนของคุณ: {self.score}")
        self.stacked_layout.setCurrentWidget(self.game_over_widget) 

    def back_to_menu(self):
        self.stacked_layout.setCurrentWidget(self.menu_widget)
        self.setFocus() 

    def keyPressEvent(self, event):
        if not self.game_timer.isActive():
            return 
        
        if event.key() == QtCore.Qt.Key_Left:
            self.boat_x = max(0, self.boat_x - self.boat_speed)
        elif event.key() == QtCore.Qt.Key_Right:
            max_x = self.game_area.width() - self.boat.width()
            self.boat_x = min(max_x, self.boat_x + self.boat_speed)

        self.boat.move(self.boat_x, self.boat_y)