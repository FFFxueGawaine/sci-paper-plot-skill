# Sci Paper Plot Skill 中文指南

这是一个面向 SCI 论文绘图的 Codex skill。它解决的核心问题不是“画一张图”，而是把论文图片按功能分类，再沉淀成可复用、可运行、可迁移的绘图模板。

## 适合谁

- 不知道论文里的图属于哪种类型；
- 有参考论文图片，但不知道从哪个模板开始复刻；
- 想把 Matplotlib 或 Seaborn 图做成统一 SCI 风格；
- 想让 Codex 帮忙审计图片、推荐 demo、生成预览图册；
- 想把新论文的图逐步沉淀到 skill 里。

## 小白最快入口

先运行新手向导：

```bash
python scripts/scimplstyle_mssp_cli.py beginner-guide --lang zh
```

如果准备复制 demo、生成图册或运行绘图脚本，先打印运行前提示单：

```bash
python scripts/scimplstyle_mssp_cli.py run-brief --lang zh
```

如果已经知道大概需求，可以直接让推荐器选模板：

```bash
python scripts/scimplstyle_mssp_cli.py recommend "误差分布" --lang zh
python scripts/scimplstyle_mssp_cli.py recommend "时域响应 三列对比" --lang zh
python scripts/scimplstyle_mssp_cli.py recommend "热图 混淆矩阵" --lang zh
```

如果手里有一批论文图片，先审计：

```bash
python scripts/scimplstyle_mssp_cli.py audit "<论文图片文件夹>" --markdown
```

## 常见任务怎么选

| 你想做什么 | 推荐入口 |
|---|---|
| 看当前有哪些模板 | `python scripts/scimplstyle_mssp_cli.py list-demos` |
| 不知道选哪个模板 | `python scripts/scimplstyle_mssp_cli.py recommend "你的目标" --lang zh` |
| 运行前先问清楚需求 | `python scripts/scimplstyle_mssp_cli.py run-brief --lang zh` |
| 生成 demo 预览图册 | `python scripts/scimplstyle_mssp_cli.py preview-gallery "<输出文件夹>" --set curated` |
| 检查 demo 图片是否正常生成 | `python scripts/scimplstyle_mssp_cli.py check-demos "<输出文件夹>" --set curated` |
| 复制 demo 到项目目录 | `python scripts/scimplstyle_mssp_cli.py copy-demos "<项目绘图工作文件夹>"` |

## 当前覆盖的图类型

- Matplotlib 工程图：折线图、散点图、误差棒、置信带、柱状图、箱线图、小提琴图、直方图、等高线、热力图、矢量场、3D 曲面。
- Seaborn 统计图：`scatterplot`、`lineplot`、`regplot`、`histplot`、`kdeplot`、`boxplot`、`violinplot`、`barplot`、`heatmap`、`pairplot`、`relplot`、`catplot`、`displot`。
- 论文场景图：Fig. 14 风格一排三列响应图、FRF 对比、时频图、局部放大验证图、后验/KDE 不确定性图、机器学习评价图。

更完整的中文对照表见 `references/plot-type-map.zh-CN.md`。
详细新手路线见 `references/codex-beginner-guide.zh-CN.md`。
论文图片的布局、语言、字体和导出约束见 `references/figure-quality-constraints.zh-CN.md`。
运行绘图程序前的提问清单见 `references/pre-run-brief.zh-CN.md`。

## 推荐工作流

1. 先用 `beginner-guide --lang zh` 确认当前阶段。
2. 用 `run-brief --lang zh` 补齐运行前提示。
3. 用 `recommend` 根据目标选一个 demo。
4. 把 demo 复制到 skill 外部的项目文件夹。
5. 先用占位数据跑通 PNG。
6. 再把占位数据换成真实 CSV/TXT/NPY 数据。
7. 最后按论文要求调整标签、单位、图例和导出格式。

## 安全规则

- 不要把生成图写进已安装的 skill 文件夹。
- 不要第一步就改原始论文图片或 Notebook。
- 运行会写文件的程序前，先确认目标、数据、输出位置、语言字体、子图标号和版面约束。
- 不要一次复刻整篇论文，先完成一类图。
- 最终论文图优先 Matplotlib 精确排版；分组表格数据优先 Seaborn 快速探索。
- `(a)(b)(c)` 标号默认放上方居中；只有期刊模板或参考图明确要求时才放下方居中。
- 英文 SCI 标题默认 Times New Roman；中文报告标题可选宋体。
- 单位未知时直接不写单位，不要用 `(-)` 占位；只有明确无量纲时才写 `(-)`。
