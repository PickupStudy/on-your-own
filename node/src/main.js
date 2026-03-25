import { runCommand } from "./commands/index.js";

async function main() {
  const [, , command = "help", ...args] = process.argv;

  try {
    await runCommand(command, args);
  } catch (error) {
    console.error("[pkb] command failed:", error.message);
    process.exitCode = 1;
  }
}

main();
