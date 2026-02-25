import { createStep, createWorkflow } from "@mastra/core/workflows";
import { z } from "zod";
import { myFirstAgent } from "../agents/index-one";

// ステップ1: アウトラインの生成
const generateOutline = createStep({
  id: "generate-outline",
  inputSchema: z.object({
    topic: z.string().describe("ブログ記事のトピック"),
  }),
  outputSchema: z.object({
    outline: z.string(),
  }),
  execute: async ({ inputData }) => {
    const response = await myFirstAgent.generate(
      `以下のトピックについて、ブログ記事のアウトラインを作成してください：${inputData.topic}`
    );
    return { outline: response.text };
  },
});

// ステップ2: 本文の生成
const generateContent = createStep({
  id: "generate-content",
  inputSchema: z.object({
    outline: z.string(),
  }),
  outputSchema: z.object({
    content: z.string(),
  }),
  execute: async ({ inputData }) => {
    const response = await myFirstAgent.generate(
      `以下のアウトラインに基づいて、ブログ記事の本文を作成してください：\n${inputData.outline}`
    );
    return { content: response.text };
  },
});

// ワークフローの定義
export const blogWorkflow = createWorkflow({
  id: "blog-generator",
  inputSchema: z.object({
    topic: z.string(),
  }),
  outputSchema: z.object({
    content: z.string(),
  }),
});

// ステップの連結
blogWorkflow.then(generateOutline).then(generateContent).commit();
