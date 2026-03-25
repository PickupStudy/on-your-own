import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

/** pkb-core 根目录（与 .env 同级），不依赖 process.cwd */
export function getPkbRoot() {
  const here = dirname(fileURLToPath(import.meta.url));
  return resolve(here, "../../..");
}

function stripQuotes(value) {
  const v = value.trim();
  if (v.length >= 2) {
    const a = v[0];
    const b = v[v.length - 1];
    if ((a === '"' && b === '"') || (a === "'" && b === "'")) {
      return v.slice(1, -1);
    }
  }
  return v;
}

function parseEnvLine(line) {
  const trimmed = line.trim();
  if (!trimmed || trimmed.startsWith("#")) return null;
  const idx = trimmed.indexOf("=");
  if (idx < 0) return null;
  const key = trimmed.slice(0, idx).trim();
  if (!key) return null;
  const rawValue = trimmed.slice(idx + 1).trim();
  return { key, value: stripQuotes(rawValue) };
}

export function getEnvFilePath() {
  return resolve(getPkbRoot(), ".env");
}

export function readEnvFile() {
  const envPath = getEnvFilePath();
  if (!existsSync(envPath)) return;

  let raw = readFileSync(envPath, "utf8");
  if (!raw.length) {
    return;
  }
  if (raw.charCodeAt(0) === 0xfeff) {
    raw = raw.slice(1);
  }

  for (const line of raw.split(/\r?\n/)) {
    const parsed = parseEnvLine(line);
    if (!parsed) continue;
    const { key, value } = parsed;
    const current = process.env[key];
    if (current === undefined || current === "") {
      process.env[key] = value;
    }
  }
}

export function getRequiredEnv(key, throwOnMissing = true) {
  const value = process.env[key];
  if (!value && throwOnMissing) {
    throw new Error(`missing required env: ${key}`);
  }
  return value;
}
