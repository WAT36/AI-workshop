import { Agent } from "@mastra/core/agent";
import { openai } from "@ai-sdk/openai";

// エージェントの定義
export const myFirstAgent = new Agent({
  id: "my-first-agent",
  name: "My First Agent",
  instructions: `
    あなたは親切で丁寧なアシスタントです。
    ユーザーの質問に対して、分かりやすく回答してください。
    日本語で応答してください。
  `,
  model: openai("gpt-4o-mini"),
});
