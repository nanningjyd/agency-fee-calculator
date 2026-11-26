# Agency Fee Calculator / 代理服务费计算器

一个用于计算招标代理服务费的桌面小工具，同时输出 **计价格〔2002〕1980号** 与 **桂建标〔2018〕37号** 两套结果，并附带普通计算器。

A desktop utility for calculating bidding agency service fees. It produces results under both **Jijia Price [2002] No. 1980** and **Guijianbiao [2018] No. 37** simultaneously, and includes a general-purpose calculator.

---

## 目录 / Table of Contents

- [功能特性 / Features](#功能特性--features)
- [计费依据 / Fee Basis](#计费依据--fee-basis)
- [使用方法 / Usage](#使用方法--usage)
- [普通计算器 / General Calculator](#普通计算器--general-calculator)
- [文件说明 / Files](#文件说明--files)
- [从源码构建 / Build from Source](#从源码构建--build-from-source)
- [已知差异与免责声明 / Known Differences & Disclaimer](#已知差异与免责声明--known-differences--disclaimer)
- [许可证 / License](#许可证--license)

---

## 功能特性 / Features

| 中文 | English |
| --- | --- |
| 一次输入中标金额，左右并排显示 1980 号与 2018 号两套计算结果 | Enter the winning bid amount once; 1980 and 2018 results are shown side by side |
| 支持货物招标、服务招标、工程招标三种类型 | Supports goods, services, and construction bidding |
| 支持“万元 / 元”单位切换，输入输出单位同步 | Supports switching between 10,000 CNY and CNY, with synchronized input/output units |
| 粘贴金额时自动去除逗号、空格与货币后缀 | Automatically strips commas, spaces, and currency suffixes when pasting amounts |
| 支持下浮系数 | Supports a discount (markdown) coefficient |
| 窗口可拖拽缩放，输入框与结果框同步拉伸 | Resizable window; input and result boxes stretch together |
| 双击边框按结果内容自适应不换行显示，再次双击恢复 | Double-click the border to auto-fit results without wrapping; double-click again to restore |
| 普通计算器支持键盘输入、按键字号无级调节、两行显示 | General calculator supports keyboard input, stepless key-font sizing, and a two-line display |

---

## 计费依据 / Fee Basis

### 1. 计价格〔2002〕1980号 / Jijia Price [2002] No. 1980

依据《招标代理服务费管理暂行办法》，采用**差额定率累进计费**，7 档，费率单位为 %。

Based on the *Interim Measures for the Administration of Bidding Agency Service Fees*, using **progressive tiered rates** across 7 brackets (unit: %).

| 类型 / Type | 费率（由低到高）/ Rates (low to high) |
| --- | --- |
| 货物招标 / Goods | 1.5 / 1.1 / 0.8 / 0.5 / 0.25 / 0.05 / 0.01 % |
| 服务招标 / Services | 1.5 / 0.8 / 0.45 / 0.25 / 0.1 / 0.05 / 0.01 % |
| 工程招标 / Construction | 1.0 / 0.7 / 0.55 / 0.35 / 0.2 / 0.05 / 0.01 % |

分档区间（万元）：0–100、100–500、500–1000、1000–5000、5000–10000、10000–100000、100000 以上。

Brackets (in 10,000 CNY): 0–100, 100–500, 500–1000, 1000–5000, 5000–10000, 10000–100000, above 100000.

### 2. 桂建标〔2018〕37号 / Guijianbiao [2018] No. 37

依据《自治区住房城乡建设厅关于颁布2018年〈广西壮族自治区工程建设其他费用定额〉的通知》**表三「招标代理服务费市场参考费率表」**，10 档，费率单位为 ‰。

Based on **Table 3 "Market Reference Rate Table for Bidding Agency Service Fees"** from the *Notice of the Guangxi Zhuang Autonomous Region Department of Housing and Urban-Rural Development on Promulgating the 2018 Quota for Other Construction Costs in Guangxi*, using 10 brackets (unit: ‰).

| 类型 / Type | 费率（由低到高）/ Rates (low to high) |
| --- | --- |
| 货物招标 / Goods | 9.45 / 6.93 / 5.04 / 3.15 / 1.575 / 0.315 / 0.221 / 0.05 / 0.038 / 0.025 ‰ |
| 服务招标 / Services | 9.45 / 5.04 / 2.835 / 1.575 / 0.63 / 0.315 / 0.221 / 0.05 / 0.038 / 0.025 ‰ |
| 工程招标 / Construction | 6.3 / 4.41 / 3.465 / 2.205 / 1.26 / 0.315 / 0.221 / 0.05 / 0.038 / 0.025 ‰ |

分档区间（万元）：0–100、100–500、500–1000、1000–5000、5000–10000、10000–50000、50000–100000、100000–500000、500000–1000000、1000000 以上。

Brackets (in 10,000 CNY): 0–100, 100–500, 500–1000, 1000–5000, 5000–10000, 10000–50000, 50000–100000, 100000–500000, 500000–1000000, above 1000000.

> 该结果**不含**编制工程量清单和招标控制价的费用。
> The 2018 result **excludes** fees for preparing the bill of quantities and bid ceiling price.

---

## 使用方法 / Usage

1. 双击 `服务费计算器_增强版.exe` 启动程序（无需安装 Python）。
   Double-click `服务费计算器_增强版.exe` to start (no Python installation required).

2. 在“请输入业务的中标金额”中填写金额，选择单位（万元或元）与服务类型（货物 / 服务 / 工程）。
   Enter the winning bid amount, select the unit (10,000 CNY or CNY) and the bidding type (goods / services / construction).

3. 如需下浮，在“下浮系数”中填写百分数（例如 20 表示下浮 20%）。
   If a discount applies, enter the percentage in the "discount" field (e.g. 20 means 20% off).

4. 点击“确定”或按回车，左右两侧分别显示 1980 号与 2018 号的计算明细与合计。
   Click "OK" or press Enter; the left and right panes show the 1980 and 2018 breakdowns and totals.

5. 点击“退出”关闭程序。
   Click "Exit" to close the program.

**显示说明 / Display notes**

- 万元单位：金额保留 6 位小数；元单位：金额保留 2 位小数。
  In 10,000-CNY mode amounts use 6 decimal places; in CNY mode, 2 decimal places.
- 窗口可自由拖拽改变宽度；双击窗口边框可让结果按内容宽度展开、不换行显示，再次双击恢复原尺寸。
  Drag the window edge to resize; double-click the border to expand results to their full content width without wrapping, and double-click again to restore the previous size.

---

## 普通计算器 / General Calculator

点击主界面的“普通计算器”按钮，或切换到“普通计算器”页签。

Click the "General Calculator" button on the main screen, or switch to the "General Calculator" tab.

- **两行显示**：上行显示前一次计算结果（算式 = 结果），下行显示当前输入的数字与运算符号。
  **Two-line display**: the upper line shows the previous result (expression = result), the lower line shows the current input and operators.
- **键盘输入**：支持数字、小数点、`+ - * /`、回车（等于）、退格、Esc（清除）、`%`、`F9`（正负号）；主键盘与小键盘均可用。
  **Keyboard input**: digits, decimal point, `+ - * /`, Enter (equals), Backspace, Esc (clear), `%`, and `F9` (sign toggle); both main keyboard and numpad work.
- **按键字号**：拖动底部“按键字号”滑块，可在 8–32 pt 之间无级调节，窗口会自动增高以容纳大字号。
  **Key font size**: drag the "Key Font Size" slider at the bottom to adjust steplessly from 8 to 32 pt; the window grows automatically to fit larger keys.

---

## 文件说明 / Files

| 文件 / File | 说明 / Description |
| --- | --- |
| `服务费计算器_增强版.py` | 程序源码，基于 PySide6 / Source code, based on PySide6 |
| `服务费计算器_增强版.exe` | Windows 单文件可执行程序（约 45 MB）/ Windows single-file executable (~45 MB) |
| `桂建标[2018]37号.png` | 费率依据文件截图（表三）/ Screenshot of the rate source (Table 3) |
| `桂建标〔2018〕37号_广西壮族自治区工程建设其他费用定额.docx` | 费率依据文档 / Source document for the rates |
| `服务费计算器.exe` | 原始 VB6 计算器（计价格〔2002〕1980号）/ Original VB6 calculator |

> .exe 体积约 45 MB 是因为 PyInstaller 将 Python 解释器与 Qt 运行库一并打包；原始 48 KB 的 VB6 程序依赖系统自带的 `MSVBVM60.DLL`。
> The ~45 MB size is because PyInstaller bundles the Python interpreter and Qt runtime. The original 48 KB VB6 program relies on the system-provided `MSVBVM60.DLL`.

---

## 从源码构建 / Build from Source

需要 Python 3.8+，并安装依赖：

Requires Python 3.8+ with the following dependencies:

```bash
pip install PySide6 pyinstaller
```

运行程序 / Run the program:

```bash
python 服务费计算器_增强版.py
```

打包为单文件 exe / Build a single-file executable:

```bash
pyinstaller --onefile --windowed --clean --name 服务费计算器_增强版 服务费计算器_增强版.py
```

构建产物位于 `dist/` 目录。
The output is located in the `dist/` directory.

---

## 已知差异与免责声明 / Known Differences & Disclaimer

- 原始 VB6 计算器在 10000 万元以上的分档中存在笔误（公式中多写一个 0）。本程序按 1980 号文的标准分档计算，未照抄该笔误。
  The original VB6 calculator contains a typo in the bracket above 10,000 (an extra zero in the formula). This program follows the standard brackets of the 1980 document rather than reproducing that typo.
- 桂建标〔2018〕37号的费率取自表三「市场参考费率表」。实际收费应以当地主管部门规定及合同约定为准。
  The [2018] No. 37 rates are taken from Table 3 (Market Reference Rate Table). Actual fees should follow local authority rules and contractual agreements.
- 本程序仅供估算参考，不构成法律或造价咨询意见。使用前请核对最新文件与当地规定。
  This tool is for estimation only and does not constitute legal or cost-consulting advice. Please verify against the latest official documents and local regulations before use.

---

## 许可证 / License

MIT License — 详见 [LICENSE](LICENSE)。/ See [LICENSE](LICENSE) for details.
