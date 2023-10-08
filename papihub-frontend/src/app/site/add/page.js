import SiteEditForm from "@/app/components/page-sections/site/edit-form";
import MainPageHeader from "@/app/components/layout/header/main-page-header";

export default function Page() {
  return (
      <div>
        <MainPageHeader
            title={"添加新站点"}
            breadcrumbNavs={[
              {
                name: '网站配置',
                href: '/site'
              },
              {
                name: '添加新站点',
                href: '#'
              },
            ]}
        />
        <SiteEditForm/>
      </div>
  )
}