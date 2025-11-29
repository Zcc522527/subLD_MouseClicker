# -*- coding: utf-8 -*-
"""
幽灵键鼠封装模块 - subLD项目
支持通过COM接口调用幽灵键鼠硬件
"""
import win32com.client
import time
from typing import Optional


class GhostMouse:
    """幽灵键鼠封装类"""
    
    def __init__(self):
        """初始化幽灵键鼠"""
        self.km = None
        self.is_connected = False
        
    def connect(self) -> bool:
        """
        连接幽灵键鼠设备
        :return: 连接成功返回True，失败返回False
        """
        try:
            # 创建COM对象，这里的ProgID根据实际的幽灵键鼠型号可能不同
            # 常见的有: "kmclass.kmsoft" 或 "sr.srsoft"
            self.km = win32com.client.Dispatch("kmclass.kmsoft")
            self.is_connected = True
            print("✅ 幽灵键鼠连接成功")
            return True
        except Exception as e:
            print(f"❌ 幽灵键鼠连接失败: {e}")
            print("请确保:")
            print("1. 幽灵键鼠硬件已插入USB端口")
            print("2. 已安装幽灵键鼠驱动程序")
            print("3. COM组件已正确注册")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.km:
            self.km = None
            self.is_connected = False
            print("🔌 幽灵键鼠已断开连接")
    
    def check_connection(self) -> bool:
        """检查连接状态"""
        return self.is_connected and self.km is not None
    
    # ==================== 鼠标操作 ====================
    
    def left_click(self) -> bool:
        """
        鼠标左键点击（按下并松开）
        :return: 成功返回True
        """
        if not self.check_connection():
            print("⚠️ 幽灵键鼠未连接")
            return False
        
        try:
            self.km.LeftDown()  # 左键按下
            time.sleep(0.01)  # 短暂延迟
            self.km.LeftUp()    # 左键松开
            return True
        except Exception as e:
            print(f"❌ 左键点击失败: {e}")
            return False
    
    def left_down(self) -> bool:
        """
        鼠标左键按下
        :return: 成功返回True
        """
        if not self.check_connection():
            return False
        
        try:
            result = self.km.LeftDown()
            return result == 1
        except Exception as e:
            print(f"❌ 左键按下失败: {e}")
            return False
    
    def left_up(self) -> bool:
        """
        鼠标左键松开
        :return: 成功返回True
        """
        if not self.check_connection():
            return False
        
        try:
            result = self.km.LeftUp()
            return result == 1
        except Exception as e:
            print(f"❌ 左键松开失败: {e}")
            return False
    
    def right_click(self) -> bool:
        """鼠标右键点击"""
        if not self.check_connection():
            return False
        
        try:
            self.km.RightDown()
            time.sleep(0.01)
            self.km.RightUp()
            return True
        except Exception as e:
            print(f"❌ 右键点击失败: {e}")
            return False
    
    def middle_click(self) -> bool:
        """鼠标中键点击"""
        if not self.check_connection():
            return False
        
        try:
            self.km.MiddleDown()
            time.sleep(0.01)
            self.km.MiddleUp()
            return True
        except Exception as e:
            print(f"❌ 中键点击失败: {e}")
            return False
    
    def move_to(self, x: int, y: int) -> bool:
        """
        移动鼠标到指定坐标（绝对坐标）
        :param x: X坐标
        :param y: Y坐标
        :return: 成功返回True
        """
        if not self.check_connection():
            return False
        
        try:
            result = self.km.MoveTo(x, y)
            return result == 1
        except Exception as e:
            print(f"❌ 移动鼠标失败: {e}")
            return False
    
    def move_relative(self, dx: int, dy: int) -> bool:
        """
        相对移动鼠标
        :param dx: X轴偏移量
        :param dy: Y轴偏移量
        :return: 成功返回True
        """
        if not self.check_connection():
            return False
        
        try:
            result = self.km.MoveR(dx, dy)
            return result == 1
        except Exception as e:
            print(f"❌ 相对移动失败: {e}")
            return False
    
    # ==================== 键盘操作 ====================
    
    def key_press(self, key: str) -> bool:
        """
        按键（按下并松开）
        :param key: 按键名称，如 "A", "1", "F1", "Enter" 等
        :return: 成功返回True
        """
        if not self.check_connection():
            return False
        
        try:
            self.km.KeyDown(key)
            time.sleep(0.01)
            self.km.KeyUp(key)
            return True
        except Exception as e:
            print(f"❌ 按键失败: {e}")
            return False
    
    def key_down(self, key: str) -> bool:
        """按键按下"""
        if not self.check_connection():
            return False
        
        try:
            result = self.km.KeyDown(key)
            return result == 1
        except Exception as e:
            print(f"❌ 按键按下失败: {e}")
            return False
    
    def key_up(self, key: str) -> bool:
        """按键松开"""
        if not self.check_connection():
            return False
        
        try:
            result = self.km.KeyUp(key)
            return result == 1
        except Exception as e:
            print(f"❌ 按键松开失败: {e}")
            return False
    
    def key_up_all(self) -> bool:
        """释放所有按键"""
        if not self.check_connection():
            return False
        
        try:
            result = self.km.KeyUpAll()
            return result == 1
        except Exception as e:
            print(f"❌ 释放所有按键失败: {e}")
            return False


# 全局幽灵键鼠实例（单例模式）
_ghost_mouse_instance: Optional[GhostMouse] = None


def get_ghost_mouse() -> GhostMouse:
    """
    获取全局幽灵键鼠实例（单例模式）
    :return: GhostMouse实例
    """
    global _ghost_mouse_instance
    if _ghost_mouse_instance is None:
        _ghost_mouse_instance = GhostMouse()
    return _ghost_mouse_instance


# 测试代码
if __name__ == "__main__":
    print("=== 幽灵键鼠测试 - subLD ===")
    
    # 创建实例
    ghost = GhostMouse()
    
    # 连接设备
    if ghost.connect():
        print("\n测试鼠标点击...")
        ghost.left_click()
        time.sleep(0.5)
        
        print("测试完成！")
        ghost.disconnect()
    else:
        print("无法连接幽灵键鼠，请检查设备")
