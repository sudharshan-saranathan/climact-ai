# Encoding: utf-8
# Module name: viewer
# Description: A QGraphicsView-based schema viewer for the Climact application
import types

# Module Imports:
# PySide6:
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

from apps.schema.canvas import Canvas


class Viewer(QtWidgets.QGraphicsView):

    # Default constructor:
    def __init__(self, **kwargs):

        # Base-class initialization:
        super().__init__(**kwargs)

        # Set class-level attribute(s):
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate)

        # Instantiate a canvas and set it as the scene:
        self.canvas = Canvas(self)
        self.setScene(self.canvas)
        self.setCornerWidget(checkbox := QtWidgets.QCheckBox(self)); checkbox.setChecked(True)

        # Initialize zoom and zoom-animation attribute(s):
        self._zoom = types.SimpleNamespace(
            scale = 1.0,
            min   = 0.2,
            max   = 8.0,
            exp   = 1.2
        )

        # Setup animation:
        self._anim = QtCore.QPropertyAnimation(self, b"zoom")
        self._anim.setEasingCurve(QtCore.QEasingCurve.Type.OutExpo)
        self._anim.setDuration(720)

    # Reimplementation of event handlers for Qt events:
    # Key Event Handlers:
    def keyPressEvent(self, event, /):

        # When the Shift key is pressed, switch to selection mode:
        if  event.modifiers() == QtCore.Qt.KeyboardModifier.ShiftModifier:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.RubberBandDrag)

        super().keyPressEvent(event)

    # When the Shift key is released, switch back to hand-drag mode:
    def keyReleaseEvent(self, event, /):

        # When the Shift key is released, switch back to hand-drag mode:
        if  event.modifiers() == QtCore.Qt.KeyboardModifier.NoModifier:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
            self.unsetCursor()

        super().keyReleaseEvent(event)

    # QWheelEvent:
    def wheelEvent(self, event, /):

        delta = event.angleDelta().y()
        delta = 1.5 ** (delta / 100.0)

        self.execute_zoom(delta, event.deviceType() == QtGui.QInputDevice.DeviceType.Mouse)

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
        if  self._anim.state() == QtCore.QPropertyAnimation.State.Running:
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
    zoom = QtCore.Property(float, get_zoom, set_zoom)