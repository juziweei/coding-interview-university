from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from origin_adapter import OriginAdapter


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def infer_basic_figures(data_header: list[str]) -> list[dict[str, Any]]:
    if len(data_header) >= 2:
        return [
            {
                "name": f"{data_header[0]}_{data_header[1]}_curve",
                "caption": f"{data_header[0]}-{data_header[1]} 曲线",
                "type": "line",
                "x": data_header[0],
                "y": data_header[1],
            }
        ]
    return []


def detect_csv_header(data_file: Path) -> list[str]:
    first_line = read_text(data_file).strip().splitlines()[0]
    return [h.strip() for h in first_line.split(",") if h.strip()]


def build_sections(title: str, lecture_text: str, data_file: Path) -> list[str]:
    return [
        f"# {title}",
        "",
        "## 1. 实验目的",
        "基于讲义要求，完成实验并分析结果。",
        "",
        "## 2. 实验原理",
        lecture_text.strip()[:2400] if lecture_text.strip() else "（待补充）",
        "",
        "## 3. 实验数据",
        f"原始数据文件：`{data_file}`",
        "",
        "## 4. 结果与分析",
        "根据图表结果，对趋势、误差来源和可能机理进行分析。",
        "",
        "## 5. 结论",
        "总结主要实验结论，并给出改进建议。",
        "",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="实验报告生成器（可直接运行）")
    parser.add_argument("--title", required=True)
    parser.add_argument("--lecture", type=Path, required=True)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--fig-config", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fig-dir", type=Path, required=True)
    args = parser.parse_args()

    lecture_text = read_text(args.lecture)

    if args.fig_config:
        fig_specs = json.loads(read_text(args.fig_config))
    else:
        header = detect_csv_header(args.data)
        fig_specs = infer_basic_figures(header)

    sections = build_sections(args.title, lecture_text, args.data)

    adapter = OriginAdapter()
    results = adapter.render_figures(args.data, fig_specs, args.fig_dir)

    sections.append("## 6. 图表")
    sections.append("")
    if not results:
        sections.append("（未识别到可绘制图表，请提供 --fig-config）")
        sections.append("")

    for r in results:
        sections.append(f"### {r.caption}")
        sections.append(f"![{r.caption}]({r.image_path.as_posix()})")
        if not r.ok:
            sections.append(f"> 警告：{r.message}")
        sections.append("")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(sections), encoding="utf-8")
    print(f"Report generated: {args.output}")


if __name__ == "__main__":
    main()
