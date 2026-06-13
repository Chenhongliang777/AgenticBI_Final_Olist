# Agentic BI 多表电商运营分析系统项目报告

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
