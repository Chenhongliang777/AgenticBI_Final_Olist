# Agentic BI (Olist) 多智能体电商运营分析系统

本项目基于 Kaggle Olist 巴西电商多表数据集，构建一个 Agentic BI 多智能体分析与决策系统。系统将 9 张原始业务表加载到 MySQL，构建 Pre-Aggregation 预聚合加速层，并通过 LangGraph 编排 SQL 分析、可视化、NLP、预测、What-if、异常检测和决策 Agent。业务人员可以在 Streamlit Web 页面中使用自然语言提问，获得数据表、图表、趋势预测和运营建议。

## 功能概览

- 多智能体协作：Coordinator、SQL、Forecast、NLP、Viz、Decision、What-if、Anomaly。
- 预聚合加速：6 个核心业务物化视图 + 2 个地理辅助表。
- 多轮对话：LangGraph MemorySaver + 显式 conversation_history。
- 条件路由：描述性、诊断性、预测性、评论/NLP、What-if、异常检测按需触发。
- 可视化：GMV 趋势、州级销售、支付热力图、品类评分热力图、地理热力图、词云、散点/气泡等。
- 决策智能：综合 SQL、预测、NLP 与模拟结果，输出运营策略。

## 运行环境

- Python 3.10+，本机推荐 Python 3.13。
- MySQL 8.0+。
- Streamlit。
- DeepSeek API Key，可通过 `.env` 覆盖默认配置。

## 配置说明

复制环境变量模板：

```bash
copy .env.example .env
```

常用配置项：

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=olist_agentic_bi

DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-v4-pro
```

## 一键启动流程

在项目根目录执行：

```bash
pip install -r requirements.txt
python -m utils.db_init
python -m utils.refresh_views
streamlit run dashboard/app.py
```

Dashboard 启动时会自动调用 `utils.startup_check.ensure_views_ready(auto_refresh=True)`。如果预聚合视图缺失，系统会自动刷新；如果基础表缺失，会提示先运行 `python -m utils.db_init`。

## 常用命令

```bash
# 初始化数据库并加载 9 张 Olist 原始表
python -m utils.db_init

# 刷新 6 个业务物化视图 + 2 个地理辅助表
python -m utils.refresh_views

# 生成预聚合性能对比报告和截图
python -m utils.perf_compare

# 启动 Web 仪表板
streamlit run dashboard/app.py

# CLI 入口
python app.py
```

## 演示问题清单

1. `2017年 GMV 是多少？按月和各州排名的趋势怎样？`
2. `平台整体准时交付率是多少？哪些州延迟最严重？`
3. `哪种支付方式最受欢迎？平均分期数是多少？`
4. `产品的重量、尺寸与运费之间有什么关系？`
5. `Top 10 差评品类及其主要差评原因是什么？`
6. `根据历史订单趋势，预测未来6周的销售额，并给出趋势解读。`
7. `基于全部分析结果，给出平台3个月内的三大优先改进策略。`
8. `2017年哪个州的销售额最高？交付准时率是多少？哪种支付方式最受欢迎？`
9. `为什么某些州的平均配送时长显著高于全国均值？哪些卖家的差评率最高？`
10. `如何降低巴西东北部地区的高退货率？请给出具体的运营改进方案。`
11. `如果将 Top 20 高差评卖家的商品统一下架，平台整体评分预估提升多少？`
12. `最近哪些州出现了订单量骤降或差评率突升的异常？`

## 目录结构

```text
AgenticBI_Final_Olist/
├── agents/                       # 多 Agent 定义与 LangGraph 编排
├── config/                       # 数据字典、诊断 SQL
├── dashboard/                    # Streamlit Web UI
├── data/
│   ├── raw/                      # Olist 原始 CSV
│   └── artifacts/
│       ├── demo/                 # 可视化截图素材
│       ├── perf/                 # 性能对比图与报告
│       └── rehearsal/            # 彩排记录与备用视频
├── docs/
│   ├── 01_data.md
│   ├── 02_views.md
│   ├── 03_agents.md
│   ├── 04_qa_test.md
│   ├── 05_results.md
│   ├── architecture.png
│   ├── 项目报告.md
│   ├── 项目报告.docx
│   └── 项目报告.pdf
├── models/                       # 预测、NLP、What-if 模块
├── scripts/                      # D 阶段交付物生成脚本
├── utils/                        # 数据加载、清洗、预聚合、启动自检
├── app.py                        # CLI 入口
├── 答辩讲稿.txt
├── 提交清单.txt
├── requirements.txt
└── README.md
```

## 最终提交物

- 项目代码：`agents/`、`utils/`、`models/`、`dashboard/`、`config/`、`app.py`。
- 项目报告：`docs/项目报告.docx`、`docs/项目报告.pdf`。
- 架构图：`docs/architecture.png`。
- 答辩材料：`答辩PPT.pptx`、`答辩讲稿.txt`。
- 性能与演示素材：`data/artifacts/perf/`、`data/artifacts/demo/`、`data/artifacts/rehearsal/`。
- 提交说明：`提交清单.txt`。

## 小组分工与贡献比例

| 成员 | 职责 | 贡献比例 |
|---|---|---:|
| A | 数据清洗、数据库初始化、预聚合刷新、性能对比、数据与视图文档 | 25% |
| B | MemorySaver、多轮上下文、协调器任务分解、条件路由、诊断 SQL、视图策略 | 25% |
| C | 可视化补齐、NLP 情感、What-if、异常检测、附录问题测试、结果解读 | 25% |
| D | 架构图、最终报告、PPT、讲稿、README、彩排记录、提交清单 | 25% |

## 常见问题

**1. 启动 Dashboard 后提示基础表不存在怎么办？**  
先确认 `data/raw/` 下 9 个 CSV 文件齐全，再运行 `python -m utils.db_init`。

**2. 图表生成慢怎么办？**  
Web 默认使用快速模式，只生成 1~4 张聚焦图表。点击“重新生成图表”会生成完整图表集，耗时更长。

**3. 退货率问题如何回答？**  
Olist 数据集没有真实退货表，系统用 `review_score <= 2` 作为高退货/强不满意风险代理指标，并在回答中说明口径。

**4. 为什么要使用预聚合视图？**  
高频指标若每次从原始表 JOIN 聚合，交互延迟较高。预聚合将计算前置，Agent 在线提问时直接查询物化视图，可显著加速。
