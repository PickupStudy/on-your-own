import { execSync } from "node:child_process";
import { existsSync } from "node:fs";
import { join } from "node:path";
import { getPkbRoot, getRequiredEnv } from "../utils/env.js";

function runGit(args, cwd, inherit = true) {
  execSync(`git ${args}`, {
    cwd,
    stdio: inherit ? "inherit" : "pipe",
    encoding: "utf8"
  });
}

function normalizeRepoUrl(url) {
  return String(url)
    .trim()
    .replace(/\.git$/i, "")
    .toLowerCase();
}

function ensureGitIdentity(cwd) {
  try {
    execSync("git config user.email", { cwd, stdio: "pipe" });
  } catch {
    execSync('git config user.email "pkb-bot@users.noreply.github.com"', {
      cwd,
      stdio: "ignore"
    });
    execSync('git config user.name "PKB Bot"', { cwd, stdio: "ignore" });
  }
}

function ensureGitRepo(cwd) {
  if (!existsSync(join(cwd, ".git"))) {
    runGit("init", cwd);
  }
  ensureGitIdentity(cwd);
}

function hasCommits(cwd) {
  try {
    execSync("git rev-parse --verify HEAD", { cwd, stdio: "pipe" });
    return true;
  } catch {
    return false;
  }
}

function ensureFirstCommit(cwd) {
  if (hasCommits(cwd)) return;
  runGit(
    'commit --allow-empty -m "chore(pkb): initial commit (empty repo)"',
    cwd,
    true
  );
}

function ensureBranchName(cwd, branch) {
  const target = branch.trim() || "main";
  try {
    runGit(`branch -M ${target}`, cwd, true);
  } catch {
    // ignore if already correct or detached
  }
}

function ensureOriginRemote(cwd, repo) {
  let current = "";
  try {
    current = execSync("git remote get-url origin", {
      cwd,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"]
    }).trim();
  } catch {
    current = "";
  }

  const want = repo.trim();
  if (!current) {
    try {
      runGit(`remote add origin "${want}"`, cwd);
    } catch {
      runGit(`remote set-url origin "${want}"`, cwd);
    }
    return;
  }

  if (normalizeRepoUrl(current) !== normalizeRepoUrl(want)) {
    runGit(`remote set-url origin "${want}"`, cwd);
  }
}

export async function syncToGitHub() {
  const repo = getRequiredEnv("GITHUB_REPO");
  const branch = process.env.GITHUB_BRANCH || "main";
  const cwd = getPkbRoot();

  ensureGitRepo(cwd);
  ensureOriginRemote(cwd, repo);

  try {
    runGit("status --short", cwd, false);
    runGit("add .", cwd, false);
    runGit('commit -m "chore(pkb): auto sync knowledge updates"', cwd, false);
  } catch {
    // 无变更或提交失败时仍尝试 push
  }

  ensureFirstCommit(cwd);
  ensureBranchName(cwd, branch);

  runGit(`push -u origin ${branch}`, cwd, true);
  return { status: "ok", message: "pushed to remote" };
}
