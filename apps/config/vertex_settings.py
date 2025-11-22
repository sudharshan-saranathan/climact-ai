# python
# File: apps/config/vertex_settings.py
from __future__ import annotations

from typing import Any, Iterable
from PySide6 import QtCore, QtWidgets, QtGui
import qtawesome as qta
import pyqtgraph as pg

class TimeSeriesEditor(QtWidgets.QDialog):
    """
    Simple (t, y) timeseries editor with interpolation choice.
    Stores timeseries as list of (t: float, y: float).
    """
    def __init__(self, parent: QtWidgets.QWidget | None = None, *, title: str = "Time series", series: Iterable[tuple[float, float]] | None = None, interp: str = "linear"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(520, 360)

        self._table = QtWidgets.QTableWidget(self)
        self._table.setColumnCount(2)
        self._table.setHorizontalHeaderLabels(["t", "y"])
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.verticalHeader().setVisible(False)
        self._table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self._interp = QtWidgets.QComboBox(self)
        self._interp.addItems(["step", "linear", "spline"])
        ix = max(0, self._interp.findText(interp))
        self._interp.setCurrentIndex(ix)

        btn_add = QtWidgets.QPushButton("+", self)
        btn_del = QtWidgets.QPushButton("-", self)
        btn_clr = QtWidgets.QPushButton("Clear", self)
        btn_ok = QtWidgets.QPushButton("OK", self)
        btn_ca = QtWidgets.QPushButton("Cancel", self)

        btn_add.clicked.connect(self._add_row)
        btn_del.clicked.connect(self._del_rows)
        btn_clr.clicked.connect(self._clear)
        btn_ok.clicked.connect(self.accept)
        btn_ca.clicked.connect(self.reject)

        top = QtWidgets.QHBoxLayout()
        top.addWidget(QtWidgets.QLabel("Interpolation:", self))
        top.addWidget(self._interp)
        top.addStretch()
        top.addWidget(btn_add)
        top.addWidget(btn_del)
        top.addWidget(btn_clr)

        bot = QtWidgets.QHBoxLayout()
        bot.addStretch()
        bot.addWidget(btn_ok)
        bot.addWidget(btn_ca)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addLayout(top)
        lay.addWidget(self._table)
        lay.addLayout(bot)

        for t, y in (series or []):
            self._append(t, y)

    def _append(self, t: float = 0.0, y: float = 0.0) -> None:
        r = self._table.rowCount()
        self._table.insertRow(r)
        self._table.setItem(r, 0, QtWidgets.QTableWidgetItem(f"{float(t):.6g}"))
        self._table.setItem(r, 1, QtWidgets.QTableWidgetItem(f"{float(y):.6g}"))

    @QtCore.Slot()
    def _add_row(self) -> None:
        self._append(0.0, 0.0)

    @QtCore.Slot()
    def _del_rows(self) -> None:
        rows = sorted({i.row() for i in self._table.selectedIndexes()}, reverse=True)
        for r in rows:
            self._table.removeRow(r)

    @QtCore.Slot()
    def _clear(self) -> None:
        self._table.setRowCount(0)

    def series(self) -> list[tuple[float, float]]:
        out: list[tuple[float, float]] = []
        for r in range(self._table.rowCount()):
            try:
                t = float(self._table.item(r, 0).text())
                y = float(self._table.item(r, 1).text())
                out.append((t, y))
            except Exception:
                continue
        out.sort(key=lambda p: p[0])
        return out

    def interpolation(self) -> str:
        return self._interp.currentText()

# python
# File: apps/config/vertex_settings.py

from typing import Iterable
from PySide6 import QtCore, QtWidgets


class EquationEditor(QtWidgets.QDialog):
    """
    Minimal equation editor. Expects a scalar expression per line.
    Optionally shows available symbols to the user.
    """
    def __init__(self, parent: QtWidgets.QWidget | None = None, *, title: str = "Equations", equations: Iterable[str] | None = None, symbols: Iterable[str] | None = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(720, 420)

        self._text = QtWidgets.QPlainTextEdit(self)
        self._text.setPlaceholderText("# Enter one equation per line, e.g.\n# out_flow = in_flow * efficiency")
        if equations:
            self._text.setPlainText("\n".join(equations))

        sym_label = QtWidgets.QLabel("Symbols: " + (", ".join(symbols or []) or "N/A"), self)
        sym_label.setWordWrap(True)

        btn_ok = QtWidgets.QPushButton("OK", self)
        btn_ca = QtWidgets.QPushButton("Cancel", self)
        btn_ok.clicked.connect(self.accept)
        btn_ca.clicked.connect(self.reject)

        bot = QtWidgets.QHBoxLayout()
        bot.addStretch()
        bot.addWidget(btn_ok)
        bot.addWidget(btn_ca)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(sym_label)
        lay.addWidget(self._text, 1)
        lay.addLayout(bot)

    def equations(self) -> list[str]:
        return [ln.strip() for ln in self._text.toPlainText().splitlines() if ln.strip()]

# python
# File: apps/config/vertex_settings.py

from typing import Any
from PySide6 import QtCore, QtWidgets

class VertexSettings(QtWidgets.QDialog):
    """
    Settings dialog for a vertex. Provides:
    - Editable inputs/outputs/parameters/equations with time series support
    - Right-side plot using pyqtgraph
    - Solve button to use AMPL backend if available
    """
    def __init__(self, vertex: QtWidgets.QGraphicsObject, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle(f"Vertex Settings: {vertex.property('label') or 'vertex'}")
        self.setModal(True)
        self.resize(1440, 900)

        self._vertex = vertex
        self._plot = pg.PlotWidget(background="#ffffff")
        self._tree = QtWidgets.QTreeWidget(self)

        self._inp_root = QtWidgets.QTreeWidgetItem(self._tree)
        self._inp_root.setText(0, "Inputs")
        self._inp_root.setIcon(0, qta.icon("mdi.arrow-right", color="#0077cc"))

        self._out_root = QtWidgets.QTreeWidgetItem(self._tree)
        self._out_root.setText(0, "Outputs")
        self._out_root.setIcon(0, qta.icon("mdi.arrow-left", color="#00aa00"))

        self._par_root = QtWidgets.QTreeWidgetItem(self._tree)
        self._par_root.setText(0, "Parameters")
        self._par_root.setIcon(0, qta.icon("mdi.tune", color="#ffaa00"))

        self._eqn_root = QtWidgets.QTreeWidgetItem(self._tree)
        self._eqn_root.setText(0, "Equations")
        self._eqn_root.setIcon(0, qta.icon("mdi.function", color="#9944cc"))

        self._tree.setColumnCount(5)
        self._tree.setHeaderLabels(["Name", "Type", "Value", "Units", "f(t)"])
        self._tree.setColumnWidth(0, 180)
        self._tree.setColumnWidth(1, 160)
        self._tree.setColumnWidth(2, 100)
        self._tree.setColumnWidth(3, 100)
        self._tree.setColumnWidth(4, 70)

        # Layout
        left = QtWidgets.QVBoxLayout()
        left.addWidget(self._tree, 1)
        left.addLayout(self._init_footer())

        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)
        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(self._plot)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 1)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(main_splitter)
        self.setLayout(layout)

    def _init_footer(self) -> QtWidgets.QHBoxLayout:
        btn_solve = QtWidgets.QPushButton(qta.icon("mdi.calculator-variant-outline", color="#00a650"), "Solve", self)
        btn_reset = QtWidgets.QPushButton(qta.icon("mdi.restore", color="#888888"), "Reset", self)
        btn_close = QtWidgets.QPushButton(qta.icon("mdi.close", color="#cc0000"), "Close", self)

        btn_solve.clicked.connect(self._on_solve)
        btn_reset.clicked.connect(self._on_reset)
        btn_close.clicked.connect(self.close)

        lay = QtWidgets.QHBoxLayout()
        lay.addStretch()
        lay.addWidget(btn_reset)
        lay.addWidget(btn_solve)
        lay.addWidget(btn_close)
        return lay

    def _update_tree(self) -> None:
        self._inp_root.takeChildren()
        self._out_root.takeChildren()
        self._par_root.takeChildren()
        self._eqn_root.takeChildren()

        v = self._vertex

        def add_stream_row(root: QtWidgets.QTreeWidgetItem, handle: QtWidgets.QGraphicsObject) -> None:
            item = QtWidgets.QTreeWidgetItem(root)
            label = handle.property("label") or "stream"
            item.setText(0, label)
            item.setData(0, QtCore.Qt.ItemDataRole.UserRole, handle)

            type_box = QtWidgets.QComboBox(self)
            type_box.addItem("MassFlow")
            type_box.addItem("EnergyFlow")
            type_box.addItem("Custom")
            current = handle.property("stream_type") or "MassFlow"
            ix = type_box.findText(current)
            if ix >= 0:
                type_box.setCurrentIndex(ix)
            type_box.currentTextChanged.connect(lambda t, h=handle: h.setProperty("stream_type", t))

            val_box = QtWidgets.QDoubleSpinBox(self)
            val_box.setRange(-1e18, 1e18)
            val_box.setDecimals(9)
            val_box.setSingleStep(0.1)
            try:
                val_box.setValue(float(handle.property("value") or 0.0))
            except Exception:
                val_box.setValue(0.0)
            val_box.valueChanged.connect(lambda v, h=handle: h.setProperty("value", float(v)))

            unit_box = QtWidgets.QComboBox(self)
            unit_box.addItems(["kg", "m3", "MJ", "kWh"])
            current_unit = handle.property("units") or "kg"
            ix = unit_box.findText(current_unit)
            if ix >= 0:
                unit_box.setCurrentIndex(ix)
            unit_box.currentTextChanged.connect(lambda u, h=handle: h.setProperty("units", u))

            ts_btn = QtWidgets.QToolButton(self)
            ts_btn.setIcon(qta.icon("mdi.chart-timeline-variant", color="#0077cc"))
            ts_btn.setAutoRaise(True)

            def open_ts():
                series = handle.property("timeseries") or []
                interp = handle.property("interp") or "linear"
                dlg = TimeSeriesEditor(self, title=f"{label} f(t)", series=series, interp=interp)
                if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                    handle.setProperty("timeseries", dlg.series())
                    handle.setProperty("interp", dlg.interpolation())
                    self._plot_series()

            ts_btn.clicked.connect(open_ts)

            self._tree.setItemWidget(item, 1, type_box)
            self._tree.setItemWidget(item, 2, val_box)
            self._tree.setItemWidget(item, 3, unit_box)
            self._tree.setItemWidget(item, 4, ts_btn)

        # Inputs and outputs
        for h in getattr(v.connections, "inp", []):
            add_stream_row(self._inp_root, h)
        for h in getattr(v.connections, "out", []):
            add_stream_row(self._out_root, h)

        # Parameters
        params: list[dict[str, Any]] = list(v.property("parameters") or [])
        def add_param_row(p: dict[str, Any]) -> None:
            item = QtWidgets.QTreeWidgetItem(self._par_root)
            item.setText(0, str(p.get("name", "param")))

            val = QtWidgets.QDoubleSpinBox(self)
            val.setRange(-1e18, 1e18)
            val.setDecimals(9)
            val.setValue(float(p.get("value", 0.0)))
            val.valueChanged.connect(lambda v, d=p: d.__setitem__("value", float(v)))

            units = QtWidgets.QLineEdit(self)
            units.setText(str(p.get("units", "")))
            units.editingFinished.connect(lambda d=p, w=units: d.__setitem__("units", w.text()))

            ts_btn = QtWidgets.QToolButton(self)
            ts_btn.setIcon(qta.icon("mdi.chart-timeline-variant", color="#0077cc"))
            ts_btn.setAutoRaise(True)

            def open_ts():
                dlg = TimeSeriesEditor(self, title=f"{p.get('name','param')} f(t)", series=p.get("timeseries") or [], interp=p.get("interp", "linear"))
                if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                    p["timeseries"] = dlg.series()
                    p["interp"] = dlg.interpolation()
                    self._plot_series()

            ts_btn.clicked.connect(open_ts)

            self._tree.setItemWidget(item, 2, val)
            self._tree.setItemWidget(item, 3, units)
            self._tree.setItemWidget(item, 4, ts_btn)

        for p in params:
            add_param_row(p)

        self._install_toolbar(self._par_root, on_add=lambda: self._on_add_param(params, add_param_row), on_del=lambda: self._on_del_selected(self._par_root, params))

        # Equations
        equations: list[str] = list(v.property("equations") or [])
        for eq in equations:
            item = QtWidgets.QTreeWidgetItem(self._eqn_root)
            item.setText(0, eq)

        def add_eq():
            sym = self._available_symbols()
            dlg = EquationEditor(self, equations=[], symbols=sym)
            if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                equations.extend(dlg.equations())
                v.setProperty("equations", equations)
                self._update_tree()

        def edit_eq():
            sym = self._available_symbols()
            sel = self._tree.currentItem()
            if sel and sel.parent() is self._eqn_root:
                dlg = EquationEditor(self, equations=[sel.text(0)], symbols=sym)
                if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                    lines = dlg.equations()
                    if lines:
                        idx = self._eqn_root.indexOfChild(sel)
                        equations[idx] = lines[0]
                        self._eqn_root.child(idx).setText(0, lines[0])
                        v.setProperty("equations", equations)

        self._install_toolbar(self._eqn_root, on_add=add_eq, on_del=lambda: self._on_del_selected(self._eqn_root, equations), extra_actions=[("mdi.pencil", "#ffaa00", "Edit", edit_eq)])

        self._tree.expandAll()
        v.setProperty("parameters", params)
        v.setProperty("equations", equations)

    def _install_toolbar(self, root: QtWidgets.QTreeWidgetItem, *, on_add, on_del, extra_actions: list[tuple[str, str, str, callable]] | None = None) -> None:
        bar = QtWidgets.QToolBar(self)
        bar.setIconSize(QtCore.QSize(20, 20))
        bar.addAction(qta.icon("mdi.minus", color="#efefef"), "Delete").triggered.connect(on_del)
        bar.addAction(qta.icon("mdi.plus", color="#ffcb00"), "Add").triggered.connect(on_add)
        for icon, color, text, fn in (extra_actions or []):
            bar.addAction(qta.icon(icon, color=color), text).triggered.connect(fn)
        self._tree.setItemWidget(root, 1, bar)

    def _on_add_param(self, params: list[dict[str, Any]], add_row_cb) -> None:
        p = {"name": f"param_{len(params)+1}", "value": 0.0, "units": "", "timeseries": [], "interp": "linear"}
        params.append(p)
        add_row_cb(p)

    def _on_del_selected(self, root: QtWidgets.QTreeWidgetItem, backing: list[Any]) -> None:
        it = self._tree.currentItem()
        if it and it.parent() is root:
            idx = root.indexOfChild(it)
            root.removeChild(it)
            if 0 <= idx < len(backing):
                backing.pop(idx)

    def _available_symbols(self) -> list[str]:
        v = self._vertex
        names = []
        for h in getattr(v.connections, "inp", []):
            names.append(h.property("label") or "in")
        for h in getattr(v.connections, "out", []):
            names.append(h.property("label") or "out")
        for p in (v.property("parameters") or []):
            names.append(p.get("name", "param"))
        return sorted(set(names))

    def _plot_series(self) -> None:
        self._plot.clear()
        v = self._vertex

        def plot_entity(name: str, series: list[tuple[float, float]], color: str = "#1f77b4"):
            if not series:
                return
            xs = [t for t, _ in series]
            ys = [y for _, y in series]
            self._plot.plot(xs, ys, pen=pg.mkPen(color=color, width=2), name=name, symbol=None)

        for h in list(getattr(v.connections, "inp", [])) + list(getattr(v.connections, "out", [])):
            series = h.property("timeseries") or []
            color = h.property("color") or "#1f77b4"
            label = h.property("label") or "stream"
            plot_entity(label, series, color)

        for p in (v.property("parameters") or []):
            series = p.get("timeseries") or []
            plot_entity(p.get("name", "param"), series, "#2ca02c")

    @QtCore.Slot()
    def _on_solve(self) -> None:
        v = self._vertex
        build = getattr(v, "build_ampl_model", None)

        if callable(build):
            try:
                from amplpy import AMPL
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "AMPL", f"AMPL backend not available:\n{e}")
                return
            try:
                mod, dat, var_map = build()
                ampl = AMPL()
                if mod:
                    ampl.eval(mod)
                if dat:
                    ampl.eval(dat)
                ampl.solve()

                if isinstance(var_map, dict):
                    for target, (var_name, comp) in var_map.items():
                        value = ampl.getVariable(var_name).get(comparison=comp).value() if comp is not None else ampl.getVariable(var_name).value()
                        self._assign_result(v, target, value)

                self._update_tree()
                self._plot_series()
                QtWidgets.QMessageBox.information(self, "Solve", "Solve completed.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Solve error", str(e))
            return

        try:
            eff = None
            for p in (v.property("parameters") or []):
                if (p.get("name") or "").lower() in ("efficiency", "eta"):
                    eff = float(p.get("value", 0.0))
            if eff is not None and v.connections.inp and v.connections.out:
                s_in = float(v.connections.inp[0].property("value") or 0.0)
                v.connections.out[0].setProperty("value", s_in * eff)
                self._update_tree()
                self._plot_series()
                QtWidgets.QMessageBox.information(self, "Solve", "Simple solve completed.")
                return
        except Exception:
            pass

        QtWidgets.QMessageBox.information(self, "Solve", "No AMPL model provided by vertex and no simple rule available.")

    def _assign_result(self, vertex: QtWidgets.QGraphicsObject, target: str, value: float) -> None:
        try:
            kind, rest = target.split(":", 1)
            if kind == "out":
                idx, attr = rest.split(".", 1)
                h = vertex.connections.out[int(idx)]
                h.setProperty(attr, float(value))
            elif kind == "inp":
                idx, attr = rest.split(".", 1)
                h = vertex.connections.inp[int(idx)]
                h.setProperty(attr, float(value))
            elif kind == "param":
                name = rest.strip()
                params = vertex.property("parameters") or []
                for p in params:
                    if p.get("name") == name:
                        p["value"] = float(value)
                        vertex.setProperty("parameters", params)
                        break
        except Exception:
            pass

    @QtCore.Slot()
    def _on_reset(self) -> None:
        v = self._vertex
        for h in list(getattr(v.connections, "inp", [])) + list(getattr(v.connections, "out", [])):
            h.setProperty("timeseries", [])
            h.setProperty("interp", "linear")
        for p in (v.property("parameters") or []):
            p["timeseries"] = []
            p["interp"] = "linear"
        self._update_tree()
        self._plot_series()

    def exec(self) -> int:
        self._update_tree()
        self._plot_series()
        return super().exec()