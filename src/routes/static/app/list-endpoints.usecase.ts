import { RootRepository } from "../infra/static.repository";

export const listEndpointsPage = (): string => {
  return RootRepository.listEndpoints();
};
