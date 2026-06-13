const fs = require("fs");
const path = require("path");
const {
  AlignmentType,
  BorderStyle,
  Document,
  Footer,
  HeadingLevel,
  ImageRun,
  LevelFormat,
  Packer,
  PageBreak,
  PageNumber,
  Paragraph,
  ShadingType,
  Table,
  TableCell,
  TableOfContents,
  TableRow,
  TextRun,
  WidthType,
} = require("docx");

const ROOT = path.resolve(__dirname, "..");
const DOCS = path.join(ROOT, "docs");
const DEMO = path.join(ROOT, "data", "artifacts", "demo");
const PERF = path.join(ROOT, "data", "artifacts", "perf");
const reportPath = path.join(DOCS, "项目报告.md");
const outPath = path.join(DOCS, "项目报告.docx");

const border = { style: BorderStyle.SINGLE, size: 1, color: "B7C9D6" };
const borders = { top: border, bottom: border, left: border, right: border };

function run(text, opts = {}) {
  return new TextRun({ text, font: "Microsoft YaHei", size: opts.size || 22, bold: opts.bold || false, color: opts.color || "111827" });
}

function p(text, opts = {}) {
  return new Paragraph({
    children: [run(text, opts)],
    spacing: { before: opts.before || 0, after: opts.after || 120, line: opts.line || 330 },
    alignment: opts.alignment || AlignmentType.LEFT,
  });
}

function heading(text, level = 1) {
  return new Paragraph({
    text,
    heading: level === 1 ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2,
    spacing: { before: 260, after: 150 },
  });
}

function image(file, width, height, caption) {
  if (!fs.existsSync(file)) return [];
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new ImageRun({
          type: "png",
          data: fs.readFileSync(file),
          transformation: { width, height },
          altText: { title: caption, description: caption, name: path.basename(file) },
        }),
      ],
      spacing: { before: 120, after: 80 },
    }),
    new Paragraph({ alignment: AlignmentType.CENTER, children: [run(caption, { size: 18, color: "52677A" })], spacing: { after: 160 } }),
  ];
}

function cell(text, width, bold = false) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    margins: { top: 90, bottom: 90, left: 120, right: 120 },
    shading: bold ? { fill: "EAF6FF", type: ShadingType.CLEAR } : undefined,
    children: [new Paragraph({ children: [run(text, { size: 18, bold })] })],
  });
}

function contributionTable() {
  const rows = [
    ["成员", "职责", "比例", true],
    ["A", "数据清洗、数据库初始化、预聚合刷新、性能对比、数据与视图文档", "25%", false],
    ["B", "MemorySaver、上下文、协调器、条件路由、诊断 SQL、视图策略", "25%", false],
    ["C", "可视化补齐、NLP、What-if、异常检测、附录问题测试、结果解读", "25%", false],
    ["D", "架构图、报告、PPT、讲稿、README、彩排记录与提交清单", "25%", false],
  ];
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [1100, 6860, 1400],
    rows: rows.map(([a, b, c, bold]) => new TableRow({ children: [cell(a, 1100, bold), cell(b, 6860, bold), cell(c, 1400, bold)] })),
  });
}

const md = fs.readFileSync(reportPath, "utf8");
const children = [
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 240, after: 160 },
    children: [run("Agentic BI 多表电商运营分析系统项目报告", { size: 36, bold: true, color: "17324D" })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 360 },
    children: [run("基于 Olist 巴西电商数据集的多智能体运营分析与决策智能系统", { size: 22, color: "52677A" })],
  }),
  new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-2" }),
  new Paragraph({ children: [new PageBreak()] }),
];

let inCode = false;
for (const raw of md.split(/\r?\n/)) {
  const line = raw.trim();
  if (line.startsWith("```")) {
    inCode = !inCode;
    continue;
  }
  if (inCode || line.startsWith("|")) continue;
  if (line.startsWith("# ")) continue;
  if (line.startsWith("## ")) {
    const title = line.slice(3).trim();
    children.push(heading(title, 1));
    if (title.includes("系统架构设计")) {
      children.push(...image(path.join(DOCS, "architecture.png"), 620, 348, "图 1 系统架构图：Agent 流程、预聚合视图层与 Web UI"));
    }
    if (title.includes("预聚合视图设计专节")) {
      children.push(...image(path.join(PERF, "perf_compare_chart.png"), 560, 330, "图 2 月度 GMV 查询性能对比"));
    }
    continue;
  }
  if (!line) {
    children.push(new Paragraph({ spacing: { after: 60 } }));
  } else if (line.startsWith("- ")) {
    children.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [run(line.slice(2))], spacing: { after: 80 } }));
  } else {
    children.push(p(line));
  }
}

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(heading("附录：运行截图与可视化素材", 1));
for (const [file, cap] of [
  ["bar_delivery_days.png", "配送延迟州柱状图"],
  ["heatmap_category_rating.png", "品类评分热力矩阵"],
  ["heatmap_payment_installments.png", "支付方式与分期热力图"],
  ["scatter_weight_dims_vs_freight.png", "商品重量/尺寸与运费散点图"],
]) {
  children.push(...image(path.join(DEMO, file), 560, 318, cap));
}
children.push(heading("小组贡献比例表", 1));
children.push(contributionTable());

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Microsoft YaHei", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 30, bold: true, font: "Microsoft YaHei", color: "17324D" },
        paragraph: { spacing: { before: 260, after: 150 }, outlineLevel: 0 },
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 26, bold: true, font: "Microsoft YaHei", color: "334E68" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 1 },
      },
    ],
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
      },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1080, right: 1270, bottom: 1080, left: 1270 },
        },
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [run("Agentic BI Olist 项目报告  |  Page ", { size: 16, color: "52677A" }), new TextRun({ children: [PageNumber.CURRENT], font: "Microsoft YaHei", size: 16, color: "52677A" })],
            }),
          ],
        }),
      },
      children,
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outPath, buffer);
  console.log(outPath);
});
