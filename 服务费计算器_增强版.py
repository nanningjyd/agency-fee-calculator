# -*- coding: utf-8 -*-
"""服务费计算器增强版
- 一次输入，同时输出 计价格〔2002〕1980号 与 桂建标〔2018〕37号 两套计算结果
- 2018 项下费率采用桂建标〔2018〕37号 表三“招标代理服务费市场参考费率表”（单位‰）
- 附带普通计算器按钮与页签
"""

import sys
from PySide6 import QtCore, QtWidgets

# 计价格〔2002〕1980号：7 档，单位 %
TIERS_1980 = [0, 100, 500, 1000, 5000, 10000, 100000, float("inf")]

# 桂建标〔2018〕37号 表三：10 档，单位 ‰
TIERS_2018 = [0, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000, float("inf")]

RATES_1980 = {
    "货物招标": [0.015, 0.011, 0.008, 0.005, 0.0025, 0.0005, 0.0001],
    "服务招标": [0.015, 0.008, 0.0045, 0.0025, 0.001, 0.0005, 0.0001],
    "工程招标": [0.01, 0.007, 0.0055, 0.0035, 0.002, 0.0005, 0.0001],
}

# 桂建标〔2018〕37号 表三 招标代理服务费市场参考费率表（‰ 转小数）
RATES_2018 = {
    "货物招标": [0.00945, 0.00693, 0.00504, 0.00315, 0.001575,
                 0.000315, 0.000221, 0.00005, 0.000038, 0.000025],
    "服务招标": [0.00945, 0.00504, 0.002835, 0.001575, 0.00063,
                 0.000315, 0.000221, 0.00005, 0.000038, 0.000025],
    "工程招标": [0.0063, 0.00441, 0.003465, 0.002205, 0.00126,
                 0.000315, 0.000221, 0.00005, 0.000038, 0.000025],
}

def fmt(value):
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return ("%.8f" % value).rstrip("0").rstrip(".")


def rate_text_pct(rate):
    return ("%.5f" % rate).rstrip("0").rstrip(".")


def rate_text_permille(rate):
    return ("%.3f" % (rate * 1000)).rstrip("0").rstrip(".") + "‰"


def clean_number(text):
    for ch in (",", "，", " ", "　", "\t", "\n"):
        text = text.replace(ch, "")
    for suffix in ("万元", "元", "¥", "￥"):
        if text.endswith(suffix):
            text = text[:-len(suffix)]
            break
    return text.strip()


def money(value, unit):
    return ("%.6f" % value) if unit == "万元" else ("%.2f" % value)


class CleanLineEdit(QtWidgets.QLineEdit):
    def paste(self):
        text = QtWidgets.QApplication.clipboard().text()
        if text:
            self.insert(clean_number(text))
        else:
            super().paste()


def calc_fee(amount, rates, tiers, formatter, scale, unit):
    lines = []
    total = 0.0
    for i in range(len(rates)):
        low, high = tiers[i], tiers[i + 1]
        if amount <= low:
            break
        part = min(amount, high) - low
        fee = part * rates[i]
        total += fee
        rate = formatter(rates[i])
        if i == 0:
            lines.append("%s* %s=%s%s"
                         % (money(part * scale, unit), rate, money(fee * scale, unit), unit))
        elif high == float("inf"):
            lines.append("%s以上 * %s = %s%s"
                         % (money(low * scale, unit), rate, money(fee * scale, unit), unit))
        else:
            lines.append("( %s - %s ) * %s = %s%s"
                         % (money(high * scale, unit), money(low * scale, unit),
                            rate, money(fee * scale, unit), unit))
        if amount <= high:
            break
    lines.append("合计收费=%s%s" % (money(total * scale, unit), unit))
    return lines, total


def with_discount(lines, total, discount, scale, unit):
    if discount:
        final = total * (1 - discount / 100.0)
        lines.append("下浮%s%%后的总金额为： %s * ( 1 - %s%% ) = %s%s"
                     % (fmt(discount), money(total * scale, unit),
                        fmt(discount), money(final * scale, unit), unit))
    return lines


class FeePanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.radios = {}
        self.build()

    def build(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(12, 10, 12, 10)
        root.setSpacing(7)

        amount_row = QtWidgets.QHBoxLayout()
        amount_row.addWidget(QtWidgets.QLabel("请输入业务的中标金额："))
        self.amount = CleanLineEdit()
        amount_row.addWidget(self.amount, 1)
        self.unit_wan = QtWidgets.QRadioButton("万元")
        self.unit_yuan = QtWidgets.QRadioButton("元")
        self.unit_group = QtWidgets.QButtonGroup(self)
        self.unit_group.addButton(self.unit_wan, 0)
        self.unit_group.addButton(self.unit_yuan, 1)
        self.unit_wan.setChecked(True)
        self.unit_wan.toggled.connect(self.on_unit_changed)
        self.unit_yuan.toggled.connect(self.on_unit_changed)
        amount_row.addWidget(self.unit_wan)
        amount_row.addWidget(self.unit_yuan)
        self.ok_btn = QtWidgets.QPushButton("确定")
        self.ok_btn.setFixedWidth(68)
        self.ok_btn.clicked.connect(self.on_calc)
        amount_row.addWidget(self.ok_btn)
        root.addLayout(amount_row)

        discount_row = QtWidgets.QHBoxLayout()
        discount_row.addWidget(QtWidgets.QLabel("下浮系数："))
        self.discount = QtWidgets.QLineEdit("0")
        discount_row.addWidget(self.discount, 1)
        discount_row.addWidget(QtWidgets.QLabel("%"))
        self.quit_btn = QtWidgets.QPushButton("退出")
        self.quit_btn.setFixedWidth(68)
        self.quit_btn.clicked.connect(QtWidgets.QApplication.instance().quit)
        discount_row.addWidget(self.quit_btn)
        root.addLayout(discount_row)

        type_row = QtWidgets.QHBoxLayout()
        type_row.addWidget(QtWidgets.QLabel("请选择服务类型："))
        self.type_group = QtWidgets.QButtonGroup(self)
        for key in ("货物招标", "服务招标", "工程招标"):
            rb = QtWidgets.QRadioButton(key)
            rb.setChecked(key == "货物招标")
            self.type_group.addButton(rb)
            self.radios[key] = rb
            type_row.addWidget(rb)
        type_row.addStretch(1)
        root.addLayout(type_row)

        tool_row = QtWidgets.QHBoxLayout()
        tool_row.addStretch(1)
        self.calc_btn = QtWidgets.QPushButton("普通计算器")
        btn_font = self.calc_btn.font()
        btn_font.setPointSize(11)
        self.calc_btn.setFont(btn_font)
        self.calc_btn.setFixedWidth(108)
        self.calc_btn.setFixedHeight(30)
        tool_row.addWidget(self.calc_btn)
        root.addLayout(tool_row)

        results = QtWidgets.QHBoxLayout()
        results.setSpacing(8)
        for title, attr, header_attr in (
            ("计价格〔2002〕1980号计算结果（单位：万元）", "output1980", "header1980"),
            ("桂建标〔2018〕37号计算结果（单位：万元）", "output2018", "header2018"),
        ):
            col = QtWidgets.QVBoxLayout()
            header = QtWidgets.QLabel(title)
            header.setStyleSheet(
                "background:#e8f0fa;color:#185fa5;border:1px solid #a9c6e8;"
                "padding:2px 6px;font-size:12px;"
            )
            out = QtWidgets.QTextEdit()
            out.setReadOnly(True)
            out.setMinimumHeight(150)
            out.setMinimumWidth(240)
            col.addWidget(header)
            col.addWidget(out)
            setattr(self, header_attr, header)
            setattr(self, attr, out)
            results.addLayout(col, 1)
        root.addLayout(results, 1)

        self.note = QtWidgets.QLabel(
            "注：桂建标〔2018〕37号结果按表三“招标代理服务费市场参考费率表”计算，"
            "费率单位‰，差额定率分档累进；该费用不含编制工程量清单和招标控制价费用。"
        )
        self.note.setWordWrap(True)
        self.note.setStyleSheet("color:#666;font-size:11px;")
        root.addWidget(self.note)

        self.amount.returnPressed.connect(self.on_calc)
        self.discount.returnPressed.connect(self.on_calc)

    def current_type(self):
        for name, rb in self.radios.items():
            if rb.isChecked():
                return name
        return "货物招标"

    def current_unit(self):
        return "元" if self.unit_yuan.isChecked() else "万元"

    def on_unit_changed(self, checked=None):
        unit = self.current_unit()
        self.header1980.setText("计价格〔2002〕1980号计算结果（单位：%s）" % unit)
        self.header2018.setText("桂建标〔2018〕37号计算结果（单位：%s）" % unit)
        if self.output1980.toPlainText() and not self.output1980.toPlainText().startswith("请输入"):
            self.on_calc()

    def on_calc(self):
        raw = clean_number(self.amount.text())
        self.amount.setText(raw)
        try:
            entered = float(raw)
        except ValueError:
            self.output1980.setPlainText("请输入有效的中标金额！")
            self.output2018.setPlainText("请输入有效的中标金额！")
            return
        if entered <= 0:
            self.output1980.setPlainText("中标金额必须大于 0！")
            self.output2018.setPlainText("中标金额必须大于 0！")
            return
        try:
            discount = float(self.discount.text() or 0)
        except ValueError:
            self.output1980.setPlainText("下浮系数必须是数字！")
            self.output2018.setPlainText("下浮系数必须是数字！")
            return
        if discount < 0 or discount >= 100:
            self.output1980.setPlainText("下浮系数应在 0 到 100 之间！")
            self.output2018.setPlainText("下浮系数应在 0 到 100 之间！")
            return

        unit = self.current_unit()
        scale = 10000.0 if unit == "元" else 1.0
        amount = entered / scale
        name = self.current_type()
        lines1980, total1980 = calc_fee(amount, RATES_1980[name], TIERS_1980,
                                        rate_text_pct, scale, unit)
        lines2018, total2018 = calc_fee(amount, RATES_2018[name], TIERS_2018,
                                        rate_text_permille, scale, unit)
        self.output1980.setPlainText("\n".join(with_discount(lines1980, total1980, discount, scale, unit)))
        self.output2018.setPlainText("\n".join(with_discount(lines2018, total2018, discount, scale, unit)))


class CalcPanel(QtWidgets.QWidget):
    fontChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.accum = 0.0
        self.op = None
        self.entry = "0"
        self.fresh = True
        self.last_line = ""     # 上行：前一次计算结果（算式 = 结果）
        self.tokens = []        # 下行：刚输入的数字、运算符号
        self.err = False
        self.buttons = []
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.build()

    def build(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(8)

        # 仿 Windows 计算器显示区：上行小字为前次结果，下行大字为当前输入
        screen = QtWidgets.QFrame()
        screen.setFrameShape(QtWidgets.QFrame.StyledPanel)
        screen.setStyleSheet(
            "QFrame { background:#ffffff; border:1px solid #8a8a8a; }"
        )
        screen_layout = QtWidgets.QVBoxLayout(screen)
        screen_layout.setContentsMargins(8, 6, 8, 6)
        screen_layout.setSpacing(2)
        self.history = QtWidgets.QLabel("")
        self.history.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.history.setStyleSheet("color:#808080;font-size:12px;")
        self.display = QtWidgets.QLabel("0")
        self.display.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self.display.setStyleSheet("color:#202020;font-size:30px;")
        screen_layout.addWidget(self.history)
        screen_layout.addWidget(self.display)
        root.addWidget(screen)

        labels = [
            ["C", "←", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="],
        ]
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(4)
        for r, row in enumerate(labels):
            for c, text in enumerate(row):
                btn = QtWidgets.QPushButton(text)
                btn.setFocusPolicy(QtCore.Qt.NoFocus)  # 数字键不被按钮焦点截获
                btn.setMinimumHeight(42)
                btn.clicked.connect(lambda checked=False, t=text: self.press(t))
                grid.addWidget(btn, r, c)
                self.buttons.append(btn)
        root.addLayout(grid)

        font_row = QtWidgets.QHBoxLayout()
        font_row.addWidget(QtWidgets.QLabel("按键字号："))
        self.font_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.font_slider.setRange(16, 64)   # 8~32pt，0.5pt 步进，连续可调
        self.font_slider.setValue(22)       # 默认 11pt
        self.font_slider.setSingleStep(1)
        self.font_slider.setPageStep(4)
        self.font_slider.valueChanged.connect(self.on_font_size_changed)
        font_row.addWidget(self.font_slider, 1)
        self.font_label = QtWidgets.QLabel("11 pt")
        self.font_label.setMinimumWidth(48)
        font_row.addWidget(self.font_label)
        root.addLayout(font_row)
        self.on_font_size_changed(self.font_slider.value())
        root.addStretch(1)

    def on_font_size_changed(self, value):
        pt = value / 2.0
        font = QtWidgets.QApplication.font()
        font.setPointSizeF(pt)
        for btn in self.buttons:
            btn.setFont(font)
            btn.setMinimumHeight(max(42, int(pt * 2.8) + 8))
        self.font_label.setText("%g pt" % pt)
        self.fontChanged.emit()

    def show_value(self):
        self.history.setText(self.last_line)
        self.display.setText(" ".join(self.tokens) if self.tokens else self.entry)

    OPS = ("+", "−", "×", "÷")

    def start_new(self):
        self.accum = 0.0
        self.op = None
        self.entry = "0"
        self.tokens = []
        self.last_line = ""
        self.fresh = True
        self.err = False

    def input_char(self, ch):
        # fresh=True：本次输入开启一个新的操作数；否则续接到当前操作数
        if self.err:
            self.start_new()
            self.fresh = True
        if self.fresh:
            if self.op is None:
                # 等号后或初始：从头开始新算式
                self.last_line = ""
                self.tokens = [ch]
                self.accum = 0.0
            else:
                # 刚按过运算符：保留前面的表达式与累积值
                if self.tokens and self.tokens[-1] in self.OPS:
                    self.tokens.append(ch)
                else:
                    self.tokens = [ch]
            self.entry = ch
            self.fresh = False
        else:
            self.entry = self.entry + ch
            if self.tokens and self.tokens[-1] not in self.OPS:
                self.tokens[-1] = self.entry
            else:
                self.tokens.append(self.entry)

    def press(self, key):
        if key.isdigit():
            self.input_char(key)
        elif key == ".":
            if self.fresh or self.err:
                self.input_char("0.")
            elif "." not in self.entry:
                self.input_char(".")
        elif key == "C":
            self.start_new()
        elif key == "←":
            if self.err:
                self.start_new()
            elif not self.fresh or self.op is None:
                self.entry = self.entry[:-1] or "0"
                if self.tokens and self.tokens[-1] not in self.OPS:
                    self.tokens[-1] = self.entry
                self.fresh = False
        elif key == "±":
            if self.err:
                self.start_new()
            else:
                if self.entry.startswith("-"):
                    self.entry = self.entry[1:]
                elif self.entry != "0":
                    self.entry = "-" + self.entry
                if self.tokens and self.tokens[-1] not in self.OPS:
                    self.tokens[-1] = self.entry
        elif key == "%":
            if self.err:
                self.start_new()
            else:
                self.entry = fmt(float(self.entry) / 100)
                self.fresh = True
                if self.tokens and self.tokens[-1] not in self.OPS:
                    self.tokens[-1] = self.entry
        elif key in self.OPS:
            if self.err:
                self.start_new()
            value = float(self.entry)
            if self.op is not None and not self.fresh:
                prev_expr = " ".join(self.tokens)
                value = self.apply(self.accum, value, self.op)
                if self.err:
                    self.show_value()
                    return
                self.last_line = "%s = %s" % (prev_expr, fmt(value))
            self.accum = value
            self.op = key
            self.entry = fmt(value)
            self.tokens = [self.entry, key]
            self.fresh = True
        elif key == "=":
            if self.err:
                self.start_new()
            elif self.op is not None:
                result = self.apply(self.accum, float(self.entry), self.op)
                if self.err:
                    self.show_value()
                    return
                self.last_line = "%s = %s" % (" ".join(self.tokens), fmt(result))
                self.entry = fmt(result)
                self.op = None
                self.accum = float(self.entry)
                self.tokens = []
                self.fresh = True
        self.show_value()

    def apply(self, a, b, op):
        if op == "+":
            return a + b
        if op == "−":
            return a - b
        if op == "×":
            return a * b
        if op == "÷":
            if b == 0:
                self.last_line = "%s = " % " ".join(self.tokens)
                self.entry = "无法除以零"
                self.tokens = [self.entry]
                self.accum = 0.0
                self.op = None
                self.fresh = True
                self.err = True
                return a
            return a / b
        return b

    def keyPressEvent(self, event):
        # 支持主键盘与小键盘：数字、小数点、+-*/、回车、退格、Esc、%、正负号
        mapping = {
            QtCore.Qt.Key_Plus: "+", QtCore.Qt.Key_Minus: "−",
            QtCore.Qt.Key_Asterisk: "×", QtCore.Qt.Key_Slash: "÷",
            QtCore.Qt.Key_Enter: "=", QtCore.Qt.Key_Return: "=",
            QtCore.Qt.Key_Equal: "=",
            QtCore.Qt.Key_Backspace: "←", QtCore.Qt.Key_Escape: "C",
            QtCore.Qt.Key_Delete: "C", QtCore.Qt.Key_Percent: "%",
            QtCore.Qt.Key_Period: ".", QtCore.Qt.Key_F9: "±",
        }
        key = mapping.get(event.key())
        text = event.text()
        if key is None:
            if text.isdigit():
                key = text
            elif text in (".", ","):
                key = "."
            elif text == "+":
                key = "+"
            elif text in ("-", "−"):
                key = "−"
            elif text in ("*", "×"):
                key = "×"
            elif text in ("/", "÷"):
                key = "÷"
            elif text == "%":
                key = "%"
        if key is not None:
            self.press(key)
            event.accept()
        else:
            super().keyPressEvent(event)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("服务费计算器")
        flags = self.windowFlags() & ~int(QtCore.Qt.WindowMaximizeButtonHint)
        flags |= QtCore.Qt.WindowCloseButtonHint
        flags |= QtCore.Qt.WindowMinimizeButtonHint
        flags |= QtCore.Qt.WindowSystemMenuHint
        self.setWindowFlags(flags)
        self.setMinimumSize(620, 440)
        self.resize(620, 440)
        self.expanded = False
        self.saved_geometry = None
        self.tabs = QtWidgets.QTabWidget()
        self.fee = FeePanel()
        self.tabs.addTab(self.fee, "代理服务费")
        self.calc = CalcPanel()
        self.tabs.addTab(self.calc, "普通计算器")
        self.calc.fontChanged.connect(self.on_calc_font_changed)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.fee.calc_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(1))
        self.fee.output1980.textChanged.connect(self.on_result_changed)
        self.fee.output2018.textChanged.connect(self.on_result_changed)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tabs)

    def on_tab_changed(self, index):
        # 切到普通计算器时把焦点交给面板，键盘输入直接可用
        if index == 1:
            self.calc.setFocus()

    def on_calc_font_changed(self):
        # 字号变大导致按钮放不下时，自动增高窗口；只在计算器页签激活时处理
        if self.tabs.currentIndex() != 1:
            return
        self.calc.layout().activate()
        needed = self.calc.minimumSizeHint().height() + 90  # 页签栏 + 窗口边框
        if self.height() < needed:
            self.resize(self.width(), needed)

    def event(self, ev):
        if ev.type() == QtCore.QEvent.NonClientAreaMouseButtonDblClick:
            if self.tabs.currentIndex() == 0:
                self.toggle_expand()
            return True  # 计算器页签下屏蔽双击边框，避免误改窗口尺寸
        return super().event(ev)

    def needed_size(self):
        widths = []
        heights = []
        for out in (self.fee.output1980, self.fee.output2018):
            fm = out.fontMetrics()
            lines = out.toPlainText().splitlines() or [""]
            widths.append(max(fm.horizontalAdvance(line) for line in lines) + 48)
            heights.append(max(len(lines), 1) * fm.height() + 24)
        content_width = max(widths) * 2 + 8 + 24
        height_delta = max(heights) - self.fee.output1980.height()
        return (max(self.minimumWidth(), content_width),
                max(self.minimumHeight(), self.height() + height_delta))

    def on_result_changed(self):
        if self.expanded:
            width, height = self.needed_size()
            self.resize(width, height)

    def toggle_expand(self):
        if not self.expanded:
            self.saved_geometry = self.geometry()
            self.fee.output1980.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
            self.fee.output2018.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
            width, height = self.needed_size()
            self.resize(width, height)
            self.expanded = True
        else:
            self.fee.output1980.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
            self.fee.output2018.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
            if self.saved_geometry is not None:
                self.setGeometry(self.saved_geometry)
            self.expanded = False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
