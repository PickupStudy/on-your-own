import { runDoctor } from "./runDoctor.js";
import { runPipeline } from "./runPipeline.js";
import { runSync } from "./runSync.js";

export async function runCommand(command, args) {
  switch (command) {
    case "doctor":
      return runDoctor();
    case "sync":
      return runSync();
    case "pipeline":
      return runPipeline();
    case "help":
    default:
      return printHelp(args);
  }
}

function printHelp() {
  console.log(`
PKB commands:
  doctor      检查本地环境与配置
  sync        触发 Git 同步
  pipeline    运行完整流程（ingest -> summarize -> bundle -> sync）
`);
}
