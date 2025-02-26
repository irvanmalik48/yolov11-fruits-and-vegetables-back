import { Elysia } from "elysia";
import { node } from "@elysiajs/node";
import { AppRoutes } from "./app.routes";

const app = new Elysia({ adapter: node() }).use(AppRoutes);

app.listen(5128, () => {
  console.log(
    `[A-E] Server is running on port ${app.server?.hostname}:${app.server?.port}`
  );
});
