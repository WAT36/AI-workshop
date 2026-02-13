import { Mastra } from "@mastra/core/mastra";
import { myFirstAgent, weatherAgent } from "./agents";

export const mastra = new Mastra({
  //agents: { myFirstAgent },
  agents: { weatherAgent },
});
