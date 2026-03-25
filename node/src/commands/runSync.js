import { readEnvFile } from "../utils/env.js";
import { syncToGitHub } from "../services/syncService.js";

export async function runSync() {
  readEnvFile();
  const result = await syncToGitHub();
  console.log("[sync]", result.message);
}
