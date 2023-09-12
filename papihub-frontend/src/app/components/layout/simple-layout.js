import NavMobile from "@/app/components/nav/mobile/nav-mobile";
import NavDesktop from "@/app/components/nav/desktop/nav-desktop";
import Footer from "@/app/components/footer/footer";
import Link from "next/link";

const navigation = [
  {name: '首页', href: '/'},
  {name: '网站配置', href: '/site'},
  {name: '使用接口', href: '/apidoc'},
]
export default function SimpleLayout({children}) {
  return (<div>
    {/* Header */}
    <header className="absolute inset-x-0 top-0 z-50">
      <nav className="flex items-center justify-between p-6 lg:px-8"
           aria-label="Global">
        <div className="flex lg:flex-1">
          <a href="#" className="-m-1.5 p-1.5">
            <span className="sr-only">PapiHub</span>
            <img
                className="h-8 w-auto"
                src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=500"
                alt=""
            />
          </a>
        </div>
        <div className="flex lg:hidden">
          <NavMobile data={navigation}/>
        </div>
        <div className="hidden lg:flex lg:gap-x-12">
          <NavDesktop data={navigation}/>
        </div>
        <div className="hidden lg:flex lg:flex-1 lg:justify-end">
          <Link href="/auth/login"
                className="text-sm font-semibold leading-6 text-white">
            登录 <span aria-hidden="true">&rarr;</span>
          </Link>
        </div>
      </nav>

    </header>
    <main>
      {children}
    </main>
    {/* Footer */}
    <Footer/>
  </div>)
}