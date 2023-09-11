import classNames from "classnames";

const fontColors = {
  primary: "text-indigo-400",
  info: "text-blue-400",
  success: "text-green-400",
  error: "text-red-700"
};
const borderColors = {
  primary: "ring-1 ring-inset ring-indigo-400/30",
  info: "ring-1 ring-inset ring-blue-400/30",
  success: "ring-1 ring-inset ring-green-500/20",
  error: "ring-1 ring-inset ring-red-600/10"
}
const transparentBgColors = {
  primary: "bg-indigo-400/10",
  info: "bg-blue-400/10",
  success: "bg-green-500/10",
  error: "bg-red-400/10"
}
const bgColor = {
  primary: "bg-indigo-50",
  info: "bg-blue-50",
  success: "bg-green-50",
  error: "bg-red-50"
}
const dotColors = {
  primary: "fill-indigo-400",
  info: "fill-blue-400",
  success: "fill-green-400",
  error: "fill-red-400"

};
export default function Badge({
  color,
  dot = false,
  fillBgColor = true,
  transparentBgColor = true,
  withBorder = true,
  children
}) {
  return (<span
      className={
        classNames(
            "inline-flex items-center rounded-md px-2 py-1 text-xs font-medium",
            fontColors[color],
            withBorder && borderColors[color],
            fillBgColor ? transparentBgColor ? transparentBgColors[color]
                : bgColor[color] : null,
            {"gap-x-1.5": dot}
        )
      }>
    {dot && <svg className={classNames("h-1.5 w-1.5", dotColors[color])}
                 viewBox="0 0 6 6"
                 aria-hidden="true">
      <circle cx={3} cy={3} r={3}/>
    </svg>}
    {children}
      </span>);
};