import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import { syncToGitHub } from "../services/syncService.js";
import { getRequiredEnv } from "../utils/env.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PYTHON_CWD = resolve(__dirname, "../../../python");

function runPythonStep(step) {
  return new Promise((resolve, reject) => {
    const child = spawn("python", ["-m", "pkb_processor.cli", step], {
      cwd: PYTHON_CWD,
      stdio: "inherit",
      shell: true
    });

    child.on("exit", (code) => {
      if (code === 0) return resolve();
      reject(new Error(`python step '${step}' failed with code ${code}`));
    });
  });
}

export async function runLearningPipeline() {
  getRequiredEnv("OBSIDIAN_VAULT_PATH");

  await runPythonStep("ingest");
  await runPythonStep("summarize");
  await runPythonStep("bundle");
  const syncResult = await syncToGitHub();

  return {
    ingest: "ok",
    summarize: "ok",
    bundle: "ok",
    sync: syncResult.status
  };
}
