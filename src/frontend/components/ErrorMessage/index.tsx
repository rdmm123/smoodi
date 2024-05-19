interface ErrorMessageProps {
  message: string
}

export default function ErrorMessage({ message }: ErrorMessageProps) {
  return (
    <div className="bg-red-200 outline outline-1 outline-red-500 text-red-500 rounded-xl p-3 text-center mb-5">
      <p className="text-lg">{message}</p>
    </div>
  )
}