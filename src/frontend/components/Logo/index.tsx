import { CupSoda } from "lucide-react";

export enum LogoSize {
  SMALL = 's',
  MEDIUM = 'm',
  LARGE = 'l',
  X_LARGE = 'xl',
  X_X_LARGE = 'xxl'
}

interface LogoProps {
  size: LogoSize
}

export function Logo({ size }: LogoProps) {
  let gapSize: string, iconSize: number, fontSize: string;

  if (size === LogoSize.SMALL) {
    gapSize = 'gap-1';
    iconSize = 30;
    fontSize =  'text-lg'
  } else if (size == LogoSize.MEDIUM) {
    gapSize = 'gap-2';
    iconSize = 32;
    fontSize =  'text-2xl'
  } else if (size == LogoSize.LARGE) {
    gapSize = 'gap-2';
    iconSize = 40;
    fontSize =  'text-3xl'
  } else if (size == LogoSize.X_LARGE) {
    gapSize = 'gap-3';
    iconSize = 48;
    fontSize =  'text-4xl'
  } else if (size == LogoSize.X_X_LARGE) {
    gapSize = 'gap-3';
    iconSize = 88;
    fontSize =  'text-7xl'
  } else {
    return;
  }

  return <div className={`flex items-end text-my-rose ${gapSize}`}>
    <CupSoda size={iconSize} />
    <h1 className={`${fontSize} font-serif`}>Blendify</h1>
  </div>
}