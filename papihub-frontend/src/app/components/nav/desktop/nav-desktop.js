import Link from "next/link";

export default function NavDesktop({data}) {
  return (<>
    {data.map((item) => (
        <Link key={item.name} href={item.href}
           className="text-sm font-semibold leading-6 text-white">
          {item.name}
        </Link>
    ))}
  </>);
}