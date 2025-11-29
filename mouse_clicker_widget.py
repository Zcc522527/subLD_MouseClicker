# -*- coding: utf-8 -*-
"""
鼠标连点器GUI组件 - subLD项目
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QDoubleSpinBox, QGroupBox, QLCDNumber,
    QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from mouse_auto_clicker import MouseAutoClicker


class MouseClickerWidget(QWidget):
    """鼠标连点器界面组件 - subLD"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicker = MouseAutoClicker(interval=0.1)
        self.init_ui()
        self.connect_signals()
        self.setup_shortcuts()
        
    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 创建分组框
        group_box = QGroupBox("🖱️ 鼠标连点器 - subLD")
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        group_layout = QVBoxLayout()
        group_layout.setSpacing(15)
        
        # === 状态显示区域 ===
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.StyledPanel)
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        status_layout = QVBoxLayout()
        
        # 状态标签
        self.status_label = QLabel("● 状态: 未启动")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_font = QFont()
        status_font.setBold(True)
        status_font.setPointSize(12)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("color: #95a5a6;")
        status_layout.addWidget(self.status_label)
        
        # 设备状态标签
        self.device_status_label = QLabel("🔌 幽灵键鼠: 未连接")
        self.device_status_label.setAlignment(Qt.AlignCenter)
        self.device_status_label.setStyleSheet("color: #7f8c8d; font-size: 10px;")
        status_layout.addWidget(self.device_status_label)
        
        # 点击计数器
        counter_layout = QHBoxLayout()
        counter_label = QLabel("点击次数:")
        counter_label.setStyleSheet("color: #34495e; font-weight: bold;")
        counter_layout.addWidget(counter_label)
        
        self.click_counter = QLCDNumber()
        self.click_counter.setDigitCount(6)
        self.click_counter.setSegmentStyle(QLCDNumber.Flat)
        self.click_counter.setStyleSheet("""
            QLCDNumber {
                background-color: #2c3e50;
                color: #2ecc71;
                border: 2px solid #34495e;
                border-radius: 3px;
            }
        """)
        self.click_counter.setFixedHeight(40)
        self.click_counter.display(0)
        counter_layout.addWidget(self.click_counter)
        
        status_layout.addLayout(counter_layout)
        status_frame.setLayout(status_layout)
        group_layout.addWidget(status_frame)
        
        # === 间隔设置 ===
        interval_layout = QHBoxLayout()
        interval_label = QLabel("点击间隔:")
        interval_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        interval_layout.addWidget(interval_label)
        
        self.interval_spin = QDoubleSpinBox()
        self.interval_spin.setRange(0.01, 10.0)
        self.interval_spin.setValue(0.1)
        self.interval_spin.setSingleStep(0.01)
        self.interval_spin.setDecimals(2)
        self.interval_spin.setSuffix(" 秒")
        self.interval_spin.setStyleSheet("""
            QDoubleSpinBox {
                padding: 5px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                font-size: 12px;
            }
            QDoubleSpinBox:focus {
                border: 2px solid #3498db;
            }
        """)
        interval_layout.addWidget(self.interval_spin)
        interval_layout.addStretch()
        group_layout.addLayout(interval_layout)
        
        # === 控制按钮 ===
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.enable_btn = QPushButton("🚀 启用连点 (F9)")
        self.enable_btn.setMinimumHeight(45)
        self.enable_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        button_layout.addWidget(self.enable_btn)
        
        self.disable_btn = QPushButton("🛑 停用连点 (F10)")
        self.disable_btn.setMinimumHeight(45)
        self.disable_btn.setEnabled(False)
        self.disable_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #ec7063;
            }
            QPushButton:pressed {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        button_layout.addWidget(self.disable_btn)
        
        group_layout.addLayout(button_layout)
        
        # === 使用说明 ===
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.StyledPanel)
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #fff3cd;
                border-left: 4px solid #ffc107;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout()
        
        info_title = QLabel("📌 使用说明:")
        info_title.setStyleSheet("color: #856404; font-weight: bold;")
        info_layout.addWidget(info_title)
        
        info_text = QLabel(
            "1. 确保幽灵键鼠硬件已插入USB端口\n"
            "2. 点击【启用连点】连接设备 (快捷键: F9)\n"
            "3. 按住鼠标左键 → 开始连点\n"
            "4. 松开鼠标左键 → 停止连点\n"
            "5. 可随时调整点击间隔\n"
            "6. 点击【停用连点】断开设备 (快捷键: F10)\n"
            "\n⚠️ 注意: 本程序需要以管理员权限运行"
        )
        info_text.setStyleSheet("color: #856404; font-size: 11px; line-height: 1.5;")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        info_frame.setLayout(info_layout)
        group_layout.addWidget(info_frame)
        
        group_box.setLayout(group_layout)
        main_layout.addWidget(group_box)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def setup_shortcuts(self):
        """设置快捷键"""
        # F9: 启用连点
        shortcut_enable = QShortcut(QKeySequence("F9"), self)
        shortcut_enable.activated.connect(self.on_enable_clicked)
        
        # F10: 停用连点
        shortcut_disable = QShortcut(QKeySequence("F10"), self)
        shortcut_disable.activated.connect(self.on_disable_clicked)
    
    def connect_signals(self):
        """连接信号和槽"""
        self.enable_btn.clicked.connect(self.on_enable_clicked)
        self.disable_btn.clicked.connect(self.on_disable_clicked)
        self.interval_spin.valueChanged.connect(self.on_interval_changed)
        self.clicker.status_changed.connect(self.on_status_changed)
        self.clicker.click_count_changed.connect(self.on_click_count_changed)
        self.clicker.error_occurred.connect(self.on_error_occurred)
    
    @Slot()
    def on_enable_clicked(self):
        """启用连点按钮点击"""
        if self.clicker.enable():
            self.enable_btn.setEnabled(False)
            self.disable_btn.setEnabled(True)
            self.status_label.setText("● 状态: 就绪 (按住左键连点)")
            self.status_label.setStyleSheet("color: #f39c12; font-weight: bold;")
            self.device_status_label.setText("🔌 幽灵键鼠: 已连接")
            self.device_status_label.setStyleSheet("color: #27ae60; font-size: 10px;")
            
            # 启动监听（这里需要实现鼠标按下/松开的监听）
            self._start_mouse_listener()
    
    @Slot()
    def on_disable_clicked(self):
        """停用连点按钮点击"""
        self.clicker.disable()
        self.enable_btn.setEnabled(True)
        self.disable_btn.setEnabled(False)
        self.status_label.setText("● 状态: 已停止")
        self.status_label.setStyleSheet("color: #95a5a6; font-weight: bold;")
        self.device_status_label.setText("🔌 幽灵键鼠: 未连接")
        self.device_status_label.setStyleSheet("color: #7f8c8d; font-size: 10px;")
        self.click_counter.display(0)
        
        # 停止监听
        self._stop_mouse_listener()
    
    @Slot(float)
    def on_interval_changed(self, value):
        """间隔改变"""
        self.clicker.set_interval(value)
    
    @Slot(bool)
    def on_status_changed(self, is_clicking):
        """连点状态改变"""
        if is_clicking:
            self.status_label.setText("● 状态: 连点中...")
            self.status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            if self.disable_btn.isEnabled():
                self.status_label.setText("● 状态: 就绪 (按住左键连点)")
                self.status_label.setStyleSheet("color: #f39c12; font-weight: bold;")
    
    @Slot(int)
    def on_click_count_changed(self, count):
        """点击次数改变"""
        self.click_counter.display(count)
    
    @Slot(str)
    def on_error_occurred(self, error_msg):
        """错误处理"""
        QMessageBox.warning(self, "subLD - 错误", error_msg)
    
    def _start_mouse_listener(self):
        """启动鼠标监听（使用Windows Hook或轮询方式）"""
        # 这里可以使用 pynput 监听或 Windows Hook
        # 为了简单起见，可以让用户通过UI按钮来控制
        from pynput import mouse
        
        def on_click(x, y, button, pressed):
            if button == mouse.Button.left:
                if pressed:
                    self.clicker.start_clicking()
                else:
                    self.clicker.stop_clicking()
        
        self.listener = mouse.Listener(on_click=on_click)
        self.listener.start()
    
        def _stop_mouse_listener(self):
        """停止鼠标监听"""
        if hasattr(self, 'listener') and self.listener:
            self.listener.stop()
            self.listener = None
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        self._stop_mouse_listener()
        self.clicker.disable()
        event.accept()


# 测试代码
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MouseClickerWidget()
    window.setWindowTitle("subLD - 鼠标连点器")
    window.resize(450, 600)
    window.show()
    
    sys.exit(app.exec())
