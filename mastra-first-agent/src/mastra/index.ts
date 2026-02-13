import { Mastra } from "@mastra/core/mastra";
import { myFirstAgent } from "./agents";

export const mastra = new Mastra({
  agents: { myFirstAgent },
});
