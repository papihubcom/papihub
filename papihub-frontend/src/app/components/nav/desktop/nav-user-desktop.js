"use client"
import {Fragment} from 'react'

import Link from "next/link";
import useUserStore from "@/auth/store/use-user-store";
import {Menu, Transition} from "@headlessui/react";
import classNames from "classnames";
import {ChevronDownIcon} from "@heroicons/react/24/solid";
import {useRouter} from "next/navigation";

export default function NavUserDesktop() {
  const router = useRouter();
  const {authenticated, user, logout} = useUserStore();
  return (<div className="hidden lg:flex lg:flex-1 lg:justify-end">
    {!authenticated && <Link href="/auth/login"
                             className="text-sm font-semibold leading-6 text-white">
      登录 <span aria-hidden="true">&rarr;</span>
    </Link>}
    {authenticated && <Menu as="div" className="relative ml-3">
      <div>
        <Menu.Button
            className="relative flex max-w-xs items-center gap-x-1 rounded-full text-sm focus:outline-none">
          {user?.nickname}
          <ChevronDownIcon className="h-5 w-5" aria-hidden="true"/>
        </Menu.Button>
      </div>
      <Transition
          as={Fragment}
          enter="transition ease-out duration-100"
          enterFrom="transform opacity-0 scale-95"
          enterTo="transform opacity-100 scale-100"
          leave="transition ease-in duration-75"
          leaveFrom="transform opacity-100 scale-100"
          leaveTo="transform opacity-0 scale-95"
      >
        <Menu.Items
            className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
          <Menu.Item>
            {({active}) => (
                <a
                    className={classNames(
                        active ? 'bg-gray-100' : '',
                        'block px-4 py-2 text-sm text-gray-700 cursor-pointer'
                    )}
                    onClick={() => {
                      logout();
                      router.push("/");
                    }}
                >
                  退出
                </a>
            )}
          </Menu.Item>
        </Menu.Items>
      </Transition>
    </Menu>}
  </div>);
}