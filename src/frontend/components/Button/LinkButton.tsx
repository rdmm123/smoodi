import { LinkButtonProps, colorClassMapping } from "./Button.types";
import classNames from "classnames";
import { Link } from "react-router-dom";
import { twMerge } from "tailwind-merge";

export default function LinkButton({ children, light, color, to, className: customClasses = '' }: LinkButtonProps) {
    const btnClass = classNames(colorClassMapping(light)[color], 'py-2 px-4 text-xl rounded-xl', {
      'border-2': light,
      'text-white': !light
    });

    const className = twMerge(btnClass, customClasses);

    return <Link
        className={className}
        to={to}>
        {children}
      </Link>;
  }