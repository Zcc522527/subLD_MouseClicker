# -*- coding: utf-8 -*-
"""
鼠标自动连点器模块 - subLD项目
使用幽灵键鼠硬件实现鼠标连点
"""
import time
import threading
from PySide6.QtCore import QObject, Signal
from ghost_mouse import get_ghost_mouse


class MouseAutoClicker(QObject):
    """鼠标自动连点器（使用幽灵键鼠）"""
    
    # 定义信号
    status_changed = Signal(bool)  # 连点状态改变信号
    click_count_changed = Signal(int)  # 点击次数改变信号
    error_occurred = Signal(str)  # 错误信号
    
    def __init__(self, interval=0.1):
        """
        初始化连点器
        :param interval: 点击间隔时间(秒)，默认0.1秒
        """
        super().__init__()
        self.interval = interval
        self.is_clicking = False
        self.is_enabled = False  # 是否启用连点功能
        self.click_thread = None
        self.click_count = 0
        self._should_stop = False
        
        # 获取幽灵键鼠实例
        self.ghost = get_ghost_mouse()
        
        # 监听状态
        self._left_button_pressed = False
    
    def enable(self) -> bool:
        """
        启用连点器（连接幽灵键鼠）
        :return: 成功返回True
        """
        if self.is_enabled:
            return True
        
        # 连接幽灵键鼠
        if self.ghost.connect():
            self.is_enabled = True
            print("✅ 连点器已启用")
            return True
        else:
            error_msg = "无法连接幽灵键鼠设备，请检查:\n1. 硬件是否已插入\n2. 驱动是否已安装\n3. 是否以管理员权限运行"
            self.error_occurred.emit(error_msg)
            return False
    
    def disable(self):
        """禁用连点器"""
        if not self.is_enabled:
            return
        
        # 停止当前连点
        self.stop_clicking()
        
        # 断开幽灵键鼠
        self.ghost.disconnect()
        self.is_enabled = False
        print("🔌 连点器已禁用")
    
    def start_clicking(self):
        """开始连点"""
        if not self.is_enabled:
            self.error_occurred.emit("连点器未启用，请先点击【启用连点】")
            return
        
        if self.is_clicking:
            return
        
        self.is_clicking = True
        self.click_count = 0
        self._should_stop = False
        self._left_button_pressed = True
        
        # 启动连点线程
        self.click_thread = threading.Thread(target=self._click_loop, daemon=True)
        self.click_thread.start()
        
        self.status_changed.emit(True)
        print("🖱️ 开始连点...")
    
    def stop_clicking(self):
        """停止连点"""
        if not self.is_clicking:
            return
        
        self.is_clicking = False
        self._should_stop = True
        self._left_button_pressed = False
        
        # 等待线程结束
        if self.click_thread and self.click_thread.is_alive():
            self.click_thread.join(timeout=1)
        
        # 确保左键松开
        self.ghost.left_up()
        
        self.status_changed.emit(False)
        print(f"⏹️ 停止连点，共点击 {self.click_count} 次")
    
    def _click_loop(self):
        """连点循环（线程函数）"""
        while self.is_clicking and not self._should_stop:
            try:
                # 使用幽灵键鼠执行点击
                if self.ghost.left_click():
                    self.click_count += 1
                    self.click_count_changed.emit(self.click_count)
                else:
                    # 点击失败，可能设备断开
                    error_msg = "点击失败，幽灵键鼠可能断开连接"
                    self.error_occurred.emit(error_msg)
                    break
                
                # 等待间隔时间
                time.sleep(self.interval)
                
            except Exception as e:
                print(f"❌ 连点出错: {e}")
                self.error_occurred.emit(f"连点出错: {str(e)}")
                break
        
        # 循环结束，确保状态正确
        if self.is_clicking:
            self.is_clicking = False
            self.status_changed.emit(False)
    
    def set_interval(self, interval: float):
        """
        设置点击间隔
        :param interval: 间隔时间(秒)，最小值为0.01
        """
        self.interval = max(0.01, interval)
        print(f"⏱️ 点击间隔已设置为: {self.interval}秒")
    
    def get_status(self) -> dict:
        """获取当前状态"""
        return {
            'is_enabled': self.is_enabled,
            'is_clicking': self.is_clicking,
            'click_count': self.click_count,
            'interval': self.interval,
            'ghost_connected': self.ghost.is_connected
        }
    
    def simulate_left_button_press(self):
        """模拟左键按下事件（用于外部触发）"""
        if self.is_enabled and not self.is_clicking:
            self.start_clicking()
    
    def simulate_left_button_release(self):
        """模拟左键松开事件（用于外部触发）"""
        if self.is_enabled and self.is_clicking:
            self.stop_clicking()


# 测试代码
if __name__ == "__main__":
    import sys
    from PySide6.QtCore import QCoreApplication
    
    app = QCoreApplication(sys.argv)
    
    print("=== subLD 鼠标连点器测试 ===")
    
    clicker = MouseAutoClicker(interval=0.1)
    
    def on_status_changed(is_clicking):
        status = "连点中" if is_clicking else "已停止"
        print(f"状态改变: {status}")
    
    def on_click_count_changed(count):
        if count % 10 == 0:  # 每10次打印一次
            print(f"已点击: {count} 次")
    
    def on_error(error_msg):
        print(f"错误: {error_msg}")
    
    clicker.status_changed.connect(on_status_changed)
    clicker.click_count_changed.connect(on_click_count_changed)
    clicker.error_occurred.connect(on_error)
    
    # 启用连点器
    if clicker.enable():
        print("\n3秒后开始连点...")
        time.sleep(3)
        
        # 开始连点
        clicker.start_clicking()
        
        # 连点5秒
        time.sleep(5)
        
        # 停止连点
        clicker.stop_clicking()
        
        # 禁用连点器
        clicker.disable()
    
    print("\n测试完成！")
