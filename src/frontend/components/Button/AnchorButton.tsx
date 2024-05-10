import { AnchorButtonProps, colorClassMapping } from "./Button.types";
import classNames from 'classnames';
import { twMerge } from "tailwind-merge";

export default function AnchorButton({ children, light, color, href, target, className: customClasses = '' }: AnchorButtonProps) {
  const btnClass = classNames(colorClassMapping(light)[color], 'py-2 px-4 text-xl rounded-xl', {
    'border-2': light,
    'text-white': !light
  })
  const className = twMerge(btnClass, customClasses);
  return (
    <a
      className={className}
      href={href}
      target={target}
    >
      {children}
    </a>
  )
}