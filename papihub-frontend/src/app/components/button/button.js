"use client";
import classNames from "classnames";
import {useRouter} from "next/navigation";

const sizes = {
  small: "px-2.5 py-1.5 text-sm",
  medium: "px-3 py-2 text-sm",
  large: "px-3.5 py-2.5 text-sm",
}
const colors = {
  primary: "bg-indigo-500 hover:bg-indigo-400 focus-visible:outline-indigo-500 text-white",
  secondary: "bg-white/10 hover:bg-white/20 text-white",
}
export default function Button(
    {
      type = 'button',
      size = 'medium',
      color = 'primary',
      className = null,
      href = null,
      onClick,
      disabled,
      children,
    }
) {
  const router = useRouter();
  const handleClick = (e) => {
    if (href) {
      e.preventDefault();
      router.push(href);
    } else if (onClick) {
      onClick(e);
    }
  }
  return (<button
      type={type}
      onClick={handleClick}
      className={
        classNames(
            colors[color],
            "rounded-md text-sm shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2",
            sizes[size],
            {"cursor-not-allowed opacity-50": disabled},
            className
        )
      }
  >
    {children}
  </button>);
}