import "dotenv/config";
import OpenAI from "openai";
import { observeOpenAI, Langfuse } from "langfuse";

const langfuse = new Langfuse();

async function main() {
  // =============================
  // トレース作成
  // =============================
  const trace = langfuse.trace({
    name: "wrapper-example",
    userId: "user-002",
    tags: ["handson", "wrapper"],
  });

  // =============================
  // OpenAI SDKをLangfuseでラップ
  // =============================
  const openai = observeOpenAI(
    new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    }),
    {
      parent: trace,
      generationName: "openai-wrapped-call",
    }
  );

  // =============================
  // 通常どおりOpenAI APIを呼ぶだけで自動記録
  // =============================
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    temperature: 0.7,
    messages: [
      {
        role: "system",
        content:
          "あなたは優秀なプログラミング講師です。簡潔に回答してください。",
      },
      {
        role: "user",
        content: "TypeScriptのユニオン型の使い方を教えてください。",
      },
    ],
  });

  const output = response.choices[0].message.content;
  console.log(output);

  // =============================
  // フラッシュ
  // =============================
  try {
    await langfuse.flushAsync();
    console.log("✓ Langfuseへのデータ送信が完了しました");
  } catch (error) {
    console.error("✗ Langfuseへのデータ送信に失敗しました:", error);
    // エラーが発生しても処理は続行（データは送信されていないが、アプリケーションは正常終了）
  }
}

main().catch(console.error);
