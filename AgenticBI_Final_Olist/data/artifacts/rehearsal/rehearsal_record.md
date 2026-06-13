# 端到端演示彩排记录

## 彩排目标

按分工清单 D7 要求，覆盖“初始化 → 刷新视图 → 启动 Web → 3 个典型问题 → 截图/备用视频”的完整路径。

## 环境准备

- Python：本机优先使用 `C:\Users\21125\AppData\Local\Programs\Python\Python313\python.exe`
- 数据库：MySQL 8.x，本地库 `olist_agentic_bi`
- 原始数据：`data/raw/` 下 9 个 Olist CSV
- 环境变量：可复制 `.env.example` 为 `.env`

## 彩排命令

```bash
python -m utils.db_init
python -m utils.refresh_views
python -m utils.perf_compare
streamlit run dashboard/app.py
```

Dashboard 启动时会调用 `utils.startup_check.ensure_views_ready(auto_refresh=True)`，如果预聚合视图缺失，会自动刷新。

## 三个现场演示问题

1. `2017年哪个州的销售额最高？交付准时率是多少？哪种支付方式最受欢迎？`
   - 展示点：多视图联合命中；`mv_state_sales`、`mv_delivery_perf`、`mv_payment_dist`。
2. `为什么某些州的平均配送时长显著高于全国均值？哪些卖家的差评率最高？`
   - 展示点：诊断下钻；配送全国均值对比 + `mv_seller_perf`。
3. `如果将 Top 20 高差评卖家的商品统一下架，平台整体评分预估提升多少？`
   - 展示点：What-if 加分功能；评分提升与业务风险说明。

## 截图与素材

- 架构图：`docs/architecture.png`
- 性能图：`data/artifacts/perf/perf_compare_chart.png`
- Demo 图表：`data/artifacts/demo/*.png`
- 备用视频：`data/artifacts/rehearsal/demo_rehearsal.mp4`

## 讲解节奏

- 0:00-1:00 背景、数据与挑战
- 1:00-2:30 架构与预聚合加速
- 2:30-5:30 三个现场问题演示
- 5:30-7:30 可视化、预测、NLP、What-if、异常检测
- 7:30-9:30 技术挑战与运营策略
- 9:30-10:00 总结与答疑入口
