import MainLayout from "@/app/components/layout/main";

export default function Layout({children}) {
  return (<MainLayout>
    {children}
  </MainLayout>)
}