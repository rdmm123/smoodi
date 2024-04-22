import React from "react"

type ButtonColor = 'blue' | 'red' | 'green';

export const colorClassMapping = (light: boolean) => ({
    red: light ? 'text-red-500 border-red-500 hover:bg-red-100' : 'bg-red-500 hover:bg-red-700',
    blue: light ? 'text-blue-500 border-blue-500 hover:bg-blue-100' : 'bg-blue-500 hover:bg-blue-700',
    green: light ? 'text-green-500 border-green-500 hover:bg-green-100' : 'bg-green-500 hover:bg-green-700',
});

export interface ButtonProps {
    children?: React.ReactNode,
    color: ButtonColor,
    light: boolean,
    className?: string
}

export interface LinkButtonProps extends ButtonProps {
    to: string
}

export interface AnchorButtonProps extends ButtonProps {
    href: string
}