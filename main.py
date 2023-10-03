import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QCheckBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl, QEvent

class MainWindow(QWidget):
  synchronise_keypresses = False
  synchronise_urls = False
  qwebengineview_left = None
  qwebengineview_right = None
  
  def onChanged(self):
    checkbox_control = self.sender()
    print("Checkbox state changed")
    self.synchronise_keypresses = checkbox_control.isChecked()

  def onChangedSyncUrls(self):
    control = self.sender()
    self.synchronise_urls = control.isChecked()

  def handle_url_changed(self, url):
    if self.synchronise_urls:
      self.qwebengineview_right.setUrl(url)

  def __init__(self):
    super().__init__()

    layout_main = QVBoxLayout()
    layout_horizontal = QHBoxLayout()
    self.qwebengineview_left = QWebEngineView()
    qprofile_left = QWebEngineProfile("left", self.qwebengineview_left)
    qwebpage_left = QWebEnginePage(qprofile_left, self.qwebengineview_left)

    self.qwebengineview_left.setPage(qwebpage_left)
    
    self.qwebengineview_right = QWebEngineView()
    qprofile_right = QWebEngineProfile("right", self.qwebengineview_right)
    self.qwebpage_right = QWebEnginePage(qprofile_right, self.qwebengineview_right)
    self.qwebengineview_right.setPage(self.qwebpage_right)

    checkbox = QCheckBox("WIP - Synchronise Key Presses Across Browsers")
    checkbox.toggled.connect(self.onChanged)
    layout_main.addWidget(checkbox)

    checkbox_sync_urls = QCheckBox("Synchronise URL Changes Across Browsers")
    checkbox_sync_urls.toggled.connect(self.onChangedSyncUrls)
    layout_main.addWidget(checkbox_sync_urls)

    layout_horizontal.addWidget(self.qwebengineview_left)
    layout_horizontal.addWidget(self.qwebengineview_right)

    self.qwebengineview_left.setUrl(QUrl("https://www.saucedemo.com"))
    self.qwebengineview_right.setUrl(QUrl("https://www.saucedemo.com"))

    self.qwebengineview_left.focusProxy().installEventFilter(self)
    self.qwebengineview_left.urlChanged.connect(self.handle_url_changed)
    
    layout_main.addLayout(layout_horizontal)
    self.setLayout(layout_main)
    self.show()

  def eventFilter(self, source, event):
    target = QApplication.focusWidget()
    if (event.type() == QEvent.KeyPress):
      if target.parentWidget() is self.qwebengineview_left:
        print("Key press from left browser")
        return False
      else:
        print("Key press from right browser")
        return True
      
    return super().eventFilter(source, event)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  app.exec()
