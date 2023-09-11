import Breadcrumbs from "@/app/components/breadcrumbs/breadcrumbs";

export default function MainPageHeader({
  title,
  breadcrumbNavs,
  actions
}) {
  return (<div className="mt-6 sm:mt-12">
    <Breadcrumbs navigation={breadcrumbNavs}/>
    <div className="mt-4 md:flex md:items-center md:justify-between">
      <div className="min-w-0 flex-1">
        <h2 className="text-2xl font-bold leading-7 text-white sm:truncate sm:text-3xl sm:tracking-tight">
          {title}
        </h2>
      </div>
      {actions && <div className="mt-4 flex flex-shrink-0 md:ml-4 md:mt-0">
        {actions}
      </div>}
    </div>
  </div>);
}