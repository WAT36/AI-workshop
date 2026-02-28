import { createTool } from "@mastra/core/tools";
import { z } from "zod";

// 天気を取得するツール（モック）
export const getWeatherTool = createTool({
  id: "get-weather",
  description: "指定された都市の現在の天気を取得します",
  inputSchema: z.object({
    city: z.string().describe("天気を取得したい都市名"),
  }),
  outputSchema: z.object({
    city: z.string(),
    temperature: z.number(),
    condition: z.string(),
  }),
  execute: async (context) => {
    const { city } = context;

    // 実際のアプリケーションでは外部APIを呼び出します
    // ここではモックデータを返します
    const mockWeatherData: Record<
      string,
      { temperature: number; condition: string }
    > = {
      東京: { temperature: 22, condition: "晴れ" },
      大阪: { temperature: 24, condition: "曇り" },
      札幌: { temperature: 15, condition: "雨" },
    };

    const weather = mockWeatherData[city] || {
      temperature: 20,
      condition: "不明",
    };

    return {
      city,
      temperature: weather.temperature,
      condition: weather.condition,
    };
  },
});
