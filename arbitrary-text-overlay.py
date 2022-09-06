from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import ctypes.wintypes
import win32gui

import threading


class visualHandler:
    textColour = "fff"  ## <- Colour of rendered text
    textSize = 17  ## <- Font size
    textSide = True  ## <- Whether to have a sidebar on the left of the text


class windowHandler:
    def getWindowRect(name: str) -> tuple:
        windowHandle = ctypes.windll.user32.FindWindowW(0, name)
        windowRect = ctypes.wintypes.RECT()

        ctypes.windll.user32.GetWindowRect(windowHandle, ctypes.pointer(windowRect))

        return (windowRect.left, windowRect.top, windowRect.right, windowRect.bottom)

    def hookWindow(origin, target):
        pointerX = windowHandler.getWindowRect(f"{target}")[0]
        pointerY = windowHandler.getWindowRect(f"{target}")[1]

        handle = win32gui.FindWindow(None, f"{origin}")

        pointerWidthX = (
            windowHandler.getWindowRect(f"{target}")[2]
            - windowHandler.getWindowRect(f"{target}")[0]
        )
        pointerWidthY = (
            windowHandler.getWindowRect(f"{target}")[3]
            - windowHandler.getWindowRect(f"{target}")[1]
        )

        win32gui.MoveWindow(
            handle, pointerX, pointerY, pointerWidthX, pointerWidthY, True
        )


class textHandler:
    class hook(QMainWindow):
        def __init__(self, target, displayText, offsetX, offsetY):
            super().__init__()
            self.displayText = displayText

            self.setWindowTitle(f"{displayText}")
            self.setWindowFlags(
                Qt.Window
                | Qt.FramelessWindowHint
                | Qt.CustomizeWindowHint
                | Qt.WindowStaysOnTopHint
            )
            self.setAttribute(Qt.WA_TranslucentBackground)

            self.setGeometry(0, 0, 400, 300)

            self.textHandler = QLabel(
                f'<font color = "#{visualHandler.textColour}">{displayText}</font>',
                self,
            )
            self.textHandler.resize((visualHandler.textSize * len(displayText)), 25)
            self.textHandler.move(offsetX, offsetY)

            if visualHandler.textSide:
                self.textHandler.setStyleSheet(
                    f"padding-left: 5px; border-left: 3px solid #{visualHandler.textColour}; background-color: rgba(0, 0, 0, 0); font-size: {visualHandler.textSize}px; color: #fff; font-weight: 400;"
                )
            else:
                self.textHandler.setStyleSheet(
                    f"padding-left: 5px; background-color: rgba(0, 0, 0, 0); font-size: {visualHandler.textSize}px; color: #fff; font-weight: 400;"
                )

            textShadow = QGraphicsDropShadowEffect()
            textShadow.setBlurRadius(4)
            textShadow.setXOffset(0)
            textShadow.setYOffset(1)
            textShadow.setColor(QColor(f"#000000"))
            self.textHandler.setGraphicsEffect(textShadow)

            hookThread = threading.Thread(target=self.initHook, args=(target,))
            hookThread.start()

            self.show()

        def initHook(self, targetWindow):
            lastX = 0
            lastY = 0

            while True:
                if (
                    windowHandler.getWindowRect(targetWindow)[0] != lastX
                    or windowHandler.getWindowRect(targetWindow)[1] != lastY
                ):
                    try:
                        windowHandler.hookWindow(self.displayText, targetWindow)

                        lastX = windowHandler.getWindowRect(targetWindow)[0]
                        lastY = windowHandler.getWindowRect(targetWindow)[1]
                    except:
                        pass

    def __init__(self, target, displayText, offsetX, offsetY):
        appHandler = QApplication(sys.argv)
        window = self.hook(target, displayText, offsetX, offsetY)

        sys.exit(appHandler.exec())


if __name__ == "__main__":
    textHandler("Lunar Client (1.8.9-43e1b02/master)", "Sample Text", 20, 45)
