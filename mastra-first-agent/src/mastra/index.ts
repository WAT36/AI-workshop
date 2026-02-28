import { Mastra } from "@mastra/core";
import { myFirstAgent, weatherAgent } from "./agents";

export const mastra = new Mastra({
  agents: {
    myFirstAgent, // ハンズオン１
    weatherAgent, // ハンズオン２
  },
});
