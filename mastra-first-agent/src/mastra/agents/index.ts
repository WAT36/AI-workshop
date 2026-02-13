import { Agent } from "@mastra/core/agent";
import { openai } from "@ai-sdk/openai";
import { getWeatherTool } from "../tools";

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

export const weatherAgent = new Agent({
  id: "weather-agent",
  name: "Weather Agent",
  instructions: `
      あなたは天気情報を提供するアシスタントです。
      ユーザーが天気について質問したら、get-weatherツールを使用して
      天気情報を取得し、分かりやすく伝えてください。
      日本語で応答してください。
    `,
  model: openai("gpt-4o-mini"),
  tools: {
    getWeatherTool,
  },
});
