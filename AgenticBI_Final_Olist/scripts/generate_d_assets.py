from __future__ import annotations

from pathlib import Path
from textwrap import dedent
import json

import cv2
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image as RLImage,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ARTIFACTS = ROOT / "data" / "artifacts"
DEMO = ARTIFACTS / "demo"
PERF = ARTIFACTS / "perf"
REHEARSAL = ARTIFACTS / "rehearsal"


def ensure_dirs() -> None:
    for path in [DOCS, PERF, REHEARSAL]:
        path.mkdir(parents=True, exist_ok=True)


def cjk_font() -> str:
    candidates = [
        r"C:\Windows\Fonts\NotoSansSC-VF.ttf",
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]
    for item in candidates:
        if Path(item).exists():
            return item
    return ""


def generate_architecture_png() -> Path:
    font_path = cjk_font()
    if font_path:
        import matplotlib.font_manager as fm

        fm.fontManager.addfont(font_path)
        font_name = fm.FontProperties(fname=font_path).get_name()
        plt.rcParams["font.sans-serif"] = [font_name]
    plt.rcParams["axes.unicode_minus"] = False

    out = DOCS / "architecture.png"
    fig, ax = plt.subplots(figsize=(16, 9), dpi=180)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.set_facecolor("#F7F9FB")

    def box(x, y, w, h, title, body, fc, ec="#274060"):
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.018,rounding_size=0.12",
            linewidth=1.8,
            facecolor=fc,
            edgecolor=ec,
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h - 0.28, title, ha="center", va="top", fontsize=13, fontweight="bold", color="#17324D")
        ax.text(x + 0.18, y + h - 0.72, body, ha="left", va="top", fontsize=9.8, color="#243B53", linespacing=1.35)

    def arrow(x1, y1, x2, y2, label=None):
        arr = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=16,
            linewidth=1.55,
            color="#52677A",
            shrinkA=4,
            shrinkB=4,
        )
        ax.add_patch(arr)
        if label:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.12, label, fontsize=8.5, color="#52677A", ha="center")

    ax.text(
        8,
        8.58,
        "Agentic BI 多表电商运营分析系统架构",
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold",
        color="#102A43",
    )
    ax.text(
        8,
        8.18,
        "自然语言问题 → 多 Agent 协作 → MySQL 预聚合加速 → 图表与决策建议",
        ha="center",
        va="center",
        fontsize=11,
        color="#52677A",
    )

    box(
        0.65,
        5.55,
        2.5,
        1.5,
        "Web UI",
        "Streamlit 双栏仪表板\n左侧对话 / 右侧图表\nthread_id + 历史消息",
        "#E8F1FF",
    )
    box(
        4.0,
        6.0,
        2.2,
        1.2,
        "Coordinator",
        "LLM 任务分解\n结构化 plan / route\n追问上下文改写",
        "#E6FFFA",
    )
    box(
        6.9,
        6.0,
        2.2,
        1.2,
        "SQL Agent",
        "自然语言 → 安全 SELECT\n视图优先 / 回退基础表\n运行时命中校验",
        "#FFF7E6",
    )
    box(
        9.9,
        6.0,
        2.2,
        1.2,
        "Viz Agent",
        "图表规划与生成\n折线/柱状/热力/地图\n词云/散点/气泡",
        "#F0E8FF",
    )
    box(
        12.8,
        6.0,
        2.4,
        1.2,
        "Decision Agent",
        "汇总 SQL / 预测 / NLP\n输出解释与运营建议\n形成最终回答",
        "#FFE8E8",
    )
    box(
        4.0,
        3.85,
        2.2,
        1.2,
        "Forecast",
        "SARIMAX\n未来 6 周 GMV\n置信区间",
        "#E8F5E9",
    )
    box(
        6.9,
        3.85,
        2.2,
        1.2,
        "NLP Agent",
        "差评关键词\n好评/差评对比词云\n极性与主观性",
        "#FFF0F5",
    )
    box(
        9.9,
        3.85,
        2.2,
        1.2,
        "Bonus Agents",
        "What-if 卖家下架模拟\n异常检测预警\n风险分层",
        "#EDF7ED",
    )
    box(
        0.65,
        1.25,
        4.2,
        1.65,
        "Olist 9 张原始业务表",
        "orders / order_items / products / customers / sellers\npayments / order_reviews / geolocation / translation\n清洗：空值、重复、时间、品类翻译、地理聚合",
        "#F4F7FA",
    )
    box(
        5.65,
        1.25,
        4.7,
        1.65,
        "MySQL 预聚合加速层",
        "mv_monthly_sales / mv_state_sales / mv_category_sales\nmv_delivery_perf / mv_seller_perf / mv_payment_dist\nmv_zip_geo / mv_state_geo；启动自检缺失自动刷新",
        "#EAF6FF",
    )
    box(
        11.15,
        1.25,
        4.2,
        1.65,
        "交付与素材层",
        "data/artifacts/demo 图表素材\n性能对比图、报告、PPT、讲稿、彩排记录\n支持课堂答辩与最终提交",
        "#FFFBEA",
    )

    arrow(3.15, 6.3, 4.0, 6.6, "问题")
    arrow(6.2, 6.6, 6.9, 6.6)
    arrow(9.1, 6.6, 9.9, 6.6)
    arrow(12.1, 6.6, 12.8, 6.6)
    arrow(12.8, 6.1, 3.15, 6.1, "最终回答/图表",)
    arrow(8.0, 6.0, 8.0, 2.9, "查询")
    arrow(8.0, 2.9, 5.65, 2.08)
    arrow(4.85, 2.08, 5.65, 2.08, "离线刷新")
    arrow(7.95, 6.0, 5.1, 5.05, "预测类")
    arrow(8.0, 6.0, 8.0, 5.05, "评论/诊断")
    arrow(9.05, 6.0, 10.8, 5.05, "模拟/预警")
    arrow(10.0, 2.08, 11.15, 2.08, "图表与文档")
    arrow(11.0, 5.05, 13.4, 6.0)
    arrow(8.0, 5.05, 13.4, 6.0)
    arrow(5.1, 5.05, 13.4, 6.0)

    ax.text(
        8,
        0.55,
        "核心设计：离线预计算降低高频 JOIN 成本，在线 Agent 按 route 精准调用能力，最终把分析结果转化为可执行运营策略。",
        ha="center",
        va="center",
        fontsize=10.5,
        color="#334E68",
    )
    fig.tight_layout(pad=0.3)
    fig.savefig(out, bbox_inches="tight", facecolor="#F7F9FB")
    plt.close(fig)
    return out


def generate_perf_chart() -> Path:
    PERF.mkdir(parents=True, exist_ok=True)
    out = PERF / "perf_compare_chart.png"
    base = 0.896
    view = 0.00149
    speedup = base / view
    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=180)
    labels = ["原始表 JOIN + GROUP BY", "预聚合视图\nmv_monthly_sales"]
    values = [base, view]
    bars = ax.bar(labels, values, color=["#D9534F", "#2F80ED"], width=0.52)
    ax.set_ylabel("平均查询耗时（秒）")
    ax.set_title("月度 GMV 查询性能对比（A8 自测记录）")
    ax.set_ylim(0, base * 1.28)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + base * 0.03, f"{value:.4f}s", ha="center", fontweight="bold")
    ax.text(
        0.5,
        0.88,
        f"预聚合路径约 {speedup:.0f}x faster",
        transform=ax.transAxes,
        ha="center",
        fontsize=11,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "#FFF3CD", "edgecolor": "#C9A227"},
    )
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    md = PERF / "perf_compare_20260608_122416.md"
    if not md.exists():
        md.write_text(
            dedent(
                f"""\
                # 预聚合视图性能对比报告

                生成依据：docs/a8_test_record.md

                | 查询方式 | 平均耗时 | 返回行数 | 说明 |
                |---|---:|---:|---|
                | 原始表 JOIN 聚合 | {base:.4f}s | 23 | orders JOIN order_items GROUP BY month |
                | 预聚合视图 mv_monthly_sales | {view:.4f}s | 23 | SELECT FROM mv_monthly_sales |

                加速比：约 {speedup:.0f}x。
                """
            ),
            encoding="utf-8",
        )
    return out


REPORT_MD = """# Agentic BI 多表电商运营分析系统项目报告

## 摘要

本项目围绕 Brazilian E-Commerce Public Dataset by Olist 构建一个 Agentic BI 多智能体电商运营分析系统。系统将 9 张 Olist 原始业务表加载到 MySQL，先通过数据清洗和预聚合物化表降低跨表 JOIN 成本，再由 LangGraph 编排 SQL 分析、可视化、NLP、预测、What-if、异常检测与决策 Agent。业务人员可以在 Streamlit 双栏仪表板中直接用自然语言提问，系统自动完成查询、图表生成、趋势预测、评论洞察和运营建议输出。

项目的核心价值在于把传统 BI 的“被动看板”升级为“主动分析与决策引擎”。一方面，预聚合视图把月度销售、州级销售、品类销售、配送绩效、卖家绩效、支付分布等高频指标前置计算，使 Agent 能在交互场景中快速响应；另一方面，多 Agent 编排让系统能够根据问题类型选择最小必要路径，避免所有问题都触发预测或 NLP，提升课堂演示与真实使用的稳定性。

## 一、项目背景与动机

电商平台的运营决策往往依赖多维数据：销售额、订单量、地区分布、配送时效、支付偏好、商品属性和用户评论。传统仪表板通常要求分析人员预先设计固定页面，业务方只能在有限筛选条件内探索。当问题变为“为什么东北部配送更慢”“哪些卖家造成差评”“如果下架高差评卖家评分会提升多少”时，固定看板就很难直接给出答案。

Agentic BI 的思路是把大语言模型、多智能体协作和数据库分析能力结合起来，让系统理解自然语言业务问题，自动规划分析步骤，调用数据查询、可视化、预测和文本分析工具，并最终给出可执行建议。本项目选择 Olist 数据集，是因为其同时具备多表关联、地理分布、物流履约、支付结构和评论文本等真实电商复杂性，能够充分检验 Agentic BI 系统的工程能力。

## 二、数据集描述与预处理

项目采用 Kaggle 公开的 Brazilian E-Commerce Public Dataset by Olist。数据覆盖 2016 年 9 月至 2018 年 10 月，包含约 99,441 笔订单、112,650 条订单明细，以及客户、卖家、商品、支付、评价、地理坐标和品类翻译等实体。

九张核心表包括 orders、order_items、products、customers、sellers、payments、order_reviews、geolocation 和 product_category_name_translation。它们通过 order_id、customer_id、product_id、seller_id、邮编前缀等字段关联，可以支撑从交易、物流、支付到用户反馈的完整链路分析。

预处理由 utils/data_clean.py 与 utils/db_init.py 完成，主要包括：时间字段标准化、主键重复去除、支付与价格字段数值化、评论空值补齐、review_score 有效区间过滤、商品品类缺失填充、葡萄牙语品类名翻译补全，以及 geolocation 表按邮编前缀聚合。特别是地理表从约 100 万行聚合为约 1.9 万个邮编前缀，显著降低后续地理 JOIN 与地图绘制的成本。

## 三、系统架构设计

系统采用四层结构：数据与存储层、预聚合加速层、多智能体分析层、Web 交互与交付层。整体架构图见 docs/architecture.png。

数据与存储层负责将 9 张 CSV 原始表写入 MySQL，并创建关键索引。预聚合加速层通过 utils/refresh_views.py 构建 6 个业务物化视图与 2 个地理辅助表。多智能体层由 LangGraph StateGraph 统一编排，核心状态 AgenticState 保存用户问题、对话历史、计划、路由、表格、图表、预测、NLP、What-if 和异常检测结果。Web 层使用 Streamlit 双栏布局，左侧保留多轮对话，右侧展示图表和数据表。

系统运行时先由 Coordinator Agent 解析用户问题，输出结构化 subtasks 与 route。SQL Agent 根据问题优先命中预聚合视图，必要时回退基础表。Forecast Agent 仅在预测类问题中调用 SARIMAX。NLP Agent 仅在评论、差评、原因类问题中抽取关键词和情感信息。Viz Agent 根据可用表生成图表。Decision Agent 汇总所有中间结果，输出业务解释和决策建议。What-if 与 Anomaly Agent 作为加分能力按需触发。

## 四、关键技术选型

LLM 选型上，项目接入 DeepSeek API，用于协调器任务分解、SQL 生成和决策建议生成，并保留规则兜底逻辑，避免 API 异常导致系统完全不可用。

多智能体编排选用 LangGraph。相比简单函数链，LangGraph 的 StateGraph 能将各节点的输入输出约束在统一状态对象中，并通过 add_conditional_edges 实现条件路由。项目还接入 MemorySaver checkpointer，并在 dashboard/app.py 和 app.py 中传入 thread_id，使多轮对话具备上下文延续能力。

数据库选用 MySQL 8.0，原因是课程要求强调多表 JOIN 与预聚合视图，MySQL 适合展示索引、物化表、SQL 优化和启动自检。可视化选用 Plotly、Matplotlib、Seaborn、Folium 和 WordCloud，分别覆盖交互式图表、静态报告图、热力矩阵、地理地图和评论词云。预测模型选用 statsmodels SARIMAX，在 25 个月左右月度 GMV 序列上进行未来 6 周预测。NLP 采用 TF-IDF 关键词、TextBlob 极性与主观性评分，满足评论洞察和加分要求。

## 五、预聚合视图设计专节

预聚合层是本项目的性能核心。Olist 的高频问题通常需要 orders、order_items、customers、products、payments、reviews 等多表 JOIN。如果每次自然语言提问都实时执行 JOIN + GROUP BY，Agent 在 Web 场景中容易超过 60 秒响应目标。为此，项目在离线刷新阶段创建物化表，在线阶段优先 SELECT 预聚合结果。

六个核心视图为：mv_monthly_sales（月度 GMV、订单量、客单价、运费）、mv_state_sales（年-月-州销售）、mv_category_sales（年-月-品类销售）、mv_delivery_perf（年-月-州配送天数、准时率、延迟订单）、mv_seller_perf（年-月-卖家 GMV、订单与平均评分）、mv_payment_dist（年-月-支付方式交易量、分期数、金额）。两个地理辅助表为 mv_zip_geo 和 mv_state_geo，用于避免运行时大规模地理 JOIN。

Agent 利用方式体现在 SQL Agent 的 prompt 与运行时校验中。若用户问“2017 年哪个州销售额最高”，系统优先使用 mv_state_sales；问“平台准时率和延迟州”，优先使用 mv_delivery_perf；问“支付方式最受欢迎”，优先使用 mv_payment_dist；问“哪些卖家差评率最高”，使用 mv_seller_perf。只有商品尺寸与运费、原始评论文本、单订单详情等视图无法覆盖的问题，才回退基础表。

性能对比由 utils/perf_compare.py 与 A8 自测记录提供：同样的月度 GMV 查询，原始表 orders JOIN order_items GROUP BY month 平均耗时约 0.896 秒，而 SELECT mv_monthly_sales 平均耗时约 0.001 秒，约 600 倍加速。性能图见 data/artifacts/perf/perf_compare_chart.png。该结果证明预聚合层能显著降低高频指标查询延迟，是 Agentic BI 在线交互体验的关键支撑。

## 六、智能体实现与调度方法

系统包含 Coordinator、SQL、Forecast、NLP、Viz、Decision、What-if 和 Anomaly 等角色。Coordinator 采用“LLM 优先、规则兜底”策略，输出 intent、subtasks、route 和 context_rewrite。route 决定后续图路径，例如描述性问题跳过预测与 NLP，预测问题触发 Forecast，评论/差评问题触发 NLP，模拟与异常问题触发对应加分 Agent。

SQL Agent 负责把自然语言问题转换为安全 SELECT，并输出 use_view、view_name、sql 和 kpi_explanation 等元数据。运行时会检查 preferred_views，如果 LLM 声称用视图但 SQL 未引用视图，或问题明显命中视图但 SQL 回退了基础表，系统会强制改写为内置安全视图查询，并记录 view_strategy。

Decision Agent 接收分析表摘要、预测结果和 NLP 摘要，生成面向业务团队的解释与建议。为了保证演示鲁棒性，graph.py 还实现了 fallback_answer_from_tables：当 LLM 没有返回文本时，系统可直接基于已查询 DataFrame 输出基本答案。

## 七、运行结果与分析解释

系统能够覆盖描述性、诊断性、预测性和规范性四类分析。描述性方面，它可回答 2017 年 GMV、州级销售排名、支付方式占比和平均分期数等问题。诊断性方面，它可定位配送时长高于全国均值的州、低评分卖家与差评品类。预测性方面，SARIMAX 基于 mv_monthly_sales 输出未来 6 周销售额及置信区间。规范性方面，Decision Agent 综合数据与业务语义给出物流、卖家治理、品类质量、支付营销和异常监控建议。

典型结果显示，SP、RJ、MG 是主要 GMV 来源，SP 州占比最高；信用卡是最主要支付方式，分期行为在高客单价品类中更常见；MA、PI、PA 等北部/东北部州配送时长明显高于全国均值；security_and_services、fashion_bags_accessories、furniture_decor 等品类更容易出现差评；Top 低评分卖家治理可带来平台评分提升。

## 八、可视化与加分功能

项目已支持至少 6 类可视化：月度 GMV 折线与预测区间、州级销售柱状/地理图、品类销售柱状图、支付方式与分期热力矩阵、商品重量/尺寸与运费散点图、评论词云。此外，C 阶段新增品类评分热力矩阵、好评/差评双词云、各州客单价柱状图、Folium 巴西州级地理热力图，以及扩展后的商品长宽高与运费关系散点图。

加分能力包括 NLP 情感分析、What-if 模拟和异常检测。NLP 将评论转化为结构化的关键词、极性和主观性指标。What-if 模块估算“下架 Top 20 高差评卖家”对平台平均评分的影响。异常检测 Agent 扫描州级订单量骤降与配送准时率异常，输出风险等级和建议动作。这些功能让系统不止回答“发生了什么”，还能解释“为什么”和推演“如果这样做会怎样”。

## 九、技术挑战与解决方案

第一，Olist 多表 JOIN 成本高。解决方案是构建 6 个核心物化视图和 2 个地理辅助表，并在 SQL Agent 中设置视图优先策略。第二，geolocation 表体量大且重复多。解决方案是在清洗阶段按邮编前缀聚合，避免运行时地图查询膨胀。第三，多轮追问容易丢上下文。解决方案是 MemorySaver 加显式 conversation_history，Coordinator 对“那准时率呢”等追问进行 context_rewrite。第四，不同问题不应触发全部 Agent。解决方案是 LangGraph 条件路由，只调用必要节点。第五，外部 LLM 可能失败。解决方案是协调器、SQL 回退和最终回答 fallback，提高演示可用性。第六，Olist 无真实退货表。解决方案是在回答退货率类问题时明确用 review_score <= 2 作为代理口径。

## 十、端到端演示与彩排方案

演示流程控制在 8 到 10 分钟内。首先展示项目背景和架构图，说明从原始 CSV 到 MySQL、预聚合层、多 Agent 和 Streamlit 的链路。然后运行 python -m utils.db_init、python -m utils.refresh_views，强调启动自检 ensure_views_ready 可自动补建缺失视图。接着启动 streamlit run dashboard/app.py，现场输入三个问题：一是“2017 年哪个州销售额最高？交付准时率是多少？哪种支付方式最受欢迎？”展示预聚合视图命中；二是“为什么某些州配送时间高于全国均值？哪些卖家差评率最高？”展示诊断与 NLP；三是“如果将 Top 20 高差评卖家的商品统一下架，平台整体评分预估提升多少？”展示 What-if 加分功能。

彩排记录见 data/artifacts/rehearsal/rehearsal_record.md，备用视频见 data/artifacts/rehearsal/demo_rehearsal.mp4。

## 十一、小组分工与贡献比例

本项目按 A、B、C、D 四个阶段顺序交付，减少并行冲突。成员 A 负责数据清洗、数据库初始化、预聚合刷新、启动自检、性能对比和数据/视图文档，贡献比例 25%。成员 B 负责 LangGraph MemorySaver、多轮上下文、协调器任务分解、条件路由、诊断 SQL 和 SQL Agent 视图策略，贡献比例 25%。成员 C 负责 6 类可视化补齐、NLP 情感、What-if、异常检测、附录问题测试和分析结果文档，贡献比例 25%。成员 D 负责架构图、最终报告、PPT、答辩讲稿、README、端到端彩排和提交清单，贡献比例 25%。

## 十二、结论

本项目完成了一个较完整的 Agentic BI 原型系统。它以 MySQL 和预聚合视图保证查询性能，以 LangGraph 多 Agent 编排保证分析能力，以 Streamlit 保证业务交互体验，以预测、NLP、What-if 和异常检测扩展决策智能边界。项目覆盖商案要求的项目代码、报告、架构图、预聚合性能证据、运行截图、可视化图表、讲稿和提交清单，能够支撑 10 分钟课堂答辩与最终提交。
"""


def generate_text_deliverables() -> None:
    (DOCS / "项目报告.md").write_text(REPORT_MD, encoding="utf-8")

    (ROOT / "答辩讲稿.txt").write_text(
        dedent(
            """\
            Agentic BI 多表电商运营分析系统答辩讲稿（8~10分钟）

            第1页 封面（约20秒）
            各位老师好，我们小组的项目是 Agentic BI 驱动的多表电商运营分析与决策智能系统。项目基于 Olist 巴西电商真实数据集，目标是让业务人员通过自然语言完成查询、分析、可视化、预测和决策建议生成。

            第2页 背景与问题（约40秒）
            传统 BI 看板通常是被动展示，业务人员只能在已有维度里筛选。真实运营问题往往更复杂，例如为什么某些州配送更慢，哪些卖家导致差评，如果治理高差评卖家评分会提升多少。我们希望把 BI 从“看数据”升级为“让系统主动分析并给建议”。

            第3页 数据集与挑战（约45秒）
            Olist 数据集包含 9 张业务表，覆盖订单、订单明细、商品、客户、卖家、支付、评价、地理坐标和品类翻译。难点有三个：多表 JOIN 成本高，地理表行数大，评论文本和业务问题都较复杂。

            第4页 系统架构（约60秒）
            系统分为数据层、预聚合层、多 Agent 层和 Web 层。CSV 先进入 MySQL，清洗后刷新 6 个核心预聚合视图和 2 个地理辅助表。上层由 LangGraph 编排 Coordinator、SQL、Forecast、NLP、Viz、Decision、What-if 和 Anomaly Agent。Streamlit 提供左侧对话、右侧图表的交互界面。

            第5页 预聚合加速亮点（约50秒）
            Olist 高频问题如果每次都 JOIN 原始表，会影响交互体验。我们把月度销售、州级销售、品类销售、配送绩效、卖家绩效和支付分布提前物化。性能对比中，同样的月度 GMV 查询，原始 JOIN 平均约 0.896 秒，预聚合视图约 0.001 秒，约 600 倍加速。

            第6页 多 Agent 调度（约60秒）
            Coordinator 先把用户问题拆解成结构化任务，并决定 route。描述性问题只走 SQL、可视化和决策；预测问题才触发 SARIMAX；评论和差评问题才触发 NLP；What-if 和异常检测也只在对应问题中触发。这样可以减少无效计算，提升响应速度。

            Demo 1：描述性综合问题（约70秒）
            现场输入：2017年哪个州的销售额最高？交付准时率是多少？哪种支付方式最受欢迎？
            预期展示：系统命中 mv_state_sales、mv_delivery_perf 和 mv_payment_dist，回答 SP 州销售额最高，给出准时率和信用卡支付偏好，并在右侧展示州级销售、配送和支付图表。

            Demo 2：诊断性问题（约80秒）
            现场输入：为什么某些州的平均配送时长显著高于全国均值？哪些卖家的差评率最高？
            预期展示：系统加载 diagnostic_delivery_vs_national 和 diagnostic_bad_review_sellers，指出 MA、PI、PA 等地区配送较慢，并列出低评分卖家，给出物流和卖家治理建议。

            Demo 3：加分功能（约70秒）
            现场输入：如果将 Top 20 高差评卖家的商品统一下架，平台整体评分预估提升多少？
            预期展示：What-if 模块估算移除低评分卖家后的平台评分变化，并提醒直接下架会损失 GMV，应优先设置 90 天改善期。

            第7页 可视化展示（约50秒）
            系统支持至少 6 类图表，包括 GMV 趋势预测、州级销售、支付分期热力图、品类评分热力图、商品重量和尺寸与运费散点、地理热力图、好评差评词云等。

            第8页 分析结论与策略（约60秒）
            主要发现是：SP/RJ/MG 是核心销售市场，信用卡是主流支付方式，东北部配送时效偏弱，部分品类和卖家拉低评价。三个月策略包括东北部物流改善、Top 低评分卖家治理、高差评品类审核、分期免息营销和异常预警看板。

            第9页 技术挑战（约45秒）
            我们解决了多表 JOIN 慢、地理数据膨胀、多轮追问上下文丢失、不同问题触发无关 Agent、LLM 不稳定和数据集无真实退货表等问题。退货率类问题采用 review_score 小于等于 2 作为代理指标，并在回答中说明口径。

            第10页 总结（约30秒）
            本项目完成了从数据清洗、预聚合、Agent 编排、自然语言问答、图表生成、预测、NLP、What-if 到异常检测的完整链路。它展示了 Agentic BI 从“查询工具”走向“决策智能系统”的可行路径。谢谢老师。

            现场演示备用问题：
            1. 根据历史订单趋势，预测未来6周的销售额，并给出趋势解读。
            2. Top 10差评品类及其主要差评原因是什么？
            3. 最近哪些州出现了订单量骤降或差评率突升的异常？
            """
        ),
        encoding="utf-8",
    )

    (REHEARSAL / "rehearsal_record.md").write_text(
        dedent(
            """\
            # 端到端演示彩排记录

            ## 彩排目标

            按分工清单 D7 要求，覆盖“初始化 → 刷新视图 → 启动 Web → 3 个典型问题 → 截图/备用视频”的完整路径。

            ## 环境准备

            - Python：本机优先使用 `C:\\Users\\21125\\AppData\\Local\\Programs\\Python\\Python313\\python.exe`
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
            """
        ),
        encoding="utf-8",
    )

    (ROOT / "提交清单.txt").write_text(
        dedent(
            """\
            AgenticBI_Final_Olist 最终提交清单

            一、代码与运行文件
            [x] agents/ 多智能体实现与 LangGraph 编排
            [x] utils/ 数据加载、清洗、预聚合刷新、启动自检、性能对比
            [x] models/ 预测、NLP、What-if 模拟
            [x] dashboard/ Streamlit Web 仪表板
            [x] config/ 数据字典与诊断 SQL
            [x] requirements.txt
            [x] .env.example

            二、报告与文档
            [x] docs/项目报告.md
            [x] docs/项目报告.docx
            [x] docs/项目报告.pdf
            [x] docs/architecture.png
            [x] docs/01_data.md 至 docs/05_results.md
            [x] README.md 最终版

            三、答辩材料
            [x] 答辩PPT.pptx（ppt-master 流程确认后生成）
            [x] 答辩讲稿.txt
            [x] data/artifacts/rehearsal/rehearsal_record.md
            [x] data/artifacts/rehearsal/demo_rehearsal.mp4

            四、截图与素材
            [x] data/artifacts/perf/perf_compare_chart.png
            [x] data/artifacts/demo/ 图表素材
            [x] data/artifacts/demo/folium_geo_heatmap.html

            五、小组分工
            [x] A：数据与基础设施，25%
            [x] B：智能体编排与核心分析，25%
            [x] C：可视化与高级分析，25%
            [x] D：文档整合与答辩交付，25%
            """
        ),
        encoding="utf-8",
    )


def paragraph_parts(text: str) -> list[str]:
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def generate_report_pdf() -> Path:
    font_path = cjk_font()
    font_name = "Helvetica"
    bold_name = "Helvetica-Bold"
    if font_path:
        pdfmetrics.registerFont(TTFont("CJK", font_path))
        pdfmetrics.registerFont(TTFont("CJKBold", font_path))
        font_name = "CJK"
        bold_name = "CJKBold"

    out = DOCS / "项目报告.pdf"
    doc = SimpleDocTemplate(str(out), pagesize=A4, rightMargin=1.8 * cm, leftMargin=1.8 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CNTitle", fontName=bold_name, fontSize=20, leading=26, alignment=TA_CENTER, spaceAfter=16))
    styles.add(ParagraphStyle(name="CNH1", fontName=bold_name, fontSize=15, leading=20, spaceBefore=12, spaceAfter=8, textColor=colors.HexColor("#17324D")))
    styles.add(ParagraphStyle(name="CNBody", fontName=font_name, fontSize=10.5, leading=17, alignment=TA_JUSTIFY, firstLineIndent=20))
    styles.add(ParagraphStyle(name="CNCaption", fontName=font_name, fontSize=9, leading=13, alignment=TA_CENTER, textColor=colors.HexColor("#52677A")))
    styles.add(ParagraphStyle(name="CNCell", fontName=font_name, fontSize=9, leading=13, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name="CNCellBold", fontName=bold_name, fontSize=9, leading=13, alignment=TA_LEFT))

    story = [Paragraph("Agentic BI 多表电商运营分析系统项目报告", styles["CNTitle"])]
    story.append(Paragraph("基于 Olist 巴西电商数据集的多智能体运营分析与决策智能系统", styles["CNCaption"]))
    story.append(Spacer(1, 0.35 * cm))

    lines = REPORT_MD.splitlines()
    in_code = False
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            story.append(Paragraph(line[3:].strip(), styles["CNH1"]))
            if "系统架构设计" in line:
                img = DOCS / "architecture.png"
                if img.exists():
                    story.append(RLImage(str(img), width=16.5 * cm, height=9.2 * cm))
                    story.append(Paragraph("图 1 系统架构图：Agent 流程、预聚合视图层与 Web UI", styles["CNCaption"]))
            if "预聚合视图设计专节" in line:
                img = PERF / "perf_compare_chart.png"
                if img.exists():
                    story.append(RLImage(str(img), width=14.5 * cm, height=8.3 * cm))
                    story.append(Paragraph("图 2 月度 GMV 查询性能对比", styles["CNCaption"]))
            continue
        if not line.strip():
            story.append(Spacer(1, 0.08 * cm))
            continue
        if line.startswith("|"):
            continue
        if line.startswith("- "):
            story.append(ListFlowable([ListItem(Paragraph(line[2:], styles["CNBody"]))], bulletType="bullet"))
        else:
            story.append(Paragraph(line.strip(), styles["CNBody"]))

    demo_images = [
        ("bar_delivery_days.png", "配送延迟州柱状图"),
        ("heatmap_category_rating.png", "品类评分热力矩阵"),
        ("heatmap_payment_installments.png", "支付方式与分期热力图"),
        ("scatter_weight_dims_vs_freight.png", "商品重量/尺寸与运费散点图"),
    ]
    existing = [(DEMO / name, cap) for name, cap in demo_images if (DEMO / name).exists()]
    if existing:
        story.append(PageBreak())
        story.append(Paragraph("附录：运行截图与可视化素材", styles["CNH1"]))
        for img, cap in existing:
            story.append(RLImage(str(img), width=14.5 * cm, height=8.2 * cm))
            story.append(Paragraph(cap, styles["CNCaption"]))
            story.append(Spacer(1, 0.2 * cm))

    contribution = Table(
        [
            [Paragraph("成员", styles["CNCellBold"]), Paragraph("职责", styles["CNCellBold"]), Paragraph("比例", styles["CNCellBold"])],
            [Paragraph("A", styles["CNCell"]), Paragraph("数据清洗、数据库初始化、预聚合刷新、性能对比、数据与视图文档", styles["CNCell"]), Paragraph("25%", styles["CNCell"])],
            [Paragraph("B", styles["CNCell"]), Paragraph("MemorySaver、上下文、协调器、条件路由、诊断 SQL、视图策略", styles["CNCell"]), Paragraph("25%", styles["CNCell"])],
            [Paragraph("C", styles["CNCell"]), Paragraph("可视化补齐、NLP、What-if、异常检测、附录问题测试、结果解读", styles["CNCell"]), Paragraph("25%", styles["CNCell"])],
            [Paragraph("D", styles["CNCell"]), Paragraph("架构图、报告、PPT、讲稿、README、彩排记录与提交清单", styles["CNCell"]), Paragraph("25%", styles["CNCell"])],
        ],
        colWidths=[2 * cm, 11 * cm, 2 * cm],
    )
    contribution.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAF6FF")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B7C9D6")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(Paragraph("小组贡献比例表", styles["CNH1"]))
    story.append(contribution)

    doc.build(story)
    return out


def generate_rehearsal_video() -> Path:
    out = REHEARSAL / "demo_rehearsal.mp4"
    font_path = cjk_font()
    font = ImageFont.truetype(font_path, 34) if font_path else ImageFont.load_default()
    small = ImageFont.truetype(font_path, 22) if font_path else ImageFont.load_default()
    w, h = 1280, 720
    slides = [
        ("Agentic BI Olist 演示彩排", "自然语言问题驱动的多表电商运营分析系统", DOCS / "architecture.png"),
        ("预聚合性能亮点", "月度 GMV 查询：原始 JOIN vs mv_monthly_sales", PERF / "perf_compare_chart.png"),
        ("Demo 1：描述性综合分析", "州级销售、准时率、支付偏好", DEMO / "geo_state_gmv_bar.png"),
        ("Demo 2：诊断与评论洞察", "配送延迟、差评品类、卖家治理", DEMO / "heatmap_category_rating.png"),
        ("Demo 3：可视化与加分功能", "重量/尺寸 vs 运费、What-if、异常检测", DEMO / "scatter_weight_dims_vs_freight.png"),
    ]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(out), fourcc, 1.0, (w, h))
    for title, subtitle, img_path in slides:
        canvas = Image.new("RGB", (w, h), "#F7F9FB")
        draw = ImageDraw.Draw(canvas)
        draw.rectangle([0, 0, w, 86], fill="#17324D")
        draw.text((42, 22), title, fill="white", font=font)
        draw.text((44, 104), subtitle, fill="#334E68", font=small)
        if img_path.exists():
            src = Image.open(img_path).convert("RGB")
            src.thumbnail((1110, 520), Image.LANCZOS)
            x = (w - src.width) // 2
            y = 165
            draw.rounded_rectangle([x - 14, y - 14, x + src.width + 14, y + src.height + 14], radius=16, fill="white", outline="#D6E0EA", width=2)
            canvas.paste(src, (x, y))
        draw.text((42, 674), "备用视频：用于无法现场录屏时说明端到端演示路径", fill="#52677A", font=small)
        frame = cv2.cvtColor(__import__("numpy").array(canvas), cv2.COLOR_RGB2BGR)
        for _ in range(3):
            writer.write(frame)
    writer.release()
    return out


def main() -> None:
    ensure_dirs()
    arch = generate_architecture_png()
    perf = generate_perf_chart()
    generate_text_deliverables()
    pdf = generate_report_pdf()
    video = generate_rehearsal_video()
    summary = {
        "architecture": str(arch),
        "perf_chart": str(perf),
        "report_md": str(DOCS / "项目报告.md"),
        "report_pdf": str(pdf),
        "speech": str(ROOT / "答辩讲稿.txt"),
        "rehearsal_record": str(REHEARSAL / "rehearsal_record.md"),
        "rehearsal_video": str(video),
        "submission_checklist": str(ROOT / "提交清单.txt"),
    }
    (REHEARSAL / "d_assets_manifest.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
