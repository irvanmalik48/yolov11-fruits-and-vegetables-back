import fastJson from "fast-json-stringify";

export interface IWelcomeMessage {
  title: string;
  description: string;
  version: string;
  apiPrefix: string;
  environment: string;
}

export interface IEndpoint {
  title: string;
  route: string;
  method: string;
  description: string;
}

export interface IListEndpoints {
  endpoints: IEndpoint[];
}

export class RootRepository {
  static welcome(): string {
    const welcomeSchema = fastJson({
      title: "Welcome Message Schema",
      type: "object",
      properties: {
        title: { type: "string" },
        description: { type: "string" },
        version: { type: "string" },
        apiPrefix: { type: "string" },
        environment: { type: "string" },
      },
    });

    const message = welcomeSchema<IWelcomeMessage>({
      title: "Arienne-Elysia",
      description: "The backend for Project Arienne. Made in ElysiaJS.",
      version: "1.0.0",
      apiPrefix: "v1",
      environment:
        process.env.BUILD_ENV === "production" ? "production" : "development",
    });

    return message;
  }

  static listEndpoints(): string {
    const listEndpointsSchema = fastJson({
      title: "List Endpoints Schema",
      type: "object",
      properties: {
        endpoints: {
          type: "array",
          items: {
            type: "object",
            properties: {
              title: { type: "string" },
              route: { type: "string" },
              method: { type: "string" },
              description: { type: "string" },
            },
          },
        },
      },
    });

    const message = listEndpointsSchema<IListEndpoints>({
      endpoints: [
        {
          title: "Welcome Message",
          route: "/",
          method: "GET",
          description: "Get the welcome message of the API.",
        },
        {
          title: "List Endpoints",
          route: "/endpoints",
          method: "GET",
          description: "List all the endpoints of the API.",
        },
        {
          title: "Classify Image",
          route: "/classify",
          method: "POST",
          description: "Classify a fruit or vegetable image using the model.",
        },
        {
          title: "Classify (WebSocket)",
          route: "/classify-ws",
          method: "WebSocket",
          description:
            "Classify a fruit or vegetable image using the model through WebSocket.",
        },
      ],
    });

    return message;
  }
}
