# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: viewer
# Description: A QGraphicsView subclass for the Climact application that provides a zoomable and scrollable view of the
#              Canvas. The viewer manages shortcuts for all canvas operations, including zooming and panning.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
# Standard:
import os
import types
import google.generativeai as genai

# PySide6:
from PySide6.QtGui import (
    QPainter,
    QShortcut,
    QKeySequence, QInputDevice
)
from PySide6.QtCore import (
    Qt,
    Property,
    QEasingCurve,
    QPropertyAnimation
)
from PySide6.QtWidgets import (
    QWidget,
    QGraphicsView
)

# Climact sub-module(s):
from apps.schema.canvas import Canvas

# QGraphicsView subclass for displaying the scene:
class Viewer(QGraphicsView):
    """
    A QGraphicsView subclass that provides a zoomable and scrollable view of the Canvas.
    """

    # Class constructor:
    def __init__(self, parent: QWidget | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent)

        # Default attributes:
        self.setMouseTracking(True)                                 # Required for detecting hover events
        self.setRenderHint(QPainter.RenderHint.Antialiasing)        # Required for smooth rendering
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)     # Panning mode is default

        # Zooming attribute(s):
        self._zoom = types.SimpleNamespace(
            exp=1.4,                            # Zoom factor (controls the speed of zooming)
            val=1.0,                            # Initial zoom value
            max=kwargs.get("max_zoom", 8.0),   # Maximum zoom value
            min=kwargs.get("min_zoom", 0.2)     # Minimum zoom value
        )

        # Animation:
        self._anim = QPropertyAnimation(self, b"animated_zoom")
        self._anim.setEasingCurve(QEasingCurve.Type.OutExpo)
        self._anim.setDuration(720)  # Animation duration in milliseconds

        # Instantiate the canvas and set it as the scene:
        self.canvas = Canvas(parent = self)
        self.setScene(self.canvas)

        # Google API client:
        genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
        self._tools = self.canvas.functions()
        self._model = genai.GenerativeModel(model_name = "gemini-2.5-flash", tools = self._tools)

        # Start a conversation:
        self._conversation = self._model.start_chat(enable_automatic_function_calling=True)

        # Set up shortcuts:
        QShortcut(QKeySequence("Ctrl+="), self, lambda: self.zoom( 120))        # Zoom in with Ctrl+= (Cmd+= on macOS)
        QShortcut(QKeySequence("Ctrl+-"), self, lambda: self.zoom(-120))        # Zoom out with Ctrl+- (Cmd+- on macOS)
        QShortcut(QKeySequence("Ctrl+0"), self, lambda: self.zoom(None))        # Reset zoom with Ctrl+0 (Cmd+0 on macOS)

    # Handle key-press events:
    def keyPressEvent(self, event):

        # Call super-class implementation, return if the event is accepted:
        super().keyPressEvent(event)
        if event.isAccepted():
            return

        # When Shift is pressed, switch to rubberband drag mode:
        if  event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
            self.setCursor(Qt.CursorShape.CrossCursor)

    # Handle key-release events:
    def keyReleaseEvent(self, event):
        """
        Handle key-press events to switch to rubberband drag mode when Shift is pressed.
        :param event:
        :return:
        """

        super().keyReleaseEvent(event)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    # Handle scroll-events:
    def wheelEvent(self, event):
        """
        Handle the wheel event to zoom in or out based on the scroll indicate.
        :param event: QWheelEvent instance containing scroll-information.
        :return: None
        """

        delta = event.angleDelta().y()
        self.zoom(
            delta,
            animate = event.deviceType() == QInputDevice.DeviceType.Mouse,
        )

    # Handle user-driven zooming:
    def zoom(self, delta: int | float | None, animate: bool = True):
        """
        Scales the field of view based on the provided delta value. If `animate` is True, the zooming operation is
        animated according to the specified easing curve.

        :param delta: The change in zoom level. If None, the zoom will be reset to 1.0.
        :param animate: A flag indicating whether the zoom transition should be animated.
        :return: None
        """

        factor = 1.0 / self._zoom.val if delta is None else self._zoom.exp ** (delta / 100.0)
        target_zoom = max(self._zoom.min, min(self._zoom.max, self._zoom.val * factor))

        if  animate:
            self._anim.stop()
            self._anim.setStartValue(self._zoom.val)
            self._anim.setEndValue(target_zoom)
            self._anim.start()

        else:
            self.scale(factor, factor)
            self._zoom.val = target_zoom

    @Property(float)
    def animated_zoom(self):    return self._zoom.val

    @animated_zoom.setter
    def animated_zoom(self, value):
        """
        Set the animated zoom value and apply the scaling transformation.
        :param value:
        """

        factor = value / self._zoom.val
        self.scale(factor, factor)
        self._zoom.val = value

    # ------------------------------------------------------------------------------------------------------------------
    # Public functions:

    # Send a message to the LLM and fetch the response:
    def get_response_from_llm(self, message: str):

        # Get response from the LLM:
        response = self._conversation.send_message(message)
        print(response)