import MainLayout from "@/app/components/layout/main-layout";

export default function Layout({children}) {
  return (<MainLayout>
    {children}
  </MainLayout>)
}