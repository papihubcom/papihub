"use client";
import React from 'react';
import {QueryClient, QueryClientProvider} from "react-query";

export const QueryProvider = ({children}) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
      },
    },
  });

  return (
      <QueryClientProvider client={queryClient}>
        {children}
        {/*<ReactQueryDevtools initialIsOpen={false} />*/}
      </QueryClientProvider>
  );

};
