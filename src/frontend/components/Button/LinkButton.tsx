import { LinkButtonProps, colorClassMapping } from "./Button.types";
import classNames from "classnames";
import { Link } from "react-router-dom";

export default function LinkButton({ children, light, color, to, className = '' }: LinkButtonProps) {
    
  
    const btnClass = classNames(colorClassMapping(light)[color], 'py-2 px-4 text-xl rounded-xl', className, {
      'border-2': light,
      'text-white': !light
    })
    return (
      <Link
        className={btnClass}
        to={to}>
        {children}
      </Link>
    )
  }