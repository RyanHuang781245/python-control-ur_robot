import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QGridLayout
from control.state_machine import ControlModule

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("夾娃娃機控制介面")
        self.control_module = ControlModule()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        grid = QGridLayout()

        # 建立按鈕
        self.btn_forward = QPushButton("前")
        self.btn_backward = QPushButton("後")
        self.btn_left = QPushButton("左")
        self.btn_right = QPushButton("右")
        self.btn_grab = QPushButton("抓取")

        grid.addWidget(self.btn_forward, 0, 1)
        grid.addWidget(self.btn_left, 1, 0)
        grid.addWidget(self.btn_right, 1, 2)
        grid.addWidget(self.btn_backward, 2, 1)
        grid.addWidget(self.btn_grab, 3, 1)

        # 狀態訊息顯示區
        self.status_label = QLabel("系統初始化中...")
        self.control_module.handle_initial_command() #夾爪移動至初始位置
        grid.addWidget(self.status_label, 4, 0, 1, 3)

        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        # 綁定按鈕事件
        self.btn_forward.clicked.connect(lambda: self.send_command("forward"))
        self.btn_backward.clicked.connect(lambda: self.send_command("backward"))
        self.btn_left.clicked.connect(lambda: self.send_command("left"))
        self.btn_right.clicked.connect(lambda: self.send_command("right"))
        self.btn_grab.clicked.connect(lambda: self.send_command("grab"))

    def send_command(self, cmd):
        if cmd in ["forward", "backward", "left", "right"]:
            result = self.control_module.handle_move_command(cmd)
            # current_pose = self.control_module.get_current_pose()
            # print(current_pose)
        elif cmd == "grab":
            result = self.control_module.handle_command("grab")
        else:
            result = "未知命令"
        self.status_label.setText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
