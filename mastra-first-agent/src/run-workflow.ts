import "dotenv/config";
import { mastra } from "./mastra";

async function main() {
  const workflow = mastra.getWorkflow("blogWorkflow");

  const run = await workflow.createRun();
  const result = await run.start({
    inputData: {
      topic: "TypeScriptの型システムの魅力",
    },
  });

  console.log(result);
}

main();
