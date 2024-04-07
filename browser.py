from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

class VideoWebView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.NoContextMenu)

    def toggle_full_screen(self):
        script = """
        var video = document.querySelector('video');
        if (video) {
            if (video.requestFullscreen) {
                video.requestFullscreen();
            } else if (video.webkitRequestFullscreen) { /* Safari */
                video.webkitRequestFullscreen();
            } else if (video.msRequestFullscreen) { /* IE11 */
                video.msRequestFullscreen();
            }
        }
        """
        self.page().runJavaScript(script)

class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.new_tab()

    def new_tab(self, url=None):
        webview = VideoWebView()
        webview.load(QUrl(url) if url else QUrl("https://www.google.com"))
        index = self.addTab(webview, "New Tab")
        self.setCurrentIndex(index)

    def close_tab(self, index):
        self.removeTab(index)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Web Browser")

        # Khởi tạo QWidget
        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        # Tạo layout
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        # Tạo layout cho thanh tìm kiếm
        self.search_layout = QHBoxLayout()
        self.layout.addLayout(self.search_layout)

        # Thêm nút "Quay lại"
        self.back_button = QPushButton("Quay lại")
        self.back_button.setFixedWidth(80)
        self.back_button.setStyleSheet("background-color: #f0f0f0; border: 1px solid gray;")
        self.back_button.setIcon(QIcon("icons/back.png"))
        self.search_layout.addWidget(self.back_button)

        # Thêm nút "Tới"
        self.forward_button = QPushButton("Tới")
        self.forward_button.setFixedWidth(80)
        self.forward_button.setStyleSheet("background-color: #f0f0f0; border: 1px solid gray;")
        self.forward_button.setIcon(QIcon("icons/forward.png"))
        self.search_layout.addWidget(self.forward_button)

        # Thêm thanh tìm kiếm
        self.search_bar = QLineEdit()
        self.search_bar.setStyleSheet("background-color: white; border: 1px solid gray;")
        self.search_layout.addWidget(self.search_bar)

        # Kết nối sự kiện nhấn Enter để tìm kiếm
        self.search_bar.returnPressed.connect(self.search)

        # Thêm QTabWidget
        self.tabs = TabWidget()
        self.layout.addWidget(self.tabs)

        # Kết nối các nút với các hàm
        self.forward_button.clicked.connect(self.go_forward)
        self.back_button.clicked.connect(self.go_back)

    def search(self):
        current_webview = self.tabs.currentWidget()
        if current_webview:
            url = self.search_bar.text()
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url
            current_webview.load(QUrl(url))

    def go_forward(self):
        current_webview = self.tabs.currentWidget()
        if current_webview:
            current_webview.forward()

    def go_back(self):
        current_webview = self.tabs.currentWidget()
        if current_webview:
            current_webview.back()

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
