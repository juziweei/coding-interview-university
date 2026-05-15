# 实验报告生成工具（可直接用）

你要的体验是：**在 Codex 聊天里给“讲义 + 数据”，就能自动生成实验报告并带图**。

这个目录提供两种用法：

1. **聊天框直接用（推荐）**：把讲义文本和数据文件发给我，我直接为你生成完整报告内容。
2. **本地一键命令用**：运行脚本自动生成 Markdown 报告并自动绘图（默认用 matplotlib，无需 Origin）。

---

## A. 聊天框直接用（最符合你的需求）

你下次直接按这个模板发我：

- 报告标题：
- 课程/实验名称：
- 讲义内容（可粘贴全文或重点）：
- 实验数据文件（csv/xlsx）：
- 你要的图（可选，不写我自动判断）：例如“温度-速率曲线、拟合图、误差棒图”
- 额外要求：例如“结论300字内、按学校模板、中文学术语气”

我会在聊天里直接返回：
- 完整报告（目的/原理/步骤/数据处理/结果分析/结论）
- 图表说明
- 可保存为 `.md` / `.docx` 的结构化文本

---

## B. 命令行直接生成（无需外部软件）

```bash
python3 extras/report_tool/report_builder.py \
  --title "实验报告：温度与反应速率" \
  --lecture extras/report_tool/examples/lecture.md \
  --data extras/report_tool/examples/data.csv \
  --output extras/report_tool/examples/output_report.md \
  --fig-dir extras/report_tool/examples/figures
```

说明：
- `--fig-config` 可省略；省略时会按 CSV 前两列自动生成基础曲线图。
- 若你提供 `--fig-config`，可精确控制图类型和列映射。

---

## C. Origin 支持说明

当前实现策略：
- 优先尝试 Origin（可在 `origin_adapter.py` 中补 COM 自动化细节）。
- 如果 Origin 不可用，自动回退到 matplotlib 出图，保证工具可直接运行。

这意味着你**现在就能用**，不被 Origin 环境阻塞。
