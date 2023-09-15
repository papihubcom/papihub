"use client"
import useUserStore from "@/auth/store/use-user-store";
import {useEffect, useState} from "react";

export default function AuthProvider({children}) {
  const {authenticated, isInitializing, initializeMethod} = useUserStore();
  const [checked, setChecked] = useState(false);
  useEffect(() => {
    if (!isInitializing) {
      return;
    }
    initializeMethod();
  }, [initializeMethod, isInitializing]);
  return (
      <>
        {children}
      </>
  );
}