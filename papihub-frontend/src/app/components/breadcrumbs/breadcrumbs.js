import {ChevronLeftIcon, ChevronRightIcon} from "@heroicons/react/20/solid";
import Link from "next/link";
import classNames from "classnames";

export default function Breadcrumbs({
  navigation
}) {
  return (
      <div>
        <nav className="sm:hidden" aria-label="Back">
          <Link href="#"
                className="flex items-center text-sm font-medium text-gray-400 hover:text-gray-200">
            <ChevronLeftIcon
                className="-ml-1 mr-1 h-5 w-5 flex-shrink-0 text-gray-500"
                aria-hidden="true"/>
            后退
          </Link>
        </nav>
        <nav className="hidden sm:flex" aria-label="Breadcrumb">
          <ol role="list" className="flex items-center space-x-4">
            {navigation && navigation.map((item, index) => (
                <li key={index}>
                  <div className="flex items-center">
                    {index > 0 ? (
                        <ChevronRightIcon
                            className="flex-shrink-0 h-5 w-5 text-gray-400"
                            aria-hidden="true"/>
                    ) : null}
                    <Link href={item.href}
                          className={classNames(
                              "text-sm font-medium text-gray-400 hover:text-gray-200",
                              {"ml-4": index > 0}
                          )}>
                      {item.name}
                    </Link>
                  </div>
                </li>
            ))}
          </ol>
        </nav>
      </div>)
}