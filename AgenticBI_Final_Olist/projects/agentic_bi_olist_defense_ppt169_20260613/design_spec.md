# agentic_bi_olist_defense - Design Spec

> Human-readable design narrative for the Agentic BI Olist defense deck.

## I. Project Information

| Item | Value |
| ---- | ----- |
| **Project Name** | agentic_bi_olist_defense |
| **Canvas Format** | PPT 16:9 (1280x720) |
| **Page Count** | 18 |
| **Design Style** | B) General Consulting + clean technology data defense |
| **Target Audience** | Course instructors and defense reviewers |
| **Use Case** | 8-10 minute final project defense |
| **Created Date** | 2026-06-13 |

---

## II. Canvas Specification

| Property | Value |
| -------- | ----- |
| **Format** | PPT 16:9 |
| **Dimensions** | 1280x720 |
| **viewBox** | `0 0 1280 720` |
| **Margins** | 48px left/right, 36px top, 32px bottom |
| **Content Area** | 1184x620 |

---

## III. Visual Theme

### Theme Style

- **Style**: General Consulting, clean data product defense
- **Theme**: Light theme
- **Tone**: professional, technical, evidence-driven, calm

### Color Scheme

| Role | HEX | Purpose |
| ---- | --- | ------- |
| **Background** | `#F7F9FB` | Page background |
| **Secondary bg** | `#FFFFFF` | Panels and chart frames |
| **Primary** | `#17324D` | Titles and dark structural elements |
| **Accent** | `#2F80ED` | Main highlights and key numbers |
| **Secondary accent** | `#00A6A6` | Process and Agent highlights |
| **Warm accent** | `#F2994A` | Performance / warning highlights |
| **Body text** | `#1F2937` | Main body text |
| **Secondary text** | `#52677A` | Captions and annotations |
| **Tertiary text** | `#94A3B8` | Footers and source notes |
| **Border/divider** | `#D6E0EA` | Light separators |
| **Success** | `#2E7D32` | Positive indicators |
| **Warning** | `#C62828` | Risk and constraint markers |

No AI image strategy is required because all images are user-provided project artifacts.

---

## IV. Typography System

### Font Plan

**Typography direction**: PPT-safe CJK-first consulting sans.

| Role | Chinese | English | Fallback tail |
| ---- | ------- | ------- | ------------- |
| **Title** | `"Microsoft YaHei"` | Arial | sans-serif |
| **Body** | `"Microsoft YaHei"` | Arial | sans-serif |
| **Emphasis** | `"Microsoft YaHei"` | Arial | sans-serif |
| **Code** | - | Consolas, `"Courier New"` | monospace |

**Per-role font stacks**

- Title: `"Microsoft YaHei", Arial, sans-serif`
- Body: `"Microsoft YaHei", Arial, sans-serif`
- Emphasis: `"Microsoft YaHei", Arial, sans-serif`
- Code: `Consolas, "Courier New", monospace`

### Font Size Hierarchy

**Baseline**: Body font size = 18px.

| Purpose | Ratio to body | Current Project | Weight |
| ------- | ------------- | --------------- | ------ |
| Cover title | 2.5-5x | 58-72px | Bold |
| Section opener | 2-2.5x | 42-48px | Bold |
| Page title | 1.5-2x | 30-34px | Bold |
| Hero number | 1.5-2x | 36-48px | Bold |
| Subtitle | 1.2-1.5x | 22-26px | Semibold |
| Body content | 1x | 18px | Regular |
| Annotation | 0.7-0.85x | 13-15px | Regular |
| Footnote | 0.5-0.65x | 10-12px | Regular |

Formula rendering policy: `text-only`.

---

## V. Layout Principles

### Page Structure

- **Header area**: 36-92px, title and page section marker.
- **Content area**: 100-640px, charts, architecture diagrams, or message blocks.
- **Footer area**: 660-700px, source note and page number.

### Layout Pattern Library

Use consulting-style compositions: assertion title + takeaway strip + main evidence. Alternate dense pages with a few breathing pages to avoid uniform card grids.

| Pattern | Usage |
| ------- | ----- |
| Single column centered | Cover, conclusion, agenda |
| Left-chart right-text | Performance, demo screenshots, result pages |
| Layered architecture | System architecture and Agent flow |
| KPI cards | Project value and scoring coverage |
| Vertical list | Challenges and final strategy |
| Timeline / numbered steps | Demo flow and end-to-end rehearsal |
| Image-as-canvas with native overlay | Architecture and screenshot slides |

### Spacing Specification

| Element | Current Project |
| ------- | --------------- |
| Safe margin | 48px |
| Content block gap | 28px |
| Icon-text gap | 12px |
| Card gap | 22px |
| Card padding | 22px |
| Card border radius | 10px |

---

## VI. Icon Usage Specification

### Source

- **Built-in icon library**: `tabler-outline`
- **Stroke width**: 2
- **Usage method**: SVG placeholder `<use data-icon="tabler-outline/icon-name" .../>`

### Recommended Icon List

| Purpose | Icon Path | Page |
| ------- | --------- | ---- |
| Data / chart | `tabler-outline/chart-bar` | P03, P06 |
| Database | `tabler-outline/database` | P05 |
| Agent / users | `tabler-outline/users` | P07 |
| Speed | `tabler-outline/bolt` | P06 |
| Decision | `tabler-outline/bulb` | P12, P17 |
| Risk | `tabler-outline/alert-triangle` | P14, P16 |

---

## VII. Visualization Reference List

Catalog read: 71 templates

This deck primarily embeds existing project screenshots and charts as image evidence. Native chart templates are not used because the source charts have already been generated by the system and should be shown as delivered artifacts.

| Page | Template | Path | Summary-quote (verbatim from `charts_index.json`) | Usage |
| ---- | -------- | ---- | ------------------------------------------------- | ----- |
| P06 | no-template-match | Existing image screenshot | "Pick for single-series category value comparison, 3-8 categories. Skip for >12 long-label items (use horizontal_bar_chart) or multi-series (use grouped_bar_chart)." | Performance screenshot is embedded as evidence rather than redrawn |
| P13 | no-template-match | Existing image screenshot | "Pick for 2D matrix where each cell is an intensity value (activity grid, correlation matrix). Skip for ranked categories (use bar_chart)." | Category rating heatmap is embedded as generated demo output |
| P15 | no-template-match | Existing image screenshot | "Pick for x-y correlation, cluster, or outlier scan. Skip if a size dimension also matters (use bubble_chart)." | Scatter screenshot is embedded as generated demo output |

**Runners-up considered**

- `kpi_cards` | rejected for P06: the benchmark page needs the actual performance screenshot, not a recreated KPI summary.
- `layered_architecture` | rejected for P04: the project already has a hand-made architecture image with exact module names.
- `vertical_list` | rejected for P17: the final strategy needs hierarchy plus timing, so a custom roadmap/list hybrid is clearer.

---

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Layout pattern | Acquire Via | Status | Reference | text_policy | page_role |
| -------- | ---------- | ----- | ------- | ---- | -------------- | ----------- | ------ | --------- | ----------- | --------- |
| architecture.png | 2901x1641 | 1.77 | System architecture evidence | Diagram | #44 Background image + native network/architecture diagram | user | Existing | Project architecture diagram | none | local |
| perf_compare_chart.png | 1511x882 | 1.71 | Pre-aggregation performance evidence | Chart screenshot | #43 Background image + native data chart on top | user | Existing | Performance benchmark screenshot | none | local |
| geo_state_gmv_bar.png | 1400x1000 | 1.40 | State GMV demo screenshot | Chart screenshot | #19 Image floating in whitespace with thin frame and caption | user | Existing | State GMV chart | none | local |
| heatmap_payment_installments.png | 1400x1000 | 1.40 | Payment heatmap demo screenshot | Chart screenshot | #19 Image floating in whitespace with thin frame and caption | user | Existing | Payment heatmap | none | local |
| heatmap_category_rating.png | 2672x1979 | 1.35 | Category rating heatmap demo screenshot | Chart screenshot | #19 Image floating in whitespace with thin frame and caption | user | Existing | Rating heatmap | none | local |
| bar_delivery_days.png | 1400x1000 | 1.40 | Delivery diagnostic demo screenshot | Chart screenshot | #19 Image floating in whitespace with thin frame and caption | user | Existing | Delivery delay chart | none | local |
| bar_state_avg_basket.png | 1400x1000 | 1.40 | AOV demo screenshot | Chart screenshot | #19 Image floating in whitespace with thin frame and caption | user | Existing | State AOV chart | none | local |
| bar_top_categories.png | 1400x1000 | 1.40 | Category GMV demo screenshot | Chart screenshot | #19 Image floating in whitespace with thin frame and caption | user | Existing | Top category chart | none | local |
| scatter_weight_dims_vs_freight.png | 2748x2457 | 1.12 | Weight and dimension freight analysis | Chart screenshot | #19 Image floating in whitespace with thin frame and caption | user | Existing | Product dimension scatter | none | local |

---

## IX. Content Outline

### Part 1: Opening

#### Slide 01 - Cover
- **Layout**: Single column centered, dark title band on light grid background.
- **Title**: Agentic BI 多表电商运营分析系统
- **Core message**: 本项目把 Olist 多表数据变成可对话、可预测、可建议的运营决策系统。
- **Content**: Olist Brazilian E-Commerce Dataset；MySQL 预聚合；LangGraph 多 Agent；Streamlit 双栏仪表板。

#### Slide 02 - Defense Roadmap
- **Layout**: Agenda list with five numbered segments.
- **Title**: 10 分钟答辩围绕“数据、Agent、Demo、决策”展开
- **Core message**: 答辩路径从业务问题出发，最终落到可运行系统和运营策略。
- **Content**: 背景与数据挑战；系统架构；预聚合加速；多 Agent 协作；Demo 与决策建议。

#### Slide 03 - Problem Framing
- **Layout**: Three contrast cards.
- **Title**: 固定看板无法覆盖复杂运营追问
- **Core message**: Agentic BI 的价值在于让系统主动规划分析，而不是只展示预设图表。
- **Content**: 多表 JOIN 难；诊断问题需要跨维度解释；业务人员希望直接得到建议。

### Part 2: Architecture and Engineering

#### Slide 04 - System Architecture
- **Layout**: Full-width architecture image with two takeaway callouts.
- **Title**: 系统采用“数据层 + 预聚合层 + 多 Agent 层 + Web 层”
- **Core message**: 四层架构把离线数据工程与在线智能分析连接起来。
- **Visualization**: Existing architecture image.

#### Slide 05 - Data Pipeline
- **Layout**: Horizontal pipeline with table counts and cleaning steps.
- **Title**: 9 张原始表先清洗落库，再进入预聚合刷新
- **Core message**: 数据清洗保证上层 Agent 查询的数据可 JOIN、可解释、可索引。
- **Content**: 时间标准化；重复去除；评论空值补齐；品类翻译；地理表按邮编聚合。

#### Slide 06 - Pre-Aggregation Benchmark
- **Layout**: Left performance screenshot, right insight panel.
- **Title**: 预聚合视图让月度 GMV 查询约 600 倍加速
- **Core message**: 高频指标离线预计算，是 Web 端交互体验稳定的关键。
- **Visualization**: Existing performance chart screenshot.

#### Slide 07 - Agent Orchestration
- **Layout**: Layered process diagram from question to answer.
- **Title**: LangGraph 按问题类型路由最小必要 Agent
- **Core message**: 条件分支避免所有问题都触发预测或 NLP，提升响应速度和可控性。
- **Content**: Coordinator 规划；SQL 视图优先；Forecast/NLP/Viz 按需；Decision 汇总建议。

#### Slide 08 - Memory and Follow-up
- **Layout**: Conversation example plus state objects.
- **Title**: MemorySaver 与显式历史让追问不丢上下文
- **Core message**: “那准时率呢？”会被改写为带上轮问题的完整分析任务。
- **Content**: thread_id；conversation_history；context_rewrite；SQL Agent 继承上下文。

### Part 3: Demo Evidence

#### Slide 09 - Demo Script
- **Layout**: Three numbered live demo questions.
- **Title**: 现场演示用三类问题覆盖核心能力
- **Core message**: 描述性、诊断性、What-if 三个问题可以证明系统链路完整。
- **Content**: 州销售 + 准时率 + 支付；配送延迟 + 差评卖家；下架高差评卖家评分提升。

#### Slide 10 - Descriptive Demo
- **Layout**: State GMV chart plus KPI notes.
- **Title**: 描述性分析优先命中州级、配送和支付视图
- **Core message**: 用户一个复合问题即可得到州销售、准时率和支付偏好。
- **Visualization**: Existing state GMV screenshot.

#### Slide 11 - Payment Behavior
- **Layout**: Payment heatmap screenshot plus short interpretation.
- **Title**: 支付热力图揭示信用卡和分期是核心支付行为
- **Core message**: 支付偏好不仅是统计结果，也能转化为分期营销建议。
- **Visualization**: Existing payment heatmap screenshot.

#### Slide 12 - Diagnostic Demo
- **Layout**: Delivery chart and seller-risk interpretation.
- **Title**: 诊断性问题把配送延迟和差评卖家连接起来
- **Core message**: 系统可从“哪里慢”进一步下钻到“为什么慢”和“谁在拉低体验”。
- **Visualization**: Existing delivery delay screenshot.

#### Slide 13 - Review and Category Insight
- **Layout**: Heatmap screenshot plus NLP insight strip.
- **Title**: 评论与评分分析定位高差评品类
- **Core message**: 品类评分热力矩阵和词云让差评原因更可解释。
- **Visualization**: Existing category rating heatmap screenshot.

#### Slide 14 - Bonus Capabilities
- **Layout**: Two-column: What-if and anomaly detection.
- **Title**: What-if 与异常检测把分析推进到决策智能
- **Core message**: 系统不仅解释历史，还能模拟治理动作并主动发现风险。
- **Content**: Top 20 低评分卖家下架模拟；州级订单骤降和准时率异常预警。

#### Slide 15 - Visualization Coverage
- **Layout**: 2x2 image mosaic with labels.
- **Title**: 可视化覆盖趋势、地区、支付、品类、物流和商品属性
- **Core message**: ≥6 类图表让同一系统可支撑多种经营分析场景。
- **Visualization**: Existing demo screenshots.

### Part 4: Results and Close

#### Slide 16 - Challenges and Fixes
- **Layout**: Challenge-solution table.
- **Title**: 工程挑战通过“预计算、路由、兜底、口径说明”逐一化解
- **Core message**: 答辩重点不是单个模型，而是系统工程的稳定闭环。
- **Content**: JOIN 慢；地理表膨胀；追问上下文；LLM 不稳定；无真实退货表。

#### Slide 17 - Three-Month Actions
- **Layout**: Priority roadmap.
- **Title**: 运营建议聚焦物流、卖家、品类、支付和预警
- **Core message**: Agent 输出的建议可转化为三个月内可执行的运营路线图。
- **Content**: P0 东北部物流改善；P1 低评分卖家治理；P2 高差评品类审核；P3 分期营销；P4 异常预警。

#### Slide 18 - Closing
- **Layout**: Centered conclusion with submission checklist.
- **Title**: 项目完成从数据工程到决策智能的端到端闭环
- **Core message**: 最终提交覆盖代码、报告、PPT、讲稿、截图素材和 README。
- **Content**: 预聚合加速；多 Agent 协作；自然语言交互；可视化与加分功能；完整答辩交付。

---

## X. Speaker Notes Requirements

One speaker note file per page, saved to `notes/`, split from `notes/total.md`. Notes should be pure spoken narration in Chinese, conclusion-first, 2-4 natural sentences per slide, and match the 8-10 minute defense script.

---

## XI. Technical Constraints Reminder

1. viewBox: `0 0 1280 720`.
2. Background uses `<rect>` elements.
3. Text wrapping uses `<tspan>`; `<foreignObject>` is forbidden.
4. Transparency uses `fill-opacity` / `stroke-opacity`; `rgba()` is forbidden.
5. Forbidden: `mask`, `<style>`, `class`, `foreignObject`, `textPath`, `animate*`, `script`, `<g opacity>`.
6. Every top-level content block must be wrapped in semantic `<g id="...">`.
7. Images use paths from `images/` only and remain no-crop when they are screenshots.
