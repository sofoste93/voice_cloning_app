from math import sin
from random import Random

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QPen, QRadialGradient
from PyQt6.QtWidgets import QWidget


class NeptuneBanner(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(188)
        random = Random(2020)
        self.stars = [(random.random(), random.random(), random.randrange(45, 185))
                      for _ in range(145)]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        bounds = QRectF(self.rect())
        background = QPainterPath()
        background.addRoundedRect(bounds, 20, 20)
        painter.setClipPath(background)
        painter.fillRect(bounds, QColor("#0b1731"))

        center = QPointF(self.width() * 0.80, 112)
        glow = QRadialGradient(center, 210)
        glow.setColorAt(0, QColor("#305d9a"))
        glow.setColorAt(1, QColor(13, 25, 50, 0))
        painter.fillRect(bounds, glow)
        for x, y, alpha in self.stars:
            painter.setPen(QPen(QColor(173, 208, 255, int(alpha * (0.45 if x < 0.5 else 1))), 1))
            painter.drawPoint(QPointF(x * self.width(), y * self.height()))

        painter.save()
        painter.translate(center)
        painter.rotate(-17)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        for radius in (117, 149, 180):
            painter.setPen(QPen(QColor(124, 177, 248, 61), 1))
            painter.drawEllipse(QPointF(), radius, radius * 0.43)
        painter.restore()

        radius = 87
        sphere = QPainterPath()
        sphere.addEllipse(center, radius, radius)
        painter.setClipPath(sphere, Qt.ClipOperation.IntersectClip)
        surface = QRadialGradient(center + QPointF(-36, -52), 158)
        for stop, color in ((0, "#bceaff"), (0.30, "#65a4f4"), (0.60, "#345db8"),
                            (0.83, "#1b3480"), (1, "#0b133c")):
            surface.setColorAt(stop, QColor(color))
        painter.fillRect(bounds, surface)
        for index in range(34):
            latitude = center.y() - radius + 5 * index
            cloud = QPainterPath(QPointF(center.x() - radius, latitude))
            for offset in range(-radius + 4, radius + 5, 4):
                wave = sin(offset / 31 + index / 5) * 3
                cloud.lineTo(center.x() + offset, latitude + wave + offset * 0.19)
            painter.setPen(QPen(QColor(167, 219, 255, 12 + index % 5 * 6), 1 + index % 3))
            painter.drawPath(cloud)
        painter.setPen(QPen(QColor(169, 222, 255, 125), 1.5))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(center, radius, radius)
