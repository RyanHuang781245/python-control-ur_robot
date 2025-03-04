from gui.main_window import MainWindow
from utils.logger import setup_logger
import sys
from PyQt5.QtWidgets import QApplication
import threading
import time

def start_heartbeat(socket_client):
    # 啟動心跳檢測，確保連線狀態
    def heartbeat_loop():
        while True:
            if socket_client.connected:
                try:
                    socket_client.send_command("heartbeat")
                except Exception as e:
                    print("Heartbeat error:", e)
            time.sleep(2)
    t = threading.Thread(target=heartbeat_loop, daemon=True)
    t.start()

if __name__ == "__main__":
    setup_logger()
    app = QApplication(sys.argv)
    window = MainWindow()
    # 啟動心跳檢測
    start_heartbeat(window.control_module.socket_client)
    window.show()
    sys.exit(app.exec_())