import Elysia from "elysia";

import { RootController } from "./routes/static/infra/static.controller";

const routes = new Elysia({ prefix: "v1" }).use(RootController);

export { routes as AppRoutes };
