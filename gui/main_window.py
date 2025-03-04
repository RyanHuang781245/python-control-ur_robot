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

        # 新增方向按鈕，排列成 3×3 格局：
        # 第一列：左前、前、右前
        self.btn_left_forward = QPushButton("左前")
        self.btn_forward = QPushButton("前")
        self.btn_right_forward = QPushButton("右前")
        # 第二列：左、右（中間留空）
        self.btn_left = QPushButton("左")
        self.btn_right = QPushButton("右")
        # 第三列：左後、後、右後
        self.btn_left_backward = QPushButton("左後")
        self.btn_backward = QPushButton("後")
        self.btn_right_backward = QPushButton("右後")
        # 抓取按鈕放置在第四列中間
        self.btn_grab = QPushButton("抓取")

        grid.addWidget(self.btn_left_forward, 0, 0)
        grid.addWidget(self.btn_forward, 0, 1)
        grid.addWidget(self.btn_right_forward, 0, 2)
        grid.addWidget(self.btn_left, 1, 0)
        grid.addWidget(self.btn_right, 1, 2)
        grid.addWidget(self.btn_left_backward, 2, 0)
        grid.addWidget(self.btn_backward, 2, 1)
        grid.addWidget(self.btn_right_backward, 2, 2)
        grid.addWidget(self.btn_grab, 3, 1)

        # 狀態訊息顯示區放在最下方
        self.status_label = QLabel("系統初始化中...")
        self.control_module.handle_initial_command()
        grid.addWidget(self.status_label, 4, 0, 1, 3)

        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        # 各方向按鈕皆以單次點擊事件觸發對應指令
        self.btn_left_forward.clicked.connect(lambda: self.send_command("left_forward"))
        self.btn_forward.clicked.connect(lambda: self.send_command("forward"))
        self.btn_right_forward.clicked.connect(lambda: self.send_command("right_forward"))
        self.btn_left.clicked.connect(lambda: self.send_command("left"))
        self.btn_right.clicked.connect(lambda: self.send_command("right"))
        self.btn_left_backward.clicked.connect(lambda: self.send_command("left_backward"))
        self.btn_backward.clicked.connect(lambda: self.send_command("backward"))
        self.btn_right_backward.clicked.connect(lambda: self.send_command("right_backward"))

        # 抓取按鈕單次觸發
        self.btn_grab.clicked.connect(lambda: self.send_command("grab"))

    def send_command(self, cmd):
        # 方向命令使用 handle_move_command，其他命令則使用 handle_command
        if cmd in ["forward", "backward", "left", "right",
                   "left_forward", "right_forward", "left_backward", "right_backward"]:
            result = self.control_module.handle_move_command(cmd)
        else:
            result = self.control_module.handle_command(cmd)
        self.status_label.setText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
