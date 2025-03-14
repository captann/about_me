import sys, math
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QFrame
from PyQt5.QtGui import QPainter, QColor, QPen, QImage, QPixmap, QCursor
from PyQt5.QtCore import Qt, QPoint, QTimer, QEvent


def expect_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class Mand(QMainWindow):
    def __init__(self):
        super().__init__()
        # РїР°СЂР°РјРµС‚СЂС‹ РѕРєРЅР°
        self.setFixedSize(600, 300)
        self.setWindowTitle('Множество Мондельброта')
        self.max_iteration = 255
        # РїР°Р»РёС‚СЂР°
        self.palette = [
            (int(255 * math.sin(i / 30.0 + 0.9) ** 2),
             int(255 * math.sin(i / 30.0 + 1.0) ** 2),
             int(255 * math.sin(i / 30.0 + 1.7) ** 2)
             ) for i in range(self.max_iteration - 1)
        ]
        self.palette.append((255, 255, 255))
        # СЃРѕР·РґР°С‘Рј РёР·РѕР±СЂР°Р¶РµРЅРёРµ
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(self.width(), self.height())
        # СЃРѕР·РґР°РЅРёРµ СЃРїРёСЃРєР° РёР·РѕР±СЂР°Р¶РµРЅРёР™
        self.images = [{'params': (-2.0, -1, 1.0, 1), 'image': None}]
        self.images[-1]['image'] = QImage(self.width(), self.height(), QImage.Format_A2RGB30_Premultiplied)
        # СЃРѕС‰РґР°С‘Рј С‚Р°Р№РјРµСЂ РґР»СЏ СЃС‚СЂРѕС‡РЅРѕРіРѕ РїРѕСЃС‚СЂРѕРµРЅРёСЏ
        self.mand_timer = QTimer(self)
        self.mand_timer.setInterval(10)
        self.mand_timer.timeout.connect(self.build_mand_line)
        # СЃРѕР·РґР°РЅРёРµ СЂР°РјРєРё
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, self.width() // 20, self.width() // 20)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setLineWidth(3)
        self.frame.setStyleSheet("color:blue;")
        self.installEventFilter(self)

        self.mouse_pos = None
        # Р·Р°РїСѓСЃРєР°РµРј РїРѕСЃС‚СЂРѕРёС‚РµР»СЊ
        self.start_build_mand()

    def start_build_mand(self):
        # СЃРїСЂСЏС‡РµРј СЂР°РјРєСѓ
        self.frame.hide()
        # СЃРѕР·РґР°РґРёРј РіРµРЅРµСЂР°С‚РѕСЂ РґР»СЏ РѕС‚СЂРёСЃРѕРІРєРё
        self.image_generator = self.mand_color()
        self.mand_timer.start()

    def build_mand_line(self):
        try:
            next(self.image_generator)
            self.image.setPixmap(QPixmap.fromImage(self.images[-1]['image']))
        except StopIteration:
            self.mand_timer.stop()
            # РїРѕРґРІРёРЅСѓС‚СЊ СЂР°РјРєСѓ РІ РЅР°С‡Р°Р»Рѕ
            # РїРѕРєР°Р·Р°С‚СЊ СЂР°РјРєСѓ
            self.frame.move(0, 0)
            self.frame.show()

    def mand_color(self):
        # РєРѕРјРїР»РµРєСЃРЅРѕРµ РїРѕР»Рµ
        painter = QPainter()
        painter.begin(self.images[-1]['image'])
        xa, ya, xb, yb = self.images[-1]['params']
        # СЂР°Р·РјРµСЂС‹ РѕРєРЅР°
        img_x, img_y = self.width(), self.height()
        # РџР°СЂР°РјРµС‚СЂС‹ РїРµСЂР°
        for y in range(img_y):
            # РЅР°Р№РґС‘Рј РєРѕРјРїР»РµРєСЃРЅСѓСЋ РѕСЂРґРёРЅР°С‚Сѓ С‚РѕС‡РєРё
            zy = y * (yb - ya) / img_y + ya
            # РЅР°Р№РґС‘Рј РєРѕРјРїР»РµРєСЃРЅСѓСЋ Р°Р±СЃС†РёСЃСЃСѓ С‚РѕС‡РєРё
            for x in range(img_x):
                zx = x * (xb - xa) / img_x + xa
                # Р·Р°РґР°РґРёРј РЅР°С‡Р°Р»СЊРЅС‹Рµ РїР°СЂР°РјРµС‚СЂС‹ РїРѕСЃР»РµРґРѕРІР°С‚РµР»СЊРЅРѕСЃС‚Рё
                c, z = zx + zy * 1j, 0
                for cnt in range(self.max_iteration):
                    if abs(z) > 2.0:
                        break
                    z = z * z + c
                pen = QPen(QColor(*self.palette[cnt]), 1)
                painter.setPen(pen)
                painter.drawPoint(QPoint(x, y))
            yield True
        painter.end()

    def eventFilter(self, object, event):
        if event.type() == QEvent.Enter:
            self.frame.setCursor(QCursor(Qt.OpenHandCursor))
        elif event.type() == QEvent.Leave:
            self.frame.setCursor(QCursor(Qt.ArrowCursor))
        elif event.type() == QEvent.MouseButtonPress:
            if event.buttons() == Qt.LeftButton:
                self.frame.setCursor(QCursor(Qt.ClosedHandCursor))
                self.mouse_pos = event.windowPos()
        elif event.type() == QEvent.MouseButtonRelease:
            self.frame.setCursor((QCursor(Qt.OpenHandCursor)))
        elif event.type() == QEvent.MouseMove:
            if event.buttons() == Qt.LeftButton:
                # РґРІРёРіР°РµРј СЂР°РјРєСѓ
                move_vector = event.windowPos() - self.mouse_pos
                new_pos = self.frame.pos() + move_vector
                self.frame.move(int(new_pos.x()), int(new_pos.y()))
                self.mouse_pos = event.windowPos()
        elif event.type() == QEvent.MouseButtonDblClick:
            if event.buttons() == Qt.LeftButton:
                old_xa, old_ya, old_xb, old_yb = self.images[-1]['params']
                new_xa = old_xa + self.frame.x() * (old_xb - old_xa) / self.width()
                new_ya = old_ya + self.frame.y() * (old_yb - old_ya) / self.height()
                new_xb = new_xa + self.frame.width() * (old_xb - old_xa) / self.width()
                new_yb = new_ya + self.frame.height() * (old_yb - old_ya) / self.height()
                self.images.append({'params': (new_xa, new_ya, new_xb, new_yb)})
                # СЃРѕР·РґР°С‚СЊ Рё РїРѕР»РѕР¶РёС‚СЊ РЅРѕРІСѓСЋ РєР°СЂС‚РёРЅРєСѓ
                self.images[-1]['image'] = QImage(self.width(), self.height(), QImage.Format_A2RGB30_Premultiplied)
                self.start_build_mand()
            else:
                if len(self.images) > 1:
                    self.images.pop()
                    self.image.setPixmap(QPixmap.fromImage(self.images[-1]['image']))
        return False

if __name__ == '__main__':

    sys.excepthook = expect_hook
    app = QApplication(sys.argv)
    mand = Mand()
    mand.show()
    sys.exit(app.exec())