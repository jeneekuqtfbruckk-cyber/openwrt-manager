
import flet as ft
import asyncio
import csv
import json
from datetime import datetime
from flet_login_manager import FletLoginManager

# Apple Design System Constants
class MacColors:
    SIDEBAR_BG = "#F5F5F7"  # Light gray sidebar
    SIDEBAR_BORDER = "#D1D1D6"
    CONTENT_BG = "#FFFFFF"
    TEXT_PRIMARY = "#1D1D1F"
    TEXT_SECONDARY = "#86868B"
    ACCENT_BLUE = "#007AFF"
    SUCCESS_GREEN = "#34C759"
    WARNING_ORANGE = "#FF9500"
    ERROR_RED = "#FF3B30"
    DIVIDER = "#E5E5EA"
    WINDOW_BG = "#00000000" # Transparent

def main(page: ft.Page):
    # Window Configuration
    page.title = "OpenWrt Manager"
    page.window_width = 1200
    page.window_height = 800
    page.window_resizable = True
    page.window_title_bar_hidden = True  # Hide system titlebar
    page.window_frameless = True  # Frameless window (macOS style)
    page.padding = 0
    page.spacing = 0
    
    # Global Font Theme (Critical: Remove default Roboto)
    page.theme = ft.Theme(
        font_family="SF Pro Display",  # macOS default
    )
    # Fallback fonts for Windows/Linux
    page.fonts = {
        "SF Pro Display": "https://fonts.cdnfonts.com/s/16550/SFProDisplay-Regular.woff", 
        "PingFang SC": "simhei", # Fallback for Windows
    }
    
    print("Flet App Started! Initializing UI...") # Debug log

    # Custom Title Bar (simulating macOS traffic lights)
    def window_drag_area(e):

        page.window_drag_area()

    title_bar = ft.Container(
        content=ft.WindowDragArea(
            content=ft.Row(
                controls=[
                    # Mac Traffic Lights (Left aligned)
                    ft.Row(
                        [
                            ft.Container(
                                width=12, height=12, 
                                border_radius=6, 
                                bgcolor="#FF5F57", # Red
                                on_click=lambda _: page.window_close()
                            ),
                            ft.Container(
                                width=12, height=12, 
                                border_radius=6, 
                                bgcolor="#FEBC2E", # Yellow
                                on_click=lambda _: page.window_minimized()
                            ),
                            ft.Container(
                                width=12, height=12, 
                                border_radius=6, 
                                bgcolor="#28C840", # Green
                                on_click=lambda _: page.window_maximized() # Should maximize/restore
                            ),
                        ],
                        spacing=8,
                    ),
                    
                    # Title (Centered)
                    ft.Row(
                        [
                            ft.Text("OpenWrt Manager", size=13, weight=ft.FontWeight.W_500, color="#4d4d4d"),
                            ft.Text("v2.0", size=11, color="#8e8e8e"),
                        ],
                        spacing=6,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),

                    # Spacer for balance (approximate width of traffic lights + padding)
                    ft.Container(width=52), 
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ),
        height=52,
        # Gradient background to match Web v0.app
        gradient=ft.LinearGradient(
            begin=ft.Alignment(0, -1),
            end=ft.Alignment(0, 1),
            colors=["#E8E8E8", "#D4D4D4"],
        ),
        padding=ft.Padding(left=16, right=16, top=0, bottom=0),
        border=ft.Border(bottom=ft.BorderSide(1, "#B8B8B8")), # Darker border to match Web
    )

    # === Export Functions ===
    def export_csv():
        """Export table data to CSV"""
        if not data_table.rows:
            return
        filename = f"openwrt_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["#", "地址", "状态", "用户名", "密码", "详情"])
            for row in data_table.rows:
                writer.writerow([cell.content.value for cell in row.cells])
        page.snack_bar = ft.SnackBar(ft.Text(f"已导出到 {filename}"))
        page.snack_bar.open = True
        page.update()
    
    def export_json():
        """Export table data to JSON"""
        if not data_table.rows:
            return
        data = []
        for row in data_table.rows:
            data.append({
                "序号": row.cells[0].content.value,
                "地址": row.cells[1].content.value,
                "状态": row.cells[2].content.value,
                "用户名": row.cells[3].content.value,
                "密码": row.cells[4].content.value,
                "详情": row.cells[5].content.value,
            })
        filename = f"openwrt_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        page.snack_bar = ft.SnackBar(ft.Text(f"已导出到 {filename}"))
        page.snack_bar.open = True
        page.update()
    
    def export_excel():
        """Export table data to Excel (requires openpyxl)"""
        page.snack_bar = ft.SnackBar(ft.Text("Excel导出需要安装 openpyxl 库"))
        page.snack_bar.open = True
        page.update()
    
    def export_markdown():
        """Export table data to Markdown"""
        if not data_table.rows:
            return
        filename = f"openwrt_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# OpenWrt Manager 扫描结果\n\n")
            f.write("| # | 地址 | 状态 | 用户名 | 密码 | 详情 |\n")
            f.write("|---|------|------|--------|------|------|\n")
            for row in data_table.rows:
                cells = [cell.content.value for cell in row.cells]
                f.write(f"| {' | '.join(str(c) for c in cells)} |\n")
        page.snack_bar = ft.SnackBar(ft.Text(f"已导出到 {filename}"))
        page.snack_bar.open = True
        page.update()
    
    # === MenuBar (28px height, matching PyQt MacMenuBar) ===
    def create_menu_item(label, is_bold=False, items=None, on_click_handlers=None):
        """Create a menu item with optional dropdown"""
        if items is None:
            # Simple text label (e.g., "OpenWrt Manager")
            return ft.Text(
                label,
                size=13,
                color="#1d1d1f",
                weight=ft.FontWeight.W_500 if is_bold else ft.FontWeight.NORMAL,
            )
        else:
            # PopupMenuButton with dropdown
            menu_items = []
            for i, item in enumerate(items):
                if item == "---":
                    menu_items.append(ft.Divider(height=1))
                else:
                    handler = on_click_handlers[i] if on_click_handlers and i < len(on_click_handlers) else None
                    menu_items.append(
                        ft.PopupMenuItem(
                            content=ft.Text(item, size=13),
                            on_click=handler
                        )
                    )
            return ft.PopupMenuButton(
                content=ft.Text(label, size=13, color="#1d1d1f"),
                items=menu_items,
            )
    
    menubar = ft.Container(
        height=28,
        bgcolor="#f0f0f0",  # Menubar background
        border=ft.Border(bottom=ft.BorderSide(1, "#d1d1d6")),
        padding=ft.Padding(left=12, right=12, top=0, bottom=0),
        content=ft.Row([
            create_menu_item("OpenWrt Manager", is_bold=True),
            create_menu_item("文件", items=["新建", "打开...", "---", "导出"], 
                           on_click_handlers=[None, None, None, lambda e: export_csv()]),
            create_menu_item("编辑", items=["撤销", "重做", "---", "剪切", "复制", "粘贴"]),
            create_menu_item("视图", items=["示例选项 1", "示例选项 2"]),
            create_menu_item("扫描", items=["示例选项 1", "示例选项 2"]),
            create_menu_item("窗口", items=["示例选项 1", "示例选项 2"]),
            create_menu_item("帮助", items=["示例选项 1", "示例选项 2"]),
        ], spacing=10)
    )

    # Sidebar Component
    def sidebar_item(icon_text, label, selected=False):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        icon_text,  # Using text/emoji instead of icons
                        size=18, 
                        color=MacColors.ACCENT_BLUE if selected else MacColors.TEXT_PRIMARY
                    ),
                    ft.Text(
                        label, 
                        size=13, 
                        weight=ft.FontWeight.W_500 if selected else ft.FontWeight.NORMAL,
                        color=MacColors.ACCENT_BLUE if selected else MacColors.TEXT_PRIMARY
                    )
                ],
                spacing=10
            ),
            padding=ft.Padding(left=12, right=12, top=8, bottom=8),
            border_radius=6,
            bgcolor=ft.Colors.with_opacity(0.1, MacColors.ACCENT_BLUE) if selected else None,
            on_hover=lambda e: e.control.update()
        )

    # URL Input Field (Custom Web-style Container)
    # Removing Material TextField borders by wrapping in Container to match v0.app Textarea
    url_input_field = ft.TextField(
        multiline=True,
        hint_text="输入 IP 地址，每行一个...",
        hint_style=ft.TextStyle(color="#8E8E8E", size=13), # Match Colors.Light.TEXT_PLACEHOLDER
        border=ft.InputBorder.NONE,  # Remove internal border
        min_lines=6,
        max_lines=10,
        text_size=13,
        content_padding=ft.Padding(12, 8, 12, 8), # Match design_system.py: 8px V, 12px H
        cursor_color=MacColors.ACCENT_BLUE,
    )
    
    url_input_container = ft.Container(
        content=url_input_field,
        height=200, # Match Web: min-h-[200px]
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#C7C7C7"),
        border_radius=6,
        padding=0,
    )
    
    # Event handler for input change (to toggle button color)
    def on_url_change(e):
        nonlocal is_running
        if is_running: return
        has_text = len(e.control.value.strip()) > 0
        # Visual State Logic: Grey (Disabled) <-> Blue (Active)
        start_button.bgcolor = MacColors.ACCENT_BLUE if has_text else "#E5E5EA"
        start_button.color = ft.Colors.WHITE if has_text else "#8E8E93"
        start_button.update()
    
    url_input_field.on_change = on_url_change
    
    # Concurrent Dropdown (40px height to match h-10)
    concurrent_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("50"),
            ft.dropdown.Option("100"),
            ft.dropdown.Option("200"),
        ],
        value="50",
        width=80,
        height=40, # Match Web: h-10 (40px)
        text_size=13,
        content_padding=10,
        # alignment removed - unsupported in Dropdown
        border_color="#C7C7C7", # Match border-[#c7c7c7]
        border_radius=6,
    )
    
    start_button = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, size=16, color="#ffffff"),
                ft.Text("开始探测", size=13, weight=ft.FontWeight.W_500, color="#ffffff"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4,
        ),
        bgcolor="#E5E5EA", # Default disabled color
        border_radius=6,
        padding=ft.Padding(16, 0, 16, 0),
        height=40, # Match Web: h-10 (40px)
        on_click=None, # Initially disabled
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
    )

    # Empty State - UPDATED to match Web v0.app (Pulse Icon + "暂无结果")
    empty_state = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.MONITOR_HEART_OUTLINED, size=40, color="#C7C7C7"), # Match Web: w-10 h-10 (40px)
                ft.Container(height=12),
                ft.Text("暂无结果", size=15, weight=ft.FontWeight.W_500, color="#1D1D1F"), # Match Web: text-[15px]
                ft.Text("输入目标地址并点击开始探测", size=13, color="#8E8E8E"), # Match Web: text-[13px]
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        ),
        alignment=ft.Alignment(0, 0),
        expand=True,
    )
    
    # Create stat label references for later updates
    stat_success = ft.Text("0", size=13, color="#34c759", weight=ft.FontWeight.W_600)
    stat_failed = ft.Text("0", size=13, color="#ff3b30", weight=ft.FontWeight.W_600)
    stat_waiting = ft.Text("0", size=13, color="#ff9500", weight=ft.FontWeight.W_600)
    
    sidebar = ft.Container(
        width=280,  # Match PyQt: 280px
        bgcolor=MacColors.SIDEBAR_BG,
        border=ft.Border(right=ft.BorderSide(1, MacColors.SIDEBAR_BORDER)),
        padding=ft.Padding(left=16, right=16, top=16, bottom=16),
        content=ft.Column(
            [
                # === 目标 === (changed from "输入")
                ft.Text("目标", size=11, color="#8e8e8e", weight=ft.FontWeight.W_600),
                # Spacing Correction: Web Source uses mb-2 which is 0.5rem = 8px.
                ft.Container(height=8),
                url_input_container, # Use the wrapped container
                ft.Container(height=12),
                ft.Row(
                    [
                        ft.Container(content=concurrent_dropdown, expand=2),
                        ft.Container(width=12),
                        ft.Container(content=start_button, expand=3),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),

                ft.Container(height=24),
                
                # === 概览统计（底部）===
                ft.Container(
                    border=ft.Border(top=ft.BorderSide(1, "#d1d1d6")),
                    padding=ft.Padding(left=0, right=0, top=12, bottom=0),
                    margin=ft.Margin(0, 8, 0, 0),
                    content=ft.Column([
                        ft.Text("概览", size=11, color="#8e8e8e", weight=ft.FontWeight.W_600),
                        ft.Container(height=6),
                        
                        # 成功
                        ft.Row([
                            ft.Text("成功", size=13, color="#1d1d1f"),
                            ft.Container(expand=True),
                            stat_success,
                        ], spacing=0),
                        ft.Container(height=6),  # Changed from 2px to 6px
                        
                        # 失败
                        ft.Row([
                            ft.Text("失败", size=13, color="#1d1d1f"),
                            ft.Container(expand=True),
                            stat_failed,
                        ], spacing=0),
                        ft.Container(height=6),  # Changed from 2px to 6px
                        
                        # 等待中
                        ft.Row([
                            ft.Text("等待中", size=13, color="#1d1d1f"),
                            ft.Container(expand=True),
                            stat_waiting,
                        ], spacing=0),
                    ], spacing=0)
                ),
            ],
            spacing=0  # Use explicit Container heights instead
        )
    )

    # Main Content Area
    
    # Stats Card Component
    def stat_card(title, value, color):
        return ft.Container(
            expand=1,
            padding=16,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(width=0.5, color=MacColors.DIVIDER),  # Fixed deprecated API
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.05, "#000000"),
                offset=ft.Offset(0, 4),
            ),
            content=ft.Column(
                [
                    ft.Text(title, size=12, color=MacColors.TEXT_SECONDARY),
                    ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=color),
                ],
                spacing=4
            )
        )

    # Data Table Component (6列: #, 地址, 状态, 用户名, 密码, 详情)
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("#")),
            ft.DataColumn(ft.Text("地址")),
            ft.DataColumn(ft.Text("状态")),
            ft.DataColumn(ft.Text("用户名")),
            ft.DataColumn(ft.Text("密码")),
            ft.DataColumn(ft.Text("详情")),
        ],
        rows=[],  # Empty initially, will be populated dynamically
        width=float("inf"),
        heading_row_height=40,
        data_row_min_height=48,
        divider_thickness=0.5,
        heading_text_style=ft.TextStyle(size=12, color=MacColors.TEXT_SECONDARY, weight=ft.FontWeight.W_500),
    )

    # ========================================================================
    # LoginManager Integration
    # ========================================================================
    
    # Initialize LoginManager
    login_manager = FletLoginManager(max_concurrent=50)
    is_running = False  # Track detection state
    
    # Status color mapping
    def get_status_color(status: str):
        if "成功" in status:
            return MacColors.SUCCESS_GREEN
        elif "失败" in status or "超时" in status:
            return MacColors.ERROR_RED
        else:
            return MacColors.WARNING_ORANGE
    
    # Callback: Update table row
    def handle_row_update(row: int, status: str, user: str, password: str, notes: str):
        if row < len(data_table.rows):
            # Update existing row (6列: index 0=#, 1=地址, 2=状态, 3=用户名, 4=密码, 5=详情)
            data_table.rows[row].cells[2].content = ft.Container(
                content=ft.Text(status, size=12, color=get_status_color(status)),
                padding=ft.Padding(left=8, right=8, top=4, bottom=4),
                border_radius=12,
                bgcolor=ft.Colors.with_opacity(0.1, get_status_color(status))
            )
            data_table.rows[row].cells[3].content = ft.Text(user, size=13)
            data_table.rows[row].cells[4].content = ft.Text(password, size=13)
            data_table.rows[row].cells[5].content = ft.Text(notes, size=12, color=MacColors.TEXT_SECONDARY)
            
            # Update statistics
            success_count = sum(1 for r in data_table.rows if "成功" in str(r.cells[2].content.content.value))
            failed_count = sum(1 for r in data_table.rows if ("失败" in str(r.cells[2].content.content.value) or "超时" in str(r.cells[2].content.content.value)))
            waiting_count = len(data_table.rows) - success_count - failed_count
            
            stat_success.value = str(success_count)
            stat_failed.value = str(failed_count)
            stat_waiting.value = str(waiting_count)
            
            page.update()
    
    # Callback: Task finished
    def handle_task_finished():
        nonlocal is_running
        is_running = False
        start_button.text = "开始探测"
        start_button.bgcolor = MacColors.ACCENT_BLUE
        url_input_field.disabled = False
        concurrent_dropdown.disabled = False
        page.update()
    
    # Start detection handler
    async def start_detection(e):
        nonlocal is_running
        
        if is_running:
            # Stop detection
            login_manager.stop()
            handle_task_finished()
            return
        
        # Get URLs from input
        urls = url_input_field.value.strip().split('\n') if url_input_field.value else []
        urls = [url.strip() for url in urls if url.strip()]
        
        if not urls:
            # Show error (TODO: add snackbar)
            print("No URLs entered!")
            return
        
        # Update UI state
        is_running = True
        start_button.text = "停止探测"
        start_button.bgcolor = MacColors.ERROR_RED
        url_input_field.disabled = True
        concurrent_dropdown.disabled = True
        
        # Show table, hide empty state
        empty_state.visible = False
        table_container.visible = True
        
        # Update concurrency
        login_manager.max_concurrent = int(concurrent_dropdown.value)
        login_manager.semaphore = asyncio.Semaphore(int(concurrent_dropdown.value))
        
        # Initialize table rows (6列: 序号, 地址, 状态, 用户名, 密码, 详情)
        data_table.rows.clear()
        for idx, url in enumerate(urls):
            data_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(idx + 1), size=13)),  # #
                    ft.DataCell(ft.Text(url, size=13)),  # 地址
                    ft.DataCell(ft.Text("检测中", size=13, color=get_status_color("检测中"))),  # 状态
                    ft.DataCell(ft.Text("", size=13)),  # 用户名
                    ft.DataCell(ft.Text("", size=13)),  # 密码
                    ft.DataCell(ft.Text("", size=13)),  # 详情
                ])
            )
        
        # Update statistics
        stat_success.value = "0"
        stat_failed.value = "0"
        stat_waiting.value = str(len(urls))
        
        # Toggle UI: hide Empty State, show Table
        empty_state.visible = False
        table_container.visible = True
        
        # Start breathing light animation
        toggle_breathing_light(True)
        
        page.update()
        
        # Register callbacks
        login_manager.on_row_update = handle_row_update
        login_manager.on_task_finished = handle_task_finished
        
        # Start batch detection
        await login_manager.batch_detect(urls)
    
    # Bind button click event
    start_button.on_click = start_detection
    
    # ========================================================================
    # End of LoginManager Integration
    # ========================================================================
    
    # === Toolbar (40px height) ===
    # Breathing light state (will be animated)
    breathing_light_ref = ft.Ref[ft.Container]()
    breathing_light_opacity = 0.3
    breathing_light_active = False
    
    async def breathing_light_animation():
        """Breathing light animation loop (1.5s cycle)"""
        import math
        while True:
            if breathing_light_active and breathing_light_ref.current:
                # Calculate opacity using sine wave (0.3 to 1.0)
                elapsed = asyncio.get_event_loop().time()
                opacity = 0.3 + 0.7 * (math.sin(elapsed * 2 * math.pi / 1.5) + 1) / 2
                breathing_light_ref.current.opacity = opacity
                page.update()
            await asyncio.sleep(0.05)  # 50ms update interval
    
    def toggle_breathing_light(active: bool):
        """Toggle breathing light animation"""
        nonlocal breathing_light_active
        breathing_light_active = active
        if active:
            breathing_light_ref.current.bgcolor = "#00ff00"  # Green
        else:
            breathing_light_ref.current.bgcolor = "#808080"  # Gray
            breathing_light_ref.current.opacity = 0.3
        page.update()
    
    toolbar = ft.Container(
        height=40,
        bgcolor="#f5f5f7",  # BG_TABLEHEAD
        border=ft.Border(bottom=ft.BorderSide(1, "#e5e5ea")),  # BORDER_SECONDARY
        padding=ft.Padding(left=16, right=16, top=0, bottom=0),
        content=ft.Row([
            ft.Text("结果", size=11, color="#8e8e8e", weight=ft.FontWeight.W_600),
            ft.Container(expand=True),
            
            # Breathing light (20x20px circle)
            ft.Container(
                ref=breathing_light_ref,
                width=20,
                height=20,
                border_radius=10,  # Circle
                bgcolor="#808080",  # Gray (inactive)
                opacity=0.3,
            ),
            
            ft.Container(width=12),
            
            # Export button (Outlined Style matching v0.app)
            # Replaces simple text with specific icon+text+arrow layout in a bordered container
            ft.PopupMenuButton(
                content=ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.FILE_UPLOAD_OUTLINED, size=14, color=MacColors.TEXT_PRIMARY),
                            ft.Text("导出", size=12, color=MacColors.TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, size=14, color=MacColors.TEXT_SECONDARY),
                        ],
                        spacing=4,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.Padding(8, 4, 8, 4),
                    border=ft.Border.all(1, "#E5E5EA"), # The specific grey border
                    border_radius=6,
                    bgcolor=ft.Colors.WHITE,
                ),
                items=[
                    ft.PopupMenuItem(content=ft.Text("📄 CSV 格式", size=13), on_click=lambda e: export_csv()),
                    ft.PopupMenuItem(content=ft.Text("📊 Excel 格式", size=13), on_click=lambda e: export_excel()),
                    ft.PopupMenuItem(content=ft.Text("📋 JSON 格式", size=13), on_click=lambda e: export_json()),
                    ft.PopupMenuItem(content=ft.Text("📝 Markdown", size=13), on_click=lambda e: export_markdown()),
                    ft.Divider(height=1),
                    ft.PopupMenuItem(content=ft.Text("🖨️ 打印预览", size=13)),
                ],
                tooltip="导出结果",
            ),
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    )
    
    # Empty State Component
    empty_state = ft.Container(
        expand=True,
        content=ft.Column([
            ft.Icon(
                ft.Icons.BOLT,  # ⚡ Lightning bolt (verified: capital I)
                size=64,
                color="#86868B",  # Grey (matching PyQt original)
            ),
            ft.Container(height=16),
            ft.Text(
                "点击「开始探测」以启动",
                size=16,
                color="#86868B",
            ),
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER)  # Use MainAxisAlignment for vertical centering
    )
    
    # Table container (initially hidden)
    table_container = ft.Container(
        content=data_table,
        border=ft.Border.all(width=0.5, color=MacColors.DIVIDER),  # Fixed deprecated API
        border_radius=10,
        visible=False,
    )
    
    main_content = ft.Container(
        expand=True,
        bgcolor="#ffffff",
        content=ft.Column(
            [
                toolbar,  # Added toolbar at the top
                ft.Stack(
                    [
                        empty_state,
                        table_container
                    ],
                    expand=True
                )
            ],
            spacing=0,
            expand=True
        )
    )

    
    # Root Layout (no wrapper needed - Flet is native!)
    layout = ft.Column(
        [
            title_bar,
            menubar,
            ft.Row(
                [
                    sidebar,
                    main_content
                ],
                expand=True,
                spacing=0
            )
        ],
        spacing=0,
        expand=True
    )
    
    # Apply Blur Effect to Sidebar (Flet 0.22+ supports blur on Container)
    # Note: Blur is tricky without specific backend support, but we try standard properties
    sidebar.blur = 10 

    page.add(layout)
    
    # Start breathing light animation loop
    page.run_task(breathing_light_animation)

if __name__ == "__main__":
    print("Launching Flet app...")
    ft.run(main)  # Modern API (ft.app is deprecated)
