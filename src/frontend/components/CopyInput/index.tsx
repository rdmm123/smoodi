interface CopyInputProps {
  text: string,
  className: string
}

export default function CopyInput({ text, className }: CopyInputProps) {
  return <div className={'flex items-center ' + className}>
    <input type="text" className="text-lg p-2 bg-slate-100 text-slate-600 outline outline-2 outline-slate-300 rounded-l-lg grow" value={text} disabled />
    <button
      type="button"
      className="text-lg bg-blue-500 text-white p-2 outline outline-2 outline-blue-500 rounded-r-lg hover:bg-blue-200"
      onClick={() => navigator.clipboard.writeText(text)}>
      Copy
    </button>
  </div>
}