
import flet as ft
import asyncio

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
    page.window_width = 1000
    page.window_height = 700
    page.window_resizable = True
    page.window_title_bar_hidden = False # Debug: Show title bar
    page.window_frameless = False # Debug: Show frame
    page.bgcolor = MacColors.SIDEBAR_BG # Debug: Visible background
    page.padding = 0
    page.spacing = 0
    
    print("Flet App Started! Initializing UI...") # Debug log

    # Custom Title Bar (simulating macOS traffic lights)
    def window_drag_area(e):

        page.window_drag_area()

    title_bar = ft.Container(
        content=ft.Row(
            controls=[
                # Mac Traffic Lights
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
                            on_click=lambda e: page.window_maximize()
                        ),
                    ],
                    spacing=8,
                    run_spacing=0,
                ),
                ft.Container(width=20), # Spacer
                ft.WindowDragArea(
                     ft.Text(
                        "OpenWrt Manager", 
                        color=MacColors.TEXT_PRIMARY,
                        weight=ft.FontWeight.W_500,
                        size=13
                    ), expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        height=40,
        bgcolor=MacColors.SIDEBAR_BG,
        padding=ft.Padding(left=16, right=16, top=0, bottom=0),
        border=ft.Border(bottom=ft.BorderSide(0.5, MacColors.SIDEBAR_BORDER))
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

    sidebar = ft.Container(
        width=240,
        bgcolor=MacColors.SIDEBAR_BG,
        border=ft.Border(right=ft.BorderSide(0.5, MacColors.SIDEBAR_BORDER)),
        padding=ft.Padding(left=16, right=16, top=16, bottom=16),
        content=ft.Column(
            [
                ft.Text("MAIN", size=11, color=MacColors.TEXT_SECONDARY, weight=ft.FontWeight.BOLD),
                ft.Container(height=4),
                sidebar_item("📊", "Overview", True),
                sidebar_item("📝", "Batch Login", False),
                sidebar_item("⚙️", "Settings", False),
                
                ft.Container(height=24),
                ft.Text("TOOLS", size=11, color=MacColors.TEXT_SECONDARY, weight=ft.FontWeight.BOLD),
                ft.Container(height=4),
                sidebar_item("💻", "SSH Console", False),
                sidebar_item("🔍", "Diagnostic", False),
            ],
            spacing=2
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
            border=ft.border.all(0.5, MacColors.DIVIDER),
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

    # Data Table Component
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("IP Address")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Latency")),
            ft.DataColumn(ft.Text("Model")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("192.168.1.1")),
                ft.DataCell(ft.Container(
                    content=ft.Text("Success", size=12, color=MacColors.SUCCESS_GREEN),
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=12,
                    bgcolor=ft.Colors.with_opacity(0.1, MacColors.SUCCESS_GREEN)
                )),
                ft.DataCell(ft.Text("2ms")),
                ft.DataCell(ft.Text("OpenWrt 21.02")),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("192.168.1.20")),
                ft.DataCell(ft.Container(
                    content=ft.Text("Auth Failed", size=12, color=MacColors.ERROR_RED),
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=12,
                    bgcolor=ft.Colors.with_opacity(0.1, MacColors.ERROR_RED)
                )),
                ft.DataCell(ft.Text("15ms")),
                ft.DataCell(ft.Text("Unknown")),
            ]),
             ft.DataRow(cells=[
                ft.DataCell(ft.Text("192.168.1.55")),
                ft.DataCell(ft.Container(
                    content=ft.Text("Pending", size=12, color=MacColors.WARNING_ORANGE),
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=12,
                    bgcolor=ft.Colors.with_opacity(0.1, MacColors.WARNING_ORANGE)
                )),
                ft.DataCell(ft.Text("-")),
                ft.DataCell(ft.Text("-")),
            ]),
        ],
        width=float("inf"),
        heading_row_height=40,
        data_row_min_height=48,
        divider_thickness=0.5,
        heading_text_style=ft.TextStyle(size=12, color=MacColors.TEXT_SECONDARY, weight=ft.FontWeight.W_500),
    )

    main_content = ft.Container(
        expand=True,
        bgcolor=MacColors.CONTENT_BG,
        padding=24,
        content=ft.Column(
            [
                ft.Row(
                    [
                        stat_card("Total Devices", "128", MacColors.TEXT_PRIMARY),
                        stat_card("Online", "96", MacColors.SUCCESS_GREEN),
                        stat_card("Offline", "32", MacColors.ERROR_RED),
                    ],
                    spacing=16
                ),
                ft.Container(height=24),
                ft.Text("Recent Activity", size=16, weight=ft.FontWeight.W_600, color=MacColors.TEXT_PRIMARY),
                ft.Container(height=12),
                ft.Container(
                    content=data_table,
                    border=ft.border.all(0.5, MacColors.DIVIDER),
                    border_radius=10,
                )
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )

    # Root Layout
    layout = ft.Column(
        [
            title_bar,
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

if __name__ == "__main__":
    print("Launching Flet app...")
    ft.app(target=main)  # Using app() - run() syntax differs
