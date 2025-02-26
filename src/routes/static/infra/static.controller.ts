import Elysia from "elysia";

import { welcomePage } from "../app/welcome.usecase";
import { listEndpointsPage } from "../app/list-endpoints.usecase";

export const RootController = new Elysia()
  .get("/", () => welcomePage())
  .get("/endpoints", () => listEndpointsPage());
