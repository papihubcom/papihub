"use client";
import SiteOptions from "@/app/components/page-sections/site/options";
import Badge from "@/app/components/badge/badge";
import {useListSite} from "@/service/site-service";
import {fToNow} from "@/utils/format-time";

const statusMessage = {
  pending: "待检测",
  active: "可用",
  error: "不可用"
}
const statusColor = {
  pending: "info",
  active: "success",
  error: "error"
}

export default function SiteList() {
  const {data} = useListSite();
  const siteList = data?.data || [];
  return (<ul role="list"
              className="mt-8 grid grid-cols-1 gap-x-6 gap-y-8 lg:grid-cols-3 xl:gap-x-8">
    {siteList && siteList.map((item) => (
        <li key={item.site_id}
            className="overflow-hidden rounded-xl border border-gray-800">
          <div
              className="flex items-center gap-x-4 border-b border-gray-700 bg-gray-900/60 p-6">
            <img
                src={`/icons/pt/${item.site_id}.ico`}
                alt={item.site_name}
                className="h-12 w-12 flex-none rounded-lg bg-gray-900 object-cover ring-1 ring-gray-900/10"
            />
            <div
                className="text-sm font-medium leading-6 text-white">{item.site_name}</div>
            <SiteOptions/>
          </div>
          <dl className="-my-3 divide-y divide-gray-700 px-6 py-4 text-sm leading-6">
            <div className="flex justify-between gap-x-4 py-3">
              <dt className="text-gray-300">上次访问</dt>
              <dd className="text-gray-400">
                <time
                    dateTime={item.last_active_time}>{fToNow(
                    item.last_active_time)}</time>
              </dd>
            </div>
            <div className="flex justify-between gap-x-4 py-3">
              <dt className="text-gray-200">状态</dt>
              <Badge color={statusColor[item.site_status]} dot={true}>
                {statusMessage[item.site_status]}
              </Badge>
            </div>
          </dl>
        </li>
    ))}
  </ul>);
}