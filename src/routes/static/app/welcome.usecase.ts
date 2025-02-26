import { RootRepository } from "../infra/static.repository";

export const welcomePage = (): string => {
  return RootRepository.welcome();
};
