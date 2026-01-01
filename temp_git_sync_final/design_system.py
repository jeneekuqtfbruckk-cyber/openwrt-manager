#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenWrt Manager - Design System (v0.app Exact Replica)
基于 v0.app 生成的设计稿，精确复刻 macOS 风格
"""

from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

class Colors:
    """v0.app 精确配色系统 - 100% 还原"""
    class Light:
        # === 背景色系 ===
        BG_PRIMARY = QColor("#FFFFFF")         # 纯白主内容区
        BG_SECONDARY = QColor("#F5F5F7")       # 侧边栏背景（Mac标准灰）
        BG_TITLEBAR_TOP = QColor("#E8E8E8")    # 标题栏渐变起点
        BG_TITLEBAR_BOTTOM = QColor("#D4D4D4")  # 标题栏渐变终点
        BG_MENUBAR_TOP = QColor("#F5F5F5")     # 菜单栏渐变起点
        BG_MENUBAR_BOTTOM = QColor("#E8E8E8")   # 菜单栏渐变终点
        BG_TABLEHEAD = QColor("#FAFAFA")       # 表头背景
        BG_HOVER = QColor("#F5F5F7")           # 悬停背景
        BG_INPUT = QColor("#FFFFFF")           # 输入框背景
        
        # === 文字色系 ===
        TEXT_PRIMARY = QColor("#1D1D1F")       # 主文字（接近黑）
        TEXT_SECONDARY = QColor("#8E8E8E")     # 副文字（中灰）
        TEXT_TITLE = QColor("#4D4D4D")         # 标题栏文字
        TEXT_VERSION = QColor("#8E8E8E")       # 版本号文字
        TEXT_PLACEHOLDER = QColor("#8E8E8E")   # 占位符文字
        
        # === 边框色系 ===
        BORDER_PRIMARY = QColor("#C7C7C7")     # 主边框
        BORDER_SECONDARY = QColor("#D1D1D6")   # 次边框（更浅）
        BORDER_SEPARATOR = QColor("#E5E5E5")   # 表格分隔线
        BORDER_MENUBAR = QColor("#B8B8B8")     # 菜单栏边框
        BORDER_FOCUS = QColor("#0071E3")       # 输入框焦点边框
        
        # === 按钮色系 ===
        BUTTON_PRIMARY = QColor("#0071E3")      # 主按钮背景（Apple蓝）
        BUTTON_PRIMARY_HOVER = QColor("#0077ED") # 主按钮悬停
        BUTTON_PRIMARY_DISABLED = QColor("#8E8E8E") # 禁用按钮
        BUTTON_SELECTED = QColor("#0061D5")     # 菜单选中高亮
        BUTTON_SECONDARY_BG = QColor("#FFFFFF")  # 次按钮背景
        BUTTON_SECONDARY_HOVER = QColor("#FAFAFA") # 次按钮悬停
        
        # === 状态色系 ===
        STATUS_SUCCESS = QColor("#34C759")      # 成功绿
        STATUS_ERROR = QColor("#FF3B30")        # 失败红
        STATUS_PENDING = QColor("#FF9500")      # 等待橙
        
        # === 红绿灯按钮 (macOS窗口控制) ===
        TRAFFIC_RED = QColor("#FF5F57")
        TRAFFIC_RED_BORDER = QColor("#E0443E")
        TRAFFIC_YELLOW = QColor("#FEBC2E")
        TRAFFIC_YELLOW_BORDER = QColor("#D4A528")
        TRAFFIC_GREEN = QColor("#28C840")
        TRAFFIC_GREEN_BORDER = QColor("#24A732")

class Typography:
    """字体系统 - 匹配 v0.app"""
    # 字体配置 - 优先使用 Apple 字体，降级到 Windows 原生
    FONT_FAMILY_SANS = '"SF Pro Text", "SF Pro Display", "Helvetica Neue", "Segoe UI", "Microsoft YaHei UI", sans-serif'
    FONT_FAMILY_MONO = '"SF Mono", "Menlo", "Consolas", "Courier New", monospace'
    
    # 字号定义（精确匹配v0.app）
    SIZE_11 = 11  # 小标签
    SIZE_12 = 12  # 小按钮
    SIZE_13 = 13  # 正文/按钮/表格
    SIZE_15 = 15  # 大标题
    
    @staticmethod
    def label_small() -> QFont:
        """小标签 (11px, 粗体, 大写)"""
        font = QFont("Segoe UI", 11)
        font.setWeight(QFont.Weight.Bold)
        return font
    
    @staticmethod
    def button() -> QFont:
        """按钮 (13px, 中等)"""
        font = QFont("Segoe UI", 13)
        font.setWeight(QFont.Weight.Medium)
        return font
        
    @staticmethod
    def body() -> QFont:
        """正文 (13px)"""
        font = QFont("Segoe UI", 13)
        return font
    
    @staticmethod
    def mono() -> QFont:
        """等宽字体 (13px) - 用于IP/密码"""
        font = QFont("Consolas", 13)
        return font
        
    @staticmethod
    def title() -> QFont:
        """窗口标题 (13px, 中等)"""
        font = QFont("Segoe UI", 13)
        font.setWeight(QFont.Weight.Medium)
        return font

class Spacing:
    """间距系统 - v0.app 精确值"""
    # 容器内边距
    PADDING_SM = 8   # py-2
    PADDING_MD = 12  # px-3
    PADDING_LG = 16  # p-4
    
    # 元素间隙
    GAP_XS = 4   # gap-1
    GAP_SM = 8   # gap-2
    GAP_MD = 12  # gap-3
    GAP_LG = 16  # gap-4
    
    # 固定尺寸
    SIDEBAR_WIDTH = 280       # 侧边栏宽度
    TITLEBAR_HEIGHT = 52      # 标题栏高度
    MENUBAR_HEIGHT = 28       # 菜单栏高度
    TOOLBAR_HEIGHT = 40       # 工具栏高度
    BUTTON_HEIGHT = 40        # 主按钮高度
    BUTTON_HEIGHT_SM = 28     # 小按钮高度
    TRAFFIC_BUTTON_SIZE = 12  # 红绿灯按钮直径
    
    # === 向后兼容：传统命名 ===
    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32
    XXL = 48

class BorderRadius:
    """圆角系统 - v0.app 精确值"""
    SMALL = 5    # rounded-[5px]
    MEDIUM = 6   # rounded-[6px]
    LARGE = 10   # rounded-[10px]
    FULL = 9999  # rounded-full

class ThemeManager:
    """主题管理器"""
    @property
    def colors(self):
        return Colors.Light

    def get_stylesheet(self) -> str:
        """生成全局样式表 - 100%匹配v0.app"""
        c = Colors.Light
        return f"""
            /* ============ 全局设置 ============ */
            QMainWindow {{
                background-color: {c.BG_SECONDARY.name()};
            }}
            
            QWidget {{
                font-family: {Typography.FONT_FAMILY_SANS};
                font-size: 13px;
                color: {c.TEXT_PRIMARY.name()};
            }}
            
            /* ============ 输入框 ============ */
            QPlainTextEdit, QTextEdit, QSpinBox {{
                background-color: {c.BG_INPUT.name()};
                border: 1px solid {c.BORDER_PRIMARY.name()};
                border-radius: {BorderRadius.MEDIUM}px;
                padding: {Spacing.PADDING_SM}px {Spacing.PADDING_MD}px;
                font-size: 13px;
                color: {c.TEXT_PRIMARY.name()};
                selection-background-color: {c.BUTTON_PRIMARY.name()};
                selection-color: white;
            }}
            
            QPlainTextEdit:focus, QTextEdit:focus, QSpinBox:focus {{
                border: 1px solid {c.BORDER_FOCUS.name()};
                outline: 2px solid {c.BORDER_FOCUS.name()}33; /* 20% 透明度 */
            }}
            
            QPlainTextEdit::placeholder {{
                color: {c.TEXT_PLACEHOLDER.name()};
            }}
            
            /* ============ 表格 (Finder风格) ============ */
            QTableWidget {{
                background-color: {c.BG_PRIMARY.name()};
                border: none;
                gridline-color: {c.BORDER_SEPARATOR.name()};
                selection-background-color: {c.BG_HOVER.name()};
                selection-color: {c.TEXT_PRIMARY.name()};
                outline: none;
            }}
            
            QHeaderView {{
                background-color: {c.BG_TABLEHEAD.name()};
                border: none;
                border-bottom: 1px solid {c.BORDER_SECONDARY.name()};
            }}
            
            QHeaderView::section {{
                background-color: {c.BG_TABLEHEAD.name()};
                border: none;
                border-right: none;
                color: {c.TEXT_SECONDARY.name()};
                font-weight: 600;
                font-size: 11px;
                padding: 8px 16px;
                text-transform: uppercase;
            }}
            
            QTableWidget::item {{
                padding: 10px 16px;
                border-bottom: 1px solid {c.BORDER_SEPARATOR.name()};
            }}
            
            QTableWidget::item:hover {{
                background-color: {c.BG_HOVER.name()};
            }}
            
            /* ============ 分割线 ============ */
            QFrame[frameShape="4"], QFrame[frameShape="5"] {{
                border: none;
                background-color: {c.BORDER_SECONDARY.name()};
            }}
        """

theme = ThemeManager()
