#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenWrt Manager - UI Components (v0.app Exact Replica)
精确复刻 v0.app 的按钮、标签等组件样式
"""

from PyQt6.QtWidgets import QPushButton, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from design_system import Colors, Typography, Spacing, BorderRadius

class ApplePrimaryButton(QPushButton):
    """主按钮 - 蓝色填充 (#0071E3)"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(Spacing.BUTTON_HEIGHT)
        self.setMinimumWidth(100)
        self.update_style()
        
    def update_style(self):
        c = Colors.Light
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {c.BUTTON_PRIMARY.name()};
                color: white;
                border: none;
                border-radius: {BorderRadius.MEDIUM}px;
                font-family: {Typography.FONT_FAMILY_SANS};
                font-size: 13px;
                font-weight: 500;
                padding: 0px 16px;
            }}
            QPushButton:hover {{
                background-color: {c.BUTTON_PRIMARY_HOVER.name()};
            }}
            QPushButton:pressed {{
                background-color: {c.BUTTON_SELECTED.name()};
            }}
            QPushButton:disabled {{
                background-color: {c.BUTTON_PRIMARY_DISABLED.name()};
                color: white;
            }}
        """)

class AppleSecondaryButton(QPushButton):
    """次要按钮 - 白色边框"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(Spacing.BUTTON_HEIGHT)
        self.setMinimumWidth(80)
        self.update_style()
        
    def update_style(self):
        c = Colors.Light
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {c.BUTTON_SECONDARY_BG.name()};
                color: {c.TEXT_PRIMARY.name()};
                border: 1px solid {c.BORDER_PRIMARY.name()};
                border-radius: {BorderRadius.MEDIUM}px;
                font-family: {Typography.FONT_FAMILY_SANS};
                font-size: 13px;
                padding: 0px 12px;
            }}
            QPushButton:hover {{
                background-color: {c.BUTTON_SECONDARY_HOVER.name()};
            }}
            QPushButton:pressed {{
                background-color: {c.BG_HOVER.name()};
            }}
        """)

class AppleSmallButton(QPushButton):
    """小按钮 - 28px高度，用于工具栏"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(Spacing.BUTTON_HEIGHT_SM)
        self.setMinimumWidth(60)
        self.update_style()
        
    def update_style(self):
        c = Colors.Light
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {c.BUTTON_SECONDARY_BG.name()};
                color: {c.TEXT_PRIMARY.name()};
                border: 1px solid {c.BORDER_PRIMARY.name()};
                border-radius: {BorderRadius.SMALL}px;
                font-family: {Typography.FONT_FAMILY_SANS};
                font-size: 12px;
                padding: 0px 10px;
            }}
            QPushButton:hover {{
                background-color: {c.BG_HOVER.name()};
            }}
        """)

class SectionHeader(QWidget):
    """章节标题 - 大写粗体小标签"""
    def __init__(self, title="", subtitle="", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, Spacing.PADDING_SM)
        layout.setSpacing(2)
        
        # 主标题 - 11px 粗体大写
        c = Colors.Light
        title_label = QLabel(title.upper())
        title_label.setStyleSheet(f"""
            color: {c.TEXT_SECONDARY.name()};
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.5px;
        """)
        layout.addWidget(title_label)
        
        # 副标题（如果有）
        if subtitle:
            sub_label = QLabel(subtitle)
            sub_label.setStyleSheet(f"""
                color: {c.TEXT_SECONDARY.name()};
                font-size: 11px;
            """)
            layout.addWidget(sub_label)

class StatusLabel(QLabel):
    """状态标签 - 带图标和颜色"""
    def __init__(self, text="", status="success", parent=None):
        super().__init__(text, parent)
        self.set_status(status)
    
    def set_status(self, status: str):
        c = Colors.Light
        color_map = {
            "success": c.STATUS_SUCCESS.name(),
            "error": c.STATUS_ERROR.name(),
            "pending": c.STATUS_PENDING.name(),
        }
        color = color_map.get(status, c.TEXT_PRIMARY.name())
        
        self.setStyleSheet(f"""
            color: {color};
            font-size: 13px;
        """)

class TrafficLightButton(QWidget):
    """macOS 红绿灯按钮组"""
    closeClicked = pyqtSignal()
    minimizeClicked = pyqtSignal()
    maximizeClicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(Spacing.TRAFFIC_BUTTON_SIZE)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Spacing.GAP_SM)
        
        c = Colors.Light
        
        # 红色按钮
        self.red_btn = QPushButton(self)
        self.red_btn.setFixedSize(Spacing.TRAFFIC_BUTTON_SIZE, Spacing.TRAFFIC_BUTTON_SIZE)
        self.red_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c.TRAFFIC_RED.name()};
                border: 1px solid {c.TRAFFIC_RED_BORDER.name()};
                border-radius: {Spacing.TRAFFIC_BUTTON_SIZE // 2}px;
            }}
            QPushButton:hover {{
                filter: brightness(0.9);
            }}
        """)
        self.red_btn.clicked.connect(self.closeClicked.emit)
        
        # 黄色按钮
        self.yellow_btn = QPushButton(self)
        self.yellow_btn.setFixedSize(Spacing.TRAFFIC_BUTTON_SIZE, Spacing.TRAFFIC_BUTTON_SIZE)
        self.yellow_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c.TRAFFIC_YELLOW.name()};
                border: 1px solid {c.TRAFFIC_YELLOW_BORDER.name()};
                border-radius: {Spacing.TRAFFIC_BUTTON_SIZE // 2}px;
            }}
            QPushButton:hover {{
                filter: brightness(0.9);
            }}
        """)
        self.yellow_btn.clicked.connect(self.minimizeClicked.emit)
        
        # 绿色按钮
        self.green_btn = QPushButton(self)
        self.green_btn.setFixedSize(Spacing.TRAFFIC_BUTTON_SIZE, Spacing.TRAFFIC_BUTTON_SIZE)
        self.green_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c.TRAFFIC_GREEN.name()};
                border: 1px solid {c.TRAFFIC_GREEN_BORDER.name()};
                border-radius: {Spacing.TRAFFIC_BUTTON_SIZE // 2}px;
            }}
            QPushButton:hover {{
                filter: brightness(0.9);
            }}
        """)
        self.green_btn.clicked.connect(self.maximizeClicked.emit)

# ============ 占位符类（保持兼容性）============
# 这些是原代码可能会调用的，但当前UI不需要
class AppleDestructiveButton(AppleSecondaryButton):
    """删除按钮 - 现在使用次要按钮样式"""
    pass

class StatusBadge(StatusLabel):
    """状态徽章 - 使用状态标签"""
    pass

class AppleCard(QWidget):
    """卡片容器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            background-color: white;
            border: 1px solid {Colors.Light.BORDER_PRIMARY.name()};
            border-radius: {BorderRadius.MEDIUM}px;
        """)

class StatsCard(AppleCard):
    """统计卡片"""
    pass

class CircularProgress(QWidget):
    """圆形进度条占位"""
    pass
