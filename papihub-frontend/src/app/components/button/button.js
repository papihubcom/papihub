import classNames from "classnames";

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
      size = 'medium',
      color = 'primary',
      children,
    }
) {
  return (<button
      type="button"
      className={
        classNames(
            colors[color],
            "rounded-md text-sm shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2",
            sizes[size]
        )
      }
  >
    {children}
  </button>);
}