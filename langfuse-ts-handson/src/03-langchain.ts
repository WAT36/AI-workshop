import "dotenv/config";
import { CallbackHandler } from "langfuse-langchain";
import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";

async function main() {
  // =============================
  // Langfuseコールバックハンドラ
  // =============================
  const langfuseHandler = new CallbackHandler({
    userId: "user-003",
    tags: ["handson", "langchain"],
  });

  // =============================
  // LangChain構成
  // =============================
  const prompt = ChatPromptTemplate.fromMessages([
    ["system", "あなたは優秀なプログラミング講師です。"],
    ["user", "{question}"],
  ]);

  const model = new ChatOpenAI({
    modelName: "gpt-4o-mini",
    temperature: 0.7,
  });

  const parser = new StringOutputParser();

  const chain = prompt.pipe(model).pipe(parser);

  // =============================
  // 実行（callbacksにハンドラを渡すだけ）
  // =============================
  const result = await chain.invoke(
    { question: "TypeScriptの型ガードについて教えてください。" },
    { callbacks: [langfuseHandler] }
  );

  console.log(result);

  // =============================
  // フラッシュ
  // =============================
  await langfuseHandler.flushAsync();
}

main().catch(console.error);
