import { ButtonProps, colorClassMapping } from "./Button.types";
import classNames from 'classnames';
import { MouseEvent } from "react";

export default function Button({ children, light, color, className = '', onClick=() => {}}: ButtonProps) {
  const handleOnClick = (e: MouseEvent<HTMLButtonElement> ) => {
    e.preventDefault()
    onClick(e)
  }

  const btnClass = classNames(colorClassMapping(light)[color], 'py-2 px-4 text-xl rounded-xl', className, {
    'border-2': light,
    'text-white': !light
  })
  return (
    <button
      type="button"
      className={btnClass}
      onClick={handleOnClick}>
      {children}
    </button>
  )
}