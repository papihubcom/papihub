"use client";
import useUserStore from "@/auth/store/use-user-store";
import {useCallback, useEffect, useState} from "react";
import {usePathname, useRouter} from "next/navigation";

export const AuthGuard = ({children}) => {
  const router = useRouter();
  const pathname = usePathname();
  const {authenticated, isInitializing} = useUserStore();
  const [checked, setChecked] = useState(false);
  const check = useCallback(async () => {
    if (isInitializing) {
      return;
    }
    if (!authenticated) {
      const params = new URLSearchParams({returnTo: pathname}).toString();
      router.replace(`/auth/login?${params}`);
    } else {
      setChecked(true);
    }
  }, [pathname, authenticated, router, isInitializing]);
  useEffect(() => {
    check();
  }, [check]);
  if (!checked) {
    return null;
  }
  return <>{children}</>;
}