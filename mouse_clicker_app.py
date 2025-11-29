# -*- coding: utf-8 -*-
"""
subLD 鼠标连点器 - 独立应用程序
使用幽灵键鼠硬件实现鼠标自动连点
"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from mouse_clicker_widget import MouseClickerWidget


class SubLDMouseClickerWindow(QMainWindow):
    """subLD 鼠标连点器主窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.check_admin_rights()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("subLD - 鼠标连点器")
        self.setMinimumSize(450, 600)
        self.setMaximumSize(550, 700)
        
        # 设置中央组件
        self.clicker_widget = MouseClickerWidget(self)
        self.setCentralWidget(self.clicker_widget)
        
        # 设置窗口图标（如果有的话）
        # self.setWindowIcon(QIcon("icon.png"))
        
        # 居中显示
        self.center_on_screen()
    
    def center_on_screen(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)
    
    def check_admin_rights(self):
        """检查是否以管理员权限运行"""
        import ctypes
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                QMessageBox.warning(
                    self,
                    "权限警告 - subLD",
                    "建议以管理员权限运行本程序\n"
                    "以确保幽灵键鼠正常工作！\n\n"
                    "右键点击程序 → 以管理员身份运行"
                )
        except:
            pass
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 确保连点器已停止
        self.clicker_widget.clicker.disable()
        event.accept()


def main():
    """主函数"""
    # 设置高DPI缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion样式
    app.setApplicationName("subLD")
    app.setOrganizationName("subLD")
    
    # 创建并显示主窗口
    window = SubLDMouseClickerWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
