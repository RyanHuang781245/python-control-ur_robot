import logging
from comm.socket_client import SocketClient
from control.motion_commands import URScriptGenerator
from utils.boundary_checker import is_within_boundaries

# 請根據您的 UR5 控制器設定 IP 與 Port
UR5_IP = "10.0.2.15"
UR5_PORT = 30002

class ControlModule:
    def __init__(self):
        self.state = "idle"  # 初始狀態
        self.logger = logging.getLogger("ControlModule")
        self.socket_client = SocketClient(UR5_IP, UR5_PORT)
        self.socket_client.connect()
        self.command_generator = URScriptGenerator()
        # 初始 TCP (x, y, z, rx, ry, rz) 值，依據實際初始位置設定
        self.current_tcp = [0.279134293245, 0.045957778215, 0.218270318258, 2.216666768333, -2.213592243070, -0.007045821207]

    def compute_new_tcp(self, delta):
        """
        根據目前 TCP 與增量 delta 計算新目標 TCP (僅更新 x, y)
        """
        new_tcp = self.current_tcp.copy()
        new_tcp[0] += delta[0]
        new_tcp[1] += delta[1]
        return new_tcp
    
    def handle_initial_command(self):
        ur_command = self.command_generator.initial_command()
        self.socket_client.send_command(ur_command)

    def handle_move_command(self, direction):
        """
        處理水平移動命令，先計算新 TCP,檢查是否在邊界範圍內
        若合法則發送移動指令，否則返回錯誤訊息。
        """
        if direction == "forward":
            delta = [self.command_generator.step, 0, 0]
        elif direction == "backward":
            delta = [-self.command_generator.step, 0, 0]
        elif direction == "left":
            delta = [0, self.command_generator.step, 0]
        elif direction == "right":
            delta = [0, -self.command_generator.step, 0]
        else:
            return "未知指令"

        new_tcp = self.compute_new_tcp(delta)
        print(new_tcp)
        if not is_within_boundaries(new_tcp):
            self.logger.warning("Target TCP {} out of boundaries".format(new_tcp))
            return "指令超出邊界，無法執行"

        # 更新目前 TCP 並發送指令
        self.current_tcp = new_tcp
        ur_command = self.command_generator.generate_move_command(direction)
        self.socket_client.send_command(ur_command)
        # response = self.socket_client.receive_response()
        # return "執行移動：" + direction + "，回傳：" + str(response)

    def handle_command(self, cmd):
        """
        根據傳入的 cmd(包含移動與抓取)，呼叫對應方法處理
        """
        if self.state != "idle" and cmd != "stop":
            self.logger.warning("State {} not idle, command {} rejected".format(self.state, cmd))
            return "當前忙碌中，請稍後再試"
        
        if cmd in ["forward", "backward", "left", "right"]:
            self.state = "moving"
            result = self.handle_move_command(cmd)
        elif cmd == "grab":
            self.state = "grabbing"
            ur_command = self.command_generator.generate_grab_command()
            self.socket_client.send_command(ur_command)
            # response = self.socket_client.receive_response()
            # result = "執行抓取，回傳：" + str(response)
        elif cmd == "stop":
            self.state = "idle"
            ur_command = "stop"
            self.socket_client.send_command(ur_command)
            result = "停止操作"
        else:
            result = "未知命令"
        
        self.logger.info("Command {} processed with result: {}".format(cmd, result))
        self.state = "idle"
        return result
