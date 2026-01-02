#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS风格窗口组件
包含标题栏、菜单栏等macOS特有元素
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QMenu)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QLinearGradient, QPalette, QPainter, QColor
from design_system import Colors, Spacing, Typography

class MacTitleBar(QWidget):
    """macOS标题栏 - 带渐变和红绿灯按钮"""
    closeClicked = pyqtSignal()
    minimizeClicked = pyqtSignal()
    maximizeClicked = pyqtSignal()
    
    def __init__(self, title="", version="", parent=None):
        super().__init__(parent)
        self.setFixedHeight(Spacing.TITLEBAR_HEIGHT)
        self.setup_ui(title, version)
        
    def setup_ui(self, title, version):
        c = Colors.Light
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(0)
        
        # 红绿灯按钮组
        traffic_lights = QWidget()
        traffic_layout = QHBoxLayout(traffic_lights)
        traffic_layout.setContentsMargins(0, 0, 0, 0)
        traffic_layout.setSpacing(8)
        
        # 红色按钮
        red_btn = QPushButton()
        red_btn.setFixedSize(12, 12)
        red_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c.TRAFFIC_RED.name()};
                border: 1px solid {c.TRAFFIC_RED_BORDER.name()};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                filter: brightness(0.9);
            }}
        """)
        red_btn.clicked.connect(self.closeClicked.emit)
        traffic_layout.addWidget(red_btn)
        
        # 黄色按钮
        yellow_btn = QPushButton()
        yellow_btn.setFixedSize(12, 12)
        yellow_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c.TRAFFIC_YELLOW.name()};
                border: 1px solid {c.TRAFFIC_YELLOW_BORDER.name()};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                filter: brightness(0.9);
            }}
        """)
        yellow_btn.clicked.connect(self.minimizeClicked.emit)
        traffic_layout.addWidget(yellow_btn)
        
        # 绿色按钮
        green_btn = QPushButton()
        green_btn.setFixedSize(12, 12)
        green_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c.TRAFFIC_GREEN.name()};
                border: 1px solid {c.TRAFFIC_GREEN_BORDER.name()};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                filter: brightness(0.9);
            }}
        """)
        green_btn.clicked.connect(self.maximizeClicked.emit)
        traffic_layout.addWidget(green_btn)
        
        layout.addWidget(traffic_lights)
        layout.addStretch()
        
        # 标题（居中）
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color: {c.TEXT_TITLE.name()};
            font-size: 13px;
            font-weight: 500;
            background-color: transparent;
        """)
        title_layout.addWidget(title_label)
        
        version_label = QLabel(version)
        version_label.setStyleSheet(f"""
            color: {c.TEXT_VERSION.name()};
            font-size: 11px;
            background-color: transparent;
        """)
        title_layout.addWidget(version_label)
        
        layout.addWidget(title_container)
        layout.addStretch()
        
    def paintEvent(self, event):
        """绘制渐变背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, Colors.Light.BG_TITLEBAR_TOP)
        gradient.setColorAt(1, Colors.Light.BG_TITLEBAR_BOTTOM)
        
        painter.fillRect(self.rect(), gradient)
        
        # 底部边框
        painter.setPen(Colors.Light.BORDER_MENUBAR)
        painter.drawLine(0, self.height()-1, self.width(), self.height()-1)

class MacMenuBar(QWidget):
    """macOS菜单栏"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(Spacing.MENUBAR_HEIGHT)
        self.setup_ui()
        
    def setup_ui(self):
        c = Colors.Light
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(0)
        
        # 占位符将菜单推到右侧
        layout.addStretch()
        
        # 菜单项
        menu_items = [
            ("OpenWrt Manager", True),  # (名称, 是否粗体)
            ("文件", False),
            ("编辑", False),
            ("视图", False),
            ("扫描", False),
            ("窗口", False),
            ("帮助", False),
        ]
        
        for menu_name, is_bold in menu_items:
            btn = QPushButton(menu_name)
            # 添加菜单 (即使是空的，为了视觉效果)
            menu = QMenu(self)
            if menu_name == "文件":
                 menu.addAction("新建")
                 menu.addAction("打开...")
                 menu.addSeparator()
                 menu.addAction("导出")
            elif menu_name == "编辑":
                 menu.addAction("撤销")
                 menu.addAction("重做")
                 menu.addSeparator()
                 menu.addAction("剪切")
                 menu.addAction("复制")
                 menu.addAction("粘贴")
            else:
                 menu.addAction("示例选项 1")
                 menu.addAction("示例选项 2")
            
            btn.setMenu(menu)
            
            if is_bold:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        color: {c.TEXT_PRIMARY.name()};
                        border: none;
                        border-radius: 4px;
                        padding: 2px 10px;
                        font-family: {Typography.FONT_FAMILY_SANS};
                        font-size: 13px;
                        font-weight: 600;
                    }}
                    QPushButton:hover {{
                        background-color: rgba(0,0,0,0.05);
                    }}
                    QPushButton::menu-indicator {{ width: 0px; }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        color: {c.TEXT_PRIMARY.name()};
                        border: none;
                        border-radius: 4px;
                        padding: 2px 10px;
                        font-family: {Typography.FONT_FAMILY_SANS};
                        font-size: 13px;
                    }}
                    QPushButton:hover {{
                        background-color: rgba(0,0,0,0.05);
                    }}
                    QPushButton::menu-indicator {{ width: 0px; }}
                """)
            layout.addWidget(btn)
        
        # 移除时间显示
        # time_label = QLabel("15:00")
        
    def paintEvent(self, event):
        """绘制渐变背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, Colors.Light.BG_MENUBAR_TOP)
        gradient.setColorAt(1, Colors.Light.BG_MENUBAR_BOTTOM)
        
        painter.fillRect(self.rect(), gradient)
        
        # 底部边框
        painter.setPen(Colors.Light.BORDER_PRIMARY)
        painter.drawLine(0, self.height()-1, self.width(), self.height()-1)

class MacWindow(QWidget):
    """macOS风格的窗口容器 - 带圆角边框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            MacWindow {{
                background-color: {Colors.Light.BG_SECONDARY.name()};
                border: 1px solid {Colors.Light.BORDER_PRIMARY.name()};
                border-radius: 10px;
            }}
        """)
