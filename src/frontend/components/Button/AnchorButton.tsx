import { AnchorButtonProps, colorClassMapping } from "./Button.types";
import classNames from 'classnames';

export default function AnchorButton({ children, light, color, href, className = '' }: AnchorButtonProps) {
  const btnClass = classNames(colorClassMapping(light)[color], 'py-2 px-4 text-xl rounded-xl', className, {
    'border-2': light,
    'text-white': !light
  })
  return (
    <a
      className={btnClass}
      href={href}>
      {children}
    </a>
  )
}