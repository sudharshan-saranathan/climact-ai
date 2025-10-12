# Encoding: utf-8
# Module name: string
# Description: A QGraphicsTextItem subclass with customizable options.

from PySide6.QtCore import Qt, Signal, QPointF, QRectF
from PySide6.QtGui import QFont, QColor, QTextCursor,  QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem, QStyle

LabelOpts = {

    "const" : False,                            # Whether the string is immutable.
    "round" : 4,                                # Radius for rounded corners.
    "coord" : QPointF(0, 0),                    # Default position of the label with respect to its parent.
    "style" : {
        "border"    : Qt.GlobalColor.transparent,
        "background": Qt.GlobalColor.transparent
    },
    "text-font"  : QFont("Trebuchet MS", 7),
    "text-color" : Qt.GlobalColor.black,
    "text-align" : Qt.AlignmentFlag.AlignCenter,
    "text-width" : 60.0
}

# Class String: A custom-QGraphicsTextItem
class Label(QGraphicsTextItem):

    # Signals:
    sig_text_changed = Signal(str, name="String.sig_text_changed")

    # Initializer:
    def __init__(self, label: str, parent: QGraphicsItem | None = None, **kwargs):

        # Initialize base-class:
        super().__init__(label, parent)
        super().setAcceptHoverEvents(True)

        # Retrieve keywords:
        self.setProperty("const", kwargs.get('const', LabelOpts["const"]))
        self.setProperty("round", kwargs.get('round', LabelOpts["round"]))
        self.setProperty("style", kwargs.get('style', LabelOpts["style"]))

        self.setProperty("text-font" , kwargs.get('font' , LabelOpts["text-font"]))
        self.setProperty("text-color", kwargs.get('color', LabelOpts["text-color"]))
        self.setProperty("text-align", kwargs.get('align', LabelOpts["text-align"]))
        self.setProperty("text-width", kwargs.get('width', LabelOpts["text-width"]))

        # Customize attribute(s):
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction if not self.property("const") else Qt.TextInteractionFlag.NoTextInteraction)
        self.setDefaultTextColor(self.property("text-color"))

        self.setTextWidth(self.property("text-width"))
        self.setFont(self.property("text-font"))

        # Set alignment:
        option = self.document().defaultTextOption()
        option.setAlignment(self.property("text-align"))
        self.document().setDefaultTextOption(option)

    # Reimplementation of QGraphicsTextItem.paint():
    def paint(self, painter, option, widget):

        # Reset the state-flag to prevent the dashed-line selection style.
        option.state = QStyle.StateFlag.State_None

        # Compute the actual text-width:
        fmet = painter.fontMetrics()
        size = fmet.size(0, self.toPlainText())

        rect = QRectF(0, 0, size.width(), size.height())
        rect = rect.translated(self.boundingRect().center() - rect.center())

        # Paint the border and background:
        painter.setPen(QPen(self.property("style")["border"], 0.75))
        painter.setBrush(self.property("style")["background"])
        painter.drawRoundedRect(rect, self.property("round"), self.property("round"))

        # Invoke base-class implementation to paint the text:
        super().paint(painter, option, widget)

    # Edit text:
    def edit(self):

        # If the item is immutable, return immediately:
        if self.property("const"):   return

        # Make label edit:
        self.setFocus(Qt.FocusReason.OtherFocusReason)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)

        # Highlight text:
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
        self.setTextCursor(cursor)

    # Reimplementation of QGraphicsTextItem.keyPressEvent():
    def keyPressEvent(self, event):
        """
        Handles key press events for the text item.
        :param event:
        :return:
        """

        # If the key pressed is `Return`, finish editing and clear focus:
        if  event.key() == Qt.Key.Key_Return:
            self.clearFocus()
            event.accept()
            return

        # Otherwise, call super-class implementation:
        super().keyPressEvent(event)

    # Reimplementation of QGraphicsTextItem.focusInEvent():
    def focusInEvent(self, event):
        """
        This method is called when the text item gains focus.
        :param event:
        :return:
        """

        # If the item is immutable, return immediately:
        if self.property("const"):   return

        # Super-class implementation:
        super().focusInEvent(event)

    # Reimplementation of QGraphicsTextItem.focusOutEvent():
    def focusOutEvent(self, event):

        # Clear text-selection and emit signal:
        string = self.toPlainText().strip()     # Get the text and strip whitespace
        self.sig_text_changed.emit(string)      # Emit signal with new text as the argument
        self.textCursor().clearSelection()      # Clear text-selection

        # Super-class implementation:
        super().focusOutEvent(event)

    # Reimplementation of QGraphicsTextItem.hoverEnterEvent():
    def hoverEnterEvent(self, event):
        """
        Handles the hover enter event to change the cursor shape.
        :param event: QGraphicsSceneHoverEvent
        """

        if  not self.property("const"):
            self.setCursor(Qt.CursorShape.IBeamCursor)
            self.update()

        super().hoverEnterEvent(event)

    # Reimplementation of QGraphicsTextItem.hoverEnterEvent():
    def hoverLeaveEvent(self, event):
        """
        Handles the hover enter event to change the cursor shape.
        """

        if  not self.property("const"):
            self.setCursor(Qt.CursorShape.IBeamCursor)
            self.update()

        super().hoverLeaveEvent(event)

    @property
    def const(self):
        return self.property("const")

    @const.setter
    def const(self, value: bool):
        """
        Set the const property of the string.
        :param value: bool
        """
        self.setProperty("const", value)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction if value else Qt.TextInteractionFlag.TextEditorInteraction)
        self.update()