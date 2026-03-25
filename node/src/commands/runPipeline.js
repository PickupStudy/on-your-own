import { readEnvFile } from "../utils/env.js";
import { runLearningPipeline } from "../orchestrator/pipelineOrchestrator.js";

export async function runPipeline() {
  readEnvFile();
  const summary = await runLearningPipeline();
  console.log("[pipeline] done");
  console.log(JSON.stringify(summary, null, 2));
}
