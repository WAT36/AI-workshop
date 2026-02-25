import { Mastra } from "@mastra/core/mastra";
import { myFirstAgent, weatherAgent } from "./agents/index-two";
import { blogWorkflow } from "./workflows";

export const mastra = new Mastra({
  //agents: { myFirstAgent },
  agents: { weatherAgent },
  workflows: { blogWorkflow },
});
