import AuthLayout from "@/app/components/layout/auth-layout";

export default function Layout({children}) {
  return (<AuthLayout>
    {children}
  </AuthLayout>)
}