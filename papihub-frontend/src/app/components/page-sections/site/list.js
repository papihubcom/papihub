import SiteOptions from "@/app/components/page-sections/site/options";
import Badge from "@/app/badge/badge";

const statusMessage = {
  success: "可用",
  error: "不可用"
}
const data = [
  {
    id: 1,
    name: '馒头',
    iconUrl: '/icons/pt/mteam.ico',
    lastActiveTime: '8分钟前',
    status: "success"
  },
  {
    id: 2,
    name: '彩虹岛',
    iconUrl: '/icons/pt/chdbits.ico',
    lastActiveTime: '8分钟前',
    status: "success"
  },
  {
    id: 3,
    name: '天空',
    iconUrl: '/icons/pt/hdsky.ico',
    lastActiveTime: '8分钟前',
    status: "success"
  },
]
export default function SiteList() {
  return (<ul role="list"
              className="mt-8 grid grid-cols-1 gap-x-6 gap-y-8 lg:grid-cols-3 xl:gap-x-8">
    {data && data.map((client) => (
        <li key={client.id}
            className="overflow-hidden rounded-xl border border-gray-800">
          <div
              className="flex items-center gap-x-4 border-b border-gray-700 bg-gray-900/60 p-6">
            <img
                src={client.iconUrl}
                alt={client.name}
                className="h-12 w-12 flex-none rounded-lg bg-gray-900 object-cover ring-1 ring-gray-900/10"
            />
            <div
                className="text-sm font-medium leading-6 text-white">{client.name}</div>
            <SiteOptions/>
          </div>
          <dl className="-my-3 divide-y divide-gray-700 px-6 py-4 text-sm leading-6">
            <div className="flex justify-between gap-x-4 py-3">
              <dt className="text-gray-300">上次访问</dt>
              <dd className="text-gray-400">
                <time
                    dateTime={client.lastActiveTime}>{client.lastActiveTime}</time>
              </dd>
            </div>
            <div className="flex justify-between gap-x-4 py-3">
              <dt className="text-gray-200">状态</dt>
              <Badge color={client.status} dot={true}>
                {statusMessage[client.status]}
              </Badge>
            </div>
          </dl>
        </li>
    ))}
  </ul>);
}