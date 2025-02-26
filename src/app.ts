import { Elysia } from "elysia";
import { node } from "@elysiajs/node";
import fastJson from "fast-json-stringify";
import { AppRoutes } from "./app.routes";

const app = new Elysia({ adapter: node() }).use(AppRoutes).get("/", () => {
  const wrongRootSchema = fastJson({
    title: "You are in the wrong place",
    type: "object",
    properties: {
      prefix: { type: "string" },
      message: { type: "string" },
      visit: { type: "string" },
    },
  });

  const message = wrongRootSchema({
    prefix: "v1",
    message: "You are in the wrong root route. Please visit `/v1`.",
    visit: "/v1",
  });

  if (process.env.NODE_ENV === "development")
    console.log("[A-E] `/` accessed. You shouldn't be here.");

  return message;
});

app.listen(5128, () => {
  console.log(`[A-E] Server is running on port 5128.`);
});
