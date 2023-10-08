import MainPageHeader from "@/app/components/layout/header/main-page-header";
import Button from "@/app/components/button/button";
import SiteList from "@/app/components/page-sections/site/list";

export const metadata = {
  title: '网站配置 | PapiHub',
  description: '配置系统内可以抓取访问的站点。',
}
export default function Page() {

  return (<div>
    <MainPageHeader
        title={"网站配置"}
        breadcrumbNavs={[
          {
            name: '网站配置',
            href: '/site'
          },
          {
            name: '列表',
            href: '#'
          },
        ]}
        actions={<Button size="small" href={"/site/add"} >添加站点</Button>}
    />
    <SiteList/>
  </div>)
}