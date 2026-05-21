# 中文图类型对照表

这个表给小白用户使用：先看中文图名，再找到英文 API 和当前 skill 里的推荐 demo。

| 中文图名 | 常见英文/API | 推荐 demo | 适用场景 |
|---|---|---|---|
| 折线图 | `plot`, `lineplot` | `demo_line_plot.py`, `demo_matplotlib_relation_gallery.py` | 时间历程、收敛曲线、趋势对比 |
| 时域响应对比图 | `plot` | `demo_validation_compare.py`, `demo_hb_fig14_three_column.py` | 实验/仿真/辨识响应对比 |
| 一排三列响应图 | `subplots(1, 3)` | `demo_hb_fig14_three_column.py` | 论文 Fig. 14 风格响应对比 |
| 局部放大图 | inset axes | `demo_validation_inset_zoom.py` | 峰值、瞬态、共振附近细节 |
| 散点图 | `scatter`, `scatterplot` | `demo_matplotlib_relation_gallery.py`, `demo_seaborn_common_gallery.py` | 特征关系、残差结构、嵌入可视化 |
| 误差棒图 | `errorbar`, `pointplot` | `demo_matplotlib_relation_gallery.py`, `demo_seaborn_common_gallery.py` | 重复试验均值和不确定性 |
| 置信带图 | `fill_between`, `lineplot(errorbar=...)` | `demo_matplotlib_relation_gallery.py`, `demo_seaborn_common_gallery.py` | 均值响应和置信区间 |
| 柱状图 | `bar`, `barplot` | `demo_bar_llm_performance.py`, `demo_matplotlib_categorical_gallery.py`, `demo_seaborn_common_gallery.py` | 方法对比、消融实验 |
| 水平柱状图 | `barh` | `demo_matplotlib_categorical_gallery.py` | 特征重要性、排序比较 |
| 箱线图 | `boxplot` | `demo_error_boxplot.py`, `demo_matplotlib_distribution_gallery.py`, `demo_seaborn_common_gallery.py` | 误差分布、重复试验统计 |
| 小提琴图 | `violinplot` | `demo_matplotlib_distribution_gallery.py`, `demo_seaborn_common_gallery.py` | 分布形状比较 |
| 直方图 | `hist`, `histplot` | `demo_matplotlib_distribution_gallery.py`, `demo_seaborn_common_gallery.py` | 样本分布、误差分布 |
| KDE 密度图 | `kdeplot` | `demo_kde_uncertainty.py`, `demo_ml_residual_kde.py`, `demo_seaborn_common_gallery.py` | 后验密度、不确定性、残差分布 |
| ECDF 累积分布图 | `ecdfplot` | `demo_matplotlib_distribution_gallery.py`, `demo_seaborn_common_gallery.py` | 避免直方图分箱选择的分布比较 |
| 热力图 | `imshow`, `pcolormesh`, `heatmap` | `demo_ml_hyperparameter_heatmap.py`, `demo_seaborn_common_gallery.py` | 相关矩阵、混淆矩阵、参数扫描 |
| 混淆矩阵 | `imshow`, `heatmap` | `demo_ml_confusion_matrix.py` | 分类模型评价 |
| 等高线图 | `contour`, `contourf` | `demo_matplotlib_field_gallery.py` | 响应面、参数场 |
| 时频图 | `pcolormesh`, spectrogram | `demo_time_frequency_map.py` | 转速变化、频率能量随时间变化 |
| 频响图 | FRF line plot | `demo_frf_compare.py` | 频率响应函数对比 |
| 矢量场图 | `quiver`, `streamplot` | `demo_matplotlib_field_gallery.py` | 动力学流场、方向场 |
| 3D 曲面图 | `plot_surface`, `plot_wireframe` | `demo_matplotlib_3d_surface.py` | 参数响应面、三维场 |
| 相图/Poincare 图 | phase plot, Poincare map | `demo_phase_poincare.py` | 非线性动力学状态分析 |
| 分岔图 | bifurcation diagram | `demo_bifurcation_diagram.py` | 参数变化下的稳定性/周期变化 |
| 吸引域图 | basin of attraction | `demo_basin_attraction.py` | 非线性系统吸引域分析 |
| ROC/PR 曲线 | ROC, precision-recall | `demo_ml_classification_curves.py` | 分类模型评价 |
| 特征重要性图 | feature importance | `demo_ml_feature_importance.py` | 模型解释和变量筛选 |
| 雷达图 | radar chart | `demo_ml_radar_chart.py` | 多指标紧凑汇总，谨慎用于正文 |

## 选择规则

- 如果目标是最终论文排版，优先选 Matplotlib demo。
- 如果数据已经是带分组列的表格，优先选 Seaborn demo。
- 如果不知道选哪个，先运行：

```bash
python scripts/scimplstyle_mssp_cli.py recommend "你的目标" --lang zh
```
