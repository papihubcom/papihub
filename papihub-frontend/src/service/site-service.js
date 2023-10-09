import useHttp from "@/hooks/use-http";
import {useMutation, useQuery} from "react-query";

export const useListParsers = (param) => {
  const client = useHttp();
  return useQuery(['list_parsers', param], () =>
      client("/api/site/list_parsers", {params: param})
  );
};
export const useListSite = (param) => {
  const client = useHttp();
  return useQuery(['list_site', param], () =>
      client("/api/site/list", {params: param})
  );
};
export const useAddSite = (param) => {
  const client = useHttp();
  return useMutation(
      (params) =>
          client("/api/site/add", {params: params, method: "POST"})
  );
};