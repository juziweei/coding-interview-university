"""实验报告出图适配器。

优先级：
1) 若可用 Origin COM，则走 Origin。
2) 若 Origin 不可用，则自动使用 matplotlib 出图（无需外部软件）。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class RenderResult:
    image_path: Path
    caption: str
    ok: bool
    message: str


class OriginAdapter:
    def render_figures(
        self,
        data_file: Path,
        figure_specs: list[dict[str, Any]],
        output_dir: Path,
    ) -> list[RenderResult]:
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            return self._render_with_origin(data_file, figure_specs, output_dir)
        except Exception as origin_exc:
            try:
                return self._render_with_matplotlib(data_file, figure_specs, output_dir)
            except Exception as mpl_exc:
                results: list[RenderResult] = []
                for i, spec in enumerate(figure_specs, start=1):
                    name = spec.get("name", f"figure_{i}")
                    fake_path = output_dir / f"{name}.png"
                    results.append(
                        RenderResult(
                            image_path=fake_path,
                            caption=spec.get("caption", name),
                            ok=False,
                            message=(
                                "Origin 与 matplotlib 都不可用，未实际出图："
                                f"Origin={origin_exc}; matplotlib={mpl_exc}"
                            ),
                        )
                    )
                return results

    def _render_with_origin(
        self,
        data_file: Path,
        figure_specs: list[dict[str, Any]],
        output_dir: Path,
    ) -> list[RenderResult]:
        raise RuntimeError("当前环境未配置 Origin COM 自动化")

    def _render_with_matplotlib(
        self,
        data_file: Path,
        figure_specs: list[dict[str, Any]],
        output_dir: Path,
    ) -> list[RenderResult]:
        import matplotlib.pyplot as plt
        import pandas as pd

        df = pd.read_csv(data_file)
        results: list[RenderResult] = []

        for i, spec in enumerate(figure_specs, start=1):
            name = spec.get("name", f"figure_{i}")
            caption = spec.get("caption", name)
            fig_type = spec.get("type", "line")
            x_col = spec.get("x")
            y_col = spec.get("y")
            out_path = output_dir / f"{name}.png"

            if x_col not in df.columns or y_col not in df.columns:
                results.append(
                    RenderResult(
                        image_path=out_path,
                        caption=caption,
                        ok=False,
                        message=f"列不存在：x={x_col}, y={y_col}",
                    )
                )
                continue

            plt.figure(figsize=(7, 4.5))
            if fig_type == "scatter":
                plt.scatter(df[x_col], df[y_col])
            else:
                plt.plot(df[x_col], df[y_col], marker="o")
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title(caption)
            plt.tight_layout()
            plt.savefig(out_path, dpi=160)
            plt.close()

            results.append(
                RenderResult(
                    image_path=out_path,
                    caption=caption,
                    ok=True,
                    message="使用 matplotlib 成功出图（无需 Origin）。",
                )
            )

        return results
