# Codex Beginner Guide

Use this guide when the user is new to Codex skills, new to Matplotlib templates, or asks how to start.

## Goal

Help the user finish one small plotting task first, then gradually move to figure classification and reusable paper-template building.

## Three Levels

| Level | User need | Codex action | Output |
|---|---|---|---|
| Level 1 | "I have figures. What are they?" | Audit exported images and classify them by manuscript role. | Markdown inventory plus recommended figure categories. |
| Level 2 | "I want a similar style." | Copy or create the closest demo in a project run folder. | Runnable `.py` script and PNG output with placeholder data. |
| Level 3 | "I want to regenerate my paper figure." | Replace demo placeholder arrays with real project data. | Project-specific plotting script and regenerated figure. |

## Beginner Prompt Templates

### Start with an audit

```text
Use $sci-paper-plot-skill. I am a beginner. Please inspect my paper figure folder, classify the figures, and tell me which demos are closest. Do not edit original files.
```

### Create a first demo

```text
Use $sci-paper-plot-skill. I am a beginner. Please create a runnable demo in my current workspace for a one-row three-column time-response figure like Fig. 14.
```

### Convert a reference paper into templates

```text
Use $sci-paper-plot-skill. I want this skill to learn a new reference paper. Please audit the paper figures, add a figure-category map, and create reusable demo templates.
```

### Regenerate with real data

```text
Use $sci-paper-plot-skill. Please adapt the closest demo to my CSV/TXT/NPY data and save the script and PNG output in my project folder.
```

## Which Template Should I Choose? / 我该选哪个模板？

| If your goal is... | Start from... | Why this is easier |
|---|---|---|
| Check what figures you already have / 先看已有图片属于什么类型 | `python scripts/scimplstyle_mssp_cli.py audit "<paper-figure-folder>" --markdown` | You get a figure inventory before changing anything. / 不改原图，先得到图片清单。 |
| See all available examples / 看当前有哪些可用示例 | `python scripts/scimplstyle_mssp_cli.py list-demos` | It shows the real demo files installed in the skill. / 看到真实存在的 demo 文件。 |
| Get a beginner menu / 我不知道该选哪个图 | `python scripts/scimplstyle_mssp_cli.py beginner-guide` | It maps user goals to templates without requiring API knowledge. / 不需要先懂 API，按目标找模板。 |
| Recreate a one-row three-column response plot / 复刻一排三列响应图 | `demo_hb_fig14_three_column.py` | It is the most direct template for Fig. 14-style comparison. / 最接近 Fig. 14 风格。 |
| Make common Matplotlib manuscript figures / 画常见 Matplotlib 论文图 | `demo_matplotlib_relation_gallery.py`, `demo_matplotlib_distribution_gallery.py`, `demo_matplotlib_categorical_gallery.py`, `demo_matplotlib_field_gallery.py` | These are best for final paper figures with precise layout control. / 适合最终论文图排版。 |
| Make common Seaborn grouped plots / 画常见 Seaborn 分组统计图 | `demo_seaborn_common_gallery.py` | It is best when your data is already a tidy `DataFrame`. / 适合已有表格数据。 |
| Plot ML evaluation results / 画机器学习评价结果 | `demo_ml_classification_curves.py`, `demo_ml_confusion_matrix.py`, `demo_ml_feature_importance.py` | These cover common model-comparison and evaluation figures. / 覆盖常见模型对比图。 |

## Codex Workflow For Beginners

1. Confirm the target folder exists.
2. Run an audit before editing anything.
3. Tell the user the figure categories in simple language.
4. Pick one figure type first, not the whole paper.
5. Copy or write the demo into the user's workspace.
6. Generate a PNG and inspect it.
7. Only then replace placeholder data with real project data.

## What Codex Should Avoid

- Do not write generated figures into the installed skill folder.
- Do not edit original notebooks before the user asks for regeneration.
- Do not copy private paper data into the skill package.
- Do not treat all line plots as the same template; use manuscript role and axis meaning.
- Do not create many new abstractions before one runnable example works.

## Recommended Beginner Answer Style

When explaining to a new user:

- Start with the purpose of the next step.
- Give one runnable command or one prompt.
- Explain what output to expect.
- Offer Level 1, Level 2, and Level 3 as increasing options.
- Report absolute paths for generated scripts and outputs.
- If the user says they do not know which plot type to choose, run or summarize `python scripts/scimplstyle_mssp_cli.py beginner-guide` first.
