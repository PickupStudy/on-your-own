import { existsSync, statSync } from "node:fs";
import { getEnvFilePath, getRequiredEnv, readEnvFile } from "../utils/env.js";

export async function runDoctor() {
  const envPath = getEnvFilePath();
  if (!existsSync(envPath)) {
    console.log(`[doctor] .env not found: ${envPath}`);
    console.log("[doctor] Copy .env.example to .env and save the file in your editor.");
    return;
  }
  const size = statSync(envPath).size;
  if (size === 0) {
    console.log(`[doctor] .env is empty (0 bytes): ${envPath}`);
    console.log(
      "[doctor] Your editor may have unsaved changes — press Save (Ctrl+S), then run again."
    );
    return;
  }

  readEnvFile();

  const required = [
    "AI_API_KEY",
    "AI_MODEL",
    "GITHUB_TOKEN",
    "GITHUB_REPO",
    "OBSIDIAN_VAULT_PATH"
  ];

  const report = required.map((key) => ({
    key,
    ok: Boolean(getRequiredEnv(key, false))
  }));

  console.log("[doctor] configuration check");
  for (const item of report) {
    console.log(`- ${item.key}: ${item.ok ? "OK" : "MISSING"}`);
  }
}
