import MainLayout from "@/app/components/layout/main-layout";
import {AuthGuard} from "@/auth/guard/auth-guard";

export default function Layout({children}) {
  return (
      <AuthGuard>
        <MainLayout>
          {children}
        </MainLayout>
      </AuthGuard>
  )
}