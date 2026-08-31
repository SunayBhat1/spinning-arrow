import { readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const siteRoot = fileURLToPath(new URL("..", import.meta.url));
const data = JSON.parse(readFileSync(join(siteRoot, "src", "data", "generated.json"), "utf8"));
const expectedCounts = { quick: 10, detailed: 33 };

for (const [name, expectedCount] of Object.entries(expectedCounts)) {
  const set = data.questionSets[name];
  if (!set || set.questions.length !== expectedCount) {
    throw new Error(`${name} profile must contain exactly ${expectedCount} questions`);
  }
  const ids = set.questions.map((question) => question.id);
  if (new Set(ids).size !== ids.length) throw new Error(`${name} profile contains duplicate questions`);
  for (const question of set.questions) {
    if (!question.source?.label || !question.source?.plain) {
      throw new Error(`${name} profile question ${question.id} is missing provenance`);
    }
  }
  for (const model of data.models) {
    const missing = ids.filter((id) => !Number.isFinite(Number(model.itemScores[id])));
    if (missing.length) {
      throw new Error(`${model.id} lacks item-level answers for ${name}: ${missing.join(", ")}`);
    }
  }
}

console.log(`Verified ${data.models.length} models against both human-form question sets.`);
