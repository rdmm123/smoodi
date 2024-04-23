import { ButtonProps, colorClassMapping } from "./Button.types";
import classNames from 'classnames';
import { MouseEvent } from "react";
import { twMerge } from "tailwind-merge";

export default function Button({ children, light, color, className: customClasses = '', onClick=() => {}, type = 'button'}: ButtonProps) {
  const handleOnClick = (e: MouseEvent<HTMLButtonElement> ) => {
    onClick(e)
  }

  const btnClass = classNames(colorClassMapping(light)[color], 'py-2 px-4 text-xl rounded-xl', {
    'border-2': light,
    'text-white': !light
  })

  const className = twMerge(btnClass, customClasses)
  return (
    <button
      type={type}
      className={className}
      onClick={handleOnClick}>
      {children}
    </button>
  )
}