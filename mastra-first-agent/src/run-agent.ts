import "dotenv/config";
import { mastra } from "./mastra";

async function main() {
  // エージェントの取得
  const agent = mastra.getAgent("myFirstAgent");

  // テキスト生成
  const response = await agent.generate("TypeScriptの利点を3つ教えてください");
  console.log(response.text);

  // ストリーミング生成
  const stream = await agent.stream("Mastraの特徴を説明してください");
  if (Symbol.asyncIterator in stream) {
    for await (const chunk of stream as AsyncIterable<any>) {
      process.stdout.write(chunk.text);
    }
  } else if (Array.isArray(stream)) {
    for (const chunk of stream) {
      process.stdout.write(chunk.text);
    }
  } else {
    process.stdout.write((await stream.text) ?? "");
  }
}

main();
