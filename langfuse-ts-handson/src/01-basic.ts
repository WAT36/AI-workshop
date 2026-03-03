import "dotenv/config";
import Langfuse from "langfuse";
import OpenAI from "openai";

const langfuse = new Langfuse();
const openai = new OpenAI();

async function main() {
  // =============================
  // トレース作成
  // =============================
  const trace = langfuse.trace({
    name: "simple-qa",
    userId: "user-001",
    metadata: { env: "development" },
    tags: ["handson", "basic"],
  });

  // =============================
  // ユーザー入力
  // =============================
  const userInput = "TypeScriptのジェネリクスについて簡潔に教えてください。";

  // =============================
  // Generation（LLM呼び出し）を記録
  // =============================
  const generation = trace.generation({
    name: "openai-chat",
    model: "gpt-4o-mini",
    modelParameters: { temperature: 0.7 },
    input: [
      { role: "system", content: "あなたは優秀なプログラミング講師です。" },
      { role: "user", content: userInput },
    ],
  });

  // =============================
  // OpenAI API 呼び出し
  // =============================
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    temperature: 0.7,
    messages: [
      { role: "system", content: "あなたは優秀なプログラミング講師です。" },
      { role: "user", content: userInput },
    ],
  });

  const output = response.choices[0].message.content;

  // =============================
  // Generation終了（出力とトークン使用量を記録）
  // =============================
  generation.end({
    output,
    usage: {
      input: response.usage?.prompt_tokens,
      output: response.usage?.completion_tokens,
      total: response.usage?.total_tokens,
    },
  });

  // =============================
  // スコア（ユーザーフィードバック相当）を付与
  // =============================
  trace.score({
    name: "user-feedback",
    value: 1, // 1: good, 0: bad
    comment: "分かりやすい回答だった",
  });

  // =============================
  // バッファをフラッシュ
  // =============================
  await langfuse.flushAsync();

  console.log(output);
}

main().catch(console.error);
