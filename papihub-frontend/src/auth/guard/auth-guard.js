"use client";
import {useRouter} from "next/router";
import useUserStore from "@/auth/store/use-user-store";
import {useCallback, useEffect, useState} from "react";
import {usePathname} from "next/navigation";

export const AuthGuard = ({children}) => {
  const router = useRouter();
  const pathname = usePathname();
  const {authenticated} = useUserStore();
  const [checked, setChecked] = useState(false);
  const check = useCallback(() => {
    if (authenticated) {
      setChecked(true);
    } else {
      const params = new URLSearchParams({returnTo: pathname}).toString();
      router.replace(`/auth/login?${params}`);
    }
  }, [pathname, authenticated, router]);
  useEffect(() => {
    check();
  }, [check]);
  if (!check()) {
    return null;
  }
  return <>{children}</>;
}