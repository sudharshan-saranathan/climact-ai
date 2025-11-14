# Encoding: utf-8
# Module name: viewer
# Description: A QGraphicsView-based schema viewer for the Climact application
import types

from PySide6.QtCore import QPropertyAnimation, Property, QEasingCurve
# Imports:
# PySide6
from PySide6.QtGui import QPainter, QInputDevice
from PySide6.QtWidgets import QGraphicsView, QCheckBox
from apps.schema.canvas import Canvas


class Viewer(QGraphicsView):

    # Default constructor:
    def __init__(self, **kwargs):

        # Base-class initialization:
        super().__init__(**kwargs)

        # Set class-level attribute(s):
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate)

        # Instantiate a canvas and set it as the scene:
        self.canvas = Canvas(self)
        self.setScene(self.canvas)
        self.setCornerWidget(QCheckBox(self))
        self.cornerWidget().setChecked(False)

        # Initialize zoom and zoom-animation attribute(s):
        self._zoom = types.SimpleNamespace(
            scale = 1.0,
            min   = 0.2,
            max   = 8.0,
            exp   = 1.2
        )

        # Setup animation:
        self._anim = QPropertyAnimation(self, b"zoom")
        self._anim.setEasingCurve(QEasingCurve.Type.OutExpo)
        self._anim.setDuration(720)

    # Reimplementation of event handlers for Qt events:
    # QWheelEvent:
    def wheelEvent(self, event, /):

        delta = event.angleDelta().y()
        delta = 1.5 ** (delta / 100.0)

        self.execute_zoom(delta, event.deviceType() == QInputDevice.DeviceType.Mouse)

    # Animation property:
    def get_zoom(self, /):
        return self._zoom.scale

    # Set the zoom level:
    def set_zoom(self, value, /):

        factor = value / self._zoom.scale
        self.scale(factor, factor)
        self._zoom.scale = value

    # Zoom execution:
    def execute_zoom(self, factor, animate = True, /):

        # Stop any ongoing animation:
        if  self._anim.state() == QPropertyAnimation.State.Running:
            self._anim.stop()

        # Calculate the target zoom level:
        target = self._zoom.scale * factor
        target = max(self._zoom.min, min(self._zoom.max, target))

        # Set up and start the animation:
        if  animate:
            self._anim.setStartValue(self._zoom.scale)
            self._anim.setEndValue(target)
            self._anim.start()

        else:
            self.set_zoom(target)

    # Zoom property:
    zoom = Property(float, get_zoom, set_zoom)