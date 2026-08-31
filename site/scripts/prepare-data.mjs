import { gunzipSync } from "node:zlib";
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const siteRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const projectRoot = resolve(siteRoot, "..");
const phase2Run = "20260830T155412Z__phase2__8fbf10";
const phase3Run = "20260830T230045Z__phase3__74142b";

const labels = {
  "anthropic/claude-sonnet-5": "Claude Sonnet 5",
  "deepseek/deepseek-v4-pro-0813": "DeepSeek V4 Pro",
  "google/gemini-2.5-flash-lite": "Gemini 2.5 Flash Lite",
  "meta-llama/llama-3.3-70b-instruct": "Llama 3.3 70B",
  "mistralai/mistral-medium-3.1": "Mistral Medium 3.1",
  "openai/gpt-5.4-mini": "GPT-5.4 mini",
  "qwen/qwen3.8-27b": "Qwen 3.8 27B",
  "x-ai/grok-4.20": "Grok 4.20",
  "z-ai/glm-5.2": "GLM 5.2",
};

const scaleInfo = {
  "ggb.impartial_beneficence": {
    label: "Helping beyond one’s circle",
    plain: "How strongly a response supports personal sacrifice to help people in serious need, including strangers.",
  },
  "ggb.instrumental_harm": {
    label: "Using harm for a larger goal",
    plain: "How willing a response is to accept harming one person to produce a larger benefit. Lower scores mean more reluctance to use harm.",
  },
  "mfq2.care": { label: "Care", plain: "Concern for people who are suffering." },
  "mfq2.equality": { label: "Equality", plain: "Preference for more equal outcomes and resources." },
  "mfq2.proportionality": { label: "Proportionality", plain: "Preference for rewards that track contribution or effort." },
  "mfq2.loyalty": { label: "Loyalty", plain: "Importance placed on commitment to one’s group or community." },
  "mfq2.authority": { label: "Authority", plain: "Importance placed on tradition, rules, and legitimate authority." },
  "mfq2.purity": { label: "Purity", plain: "Importance placed on ideas of sanctity, restraint, and contamination." },
};

// The fast path deliberately uses short, non-graphic statements. The deeper path adds
// published applied cases, but stays inside the completed Phase 2 item bank so every
// displayed comparison can use an answer from all nine models.
const quickQuestionIds = [
  "ggb_013", "ggb_016", "ggb_017", "ggb_020", "mfq2_001",
  "mfq2_002", "mfq2_003", "mfq2_010", "mfq2_005", "mfq2_006",
];

const detailedQuestionIds = [
  ...quickQuestionIds,
  "mfq2_007", "mfq2_008", "mfq2_009", "mfq2_011", "mfq2_013", "mfq2_014",
  "mfq2_015", "mfq2_016", "mfq2_017", "mfq2_018", "mfq2_019", "mfq2_020",
  "ggb_018", "ggb_019", "ggb_021", "ggb_022", "ggb_023", "ggb_024",
  "ethics_commonsense_012", "ethics_commonsense_016", "ethics_commonsense_017",
  "ethics_commonsense_022", "ethics_commonsense_024",
];

const sourceInfo = {
  ous_ggb: {
    label: "Greatest Good Benchmark",
    plain: "A published LLM benchmark adapted from the Oxford Utilitarianism Scale. These statements probe costly helping and hard trade-offs; they are not moral-answer keys.",
  },
  mfq2_phase2: {
    label: "Moral Foundations Questionnaire-2",
    plain: "A published moral-psychology questionnaire. These are self-report statements about the kinds of moral considerations a person finds important.",
  },
  ethics_phase2: {
    label: "ETHICS",
    plain: "A published benchmark of everyday moral judgments. The detailed form includes a small number of its longer, context-rich cases.",
  },
};

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function readCsv(path) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;
  const text = readFileSync(path, "utf8").replace(/\r\n/g, "\n");
  for (let index = 0; index <= text.length; index += 1) {
    const char = text[index] ?? "\n";
    if (char === '"') {
      if (quoted && text[index + 1] === '"') {
        cell += '"';
        index += 1;
      } else {
        quoted = !quoted;
      }
    } else if (char === "," && !quoted) {
      row.push(cell);
      cell = "";
    } else if (char === "\n" && !quoted) {
      row.push(cell);
      if (row.some((value) => value !== "")) rows.push(row);
      row = [];
      cell = "";
    } else {
      cell += char;
    }
  }
  const [headers, ...values] = rows;
  return values.map((line) => Object.fromEntries(headers.map((header, index) => [header, line[index] ?? ""])));
}

function optionFor(document, item) {
  return item.options ?? document.options;
}

function loadItems() {
  const files = ["ous_ggb.yaml", "mfq2_phase2.yaml", "ethics_phase2.yaml", "ipip_neo_120.yaml"];
  const items = [];
  for (const filename of files) {
    const document = readJson(join(projectRoot, "instruments", filename));
    for (const item of document.items) {
      items.push({
        id: item.id,
        scale: item.scale,
        instrument: document.instrument,
        text: item.text,
        options: optionFor(document, item).map(({ id, label, value }) => ({ id, label, value })),
      });
    }
  }
  return items;
}

function numeric(value) {
  return value === "" || value === undefined ? null : Number(value);
}

const items = loadItems();
const itemById = new Map(items.map((item) => [item.id, item]));
const scaleRows = readCsv(join(projectRoot, "data", "derived", phase2Run, "scale_scores.csv"));
const modelRows = readCsv(join(projectRoot, "data", "derived", phase2Run, "model_overview.csv"));
const phase3Rows = readCsv(join(projectRoot, "data", "derived", phase3Run, "domain_summary.csv"));
const selectedScaleRows = scaleRows
  .filter((row) => row.condition === "bare" && row.framing === "first_person" && row.score_type === "value")
  .filter((row) => Object.hasOwn(scaleInfo, row.scale))
  .map((row) => ({ ...row, score: numeric(row.score), ciLow: numeric(row.ci_low), ciHigh: numeric(row.ci_high) }));

const models = Object.entries(labels).map(([id, label]) => ({
  id,
  slug: id.replace(/[^a-z0-9]+/gi, "-").replace(/^-|-$/g, ""),
  label,
  overview: modelRows.find((row) => row.model_id === id),
  scores: selectedScaleRows.filter((row) => row.model_id === id),
  phase3: phase3Rows
    .filter((row) => row.model_id === id)
    .map((row) => ({
      domain: row.domain,
      meanBehavior: numeric(row.mean_behavior),
      surfaceGap: numeric(row.mean_surface_gap),
      positionFragility: numeric(row.mean_position_fragility),
      eligible: numeric(row.prediction_eligible),
      judged: numeric(row.judged),
      concordant: numeric(row.concordant),
    })),
  itemScores: {},
}));

const exactResponses = [];
const itemValueSamples = new Map(Object.keys(labels).map((modelId) => [modelId, new Map()]));
for (const filename of readdirSync(join(projectRoot, "data", "raw", phase2Run)).filter((name) => name.endsWith(".jsonl.gz"))) {
  const raw = gunzipSync(readFileSync(join(projectRoot, "data", "raw", phase2Run, filename))).toString("utf8");
  for (const line of raw.trim().split("\n")) {
    const record = JSON.parse(line);
    if (!itemById.has(record.item_id) || !Object.hasOwn(labels, record.model_id)) continue;
    const item = itemById.get(record.item_id);
    if (record.condition === "bare" && record.framing === "first_person" && record.parsed?.choice) {
      const selected = item.options.find((option) => option.id === record.parsed.choice);
      if (selected) {
        const modelValues = itemValueSamples.get(record.model_id);
        const samples = modelValues.get(record.item_id) ?? [];
        samples.push(selected.value);
        modelValues.set(record.item_id, samples);
      }
    }
    if (record.condition !== "bare" || record.framing !== "first_person" || record.permutation !== 0) continue;
    exactResponses.push({
      modelId: record.model_id,
      itemId: record.item_id,
      rawResponse: record.raw_response,
      parsedChoice: record.parsed?.choice ?? null,
      optionOrder: record.option_order,
      prompt: record.messages.at(-1)?.content ?? "",
    });
  }
}

for (const model of models) {
  const scores = itemValueSamples.get(model.id);
  model.itemScores = Object.fromEntries(
    [...scores.entries()].map(([itemId, values]) => [
      itemId,
      values.reduce((total, value) => total + value, 0) / values.length,
    ]),
  );
}

function questionForForm(id) {
  const item = itemById.get(id);
  if (!item) throw new Error(`Unknown human-form item: ${id}`);
  return { ...item, source: sourceInfo[item.instrument] };
}

const output = {
  phase2Run,
  phase3Run,
  generatedAt: new Date().toISOString(),
  scaleInfo,
  models,
  items,
  questionSets: {
    quick: {
      label: "Quick reflection",
      duration: "about 3 minutes",
      plain: "Ten concise statements across helping, fairness, community, and tradition.",
      questions: quickQuestionIds.map(questionForForm),
    },
    detailed: {
      label: "Deeper reflection",
      duration: "about 12 minutes",
      plain: "Thirty-three sourced prompts, including longer everyday cases with competing considerations.",
      questions: detailedQuestionIds.map(questionForForm),
    },
  },
  exactResponses,
};

const generatedPath = join(siteRoot, "src", "data", "generated.json");
mkdirSync(dirname(generatedPath), { recursive: true });
writeFileSync(generatedPath, JSON.stringify(output), "utf8");
console.log(`Prepared ${models.length} model profiles and ${exactResponses.length} exact responses.`);
