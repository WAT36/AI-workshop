import { Mastra } from "@mastra/core";
import { myFirstAgent, weatherAgent } from "./agents";
import { blogWorkflow } from "./workflows";

export const mastra = new Mastra({
  agents: {
    myFirstAgent, // ハンズオン１
    weatherAgent, // ハンズオン２
  },
  workflows: {
    blogWorkflow, // ハンズオン３
  },
});
