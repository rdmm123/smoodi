import { useState, useEffect } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Copy, Check } from "lucide-react"

interface CopyInputProps {
  text: string
}

export default function CopyInput({ text }: CopyInputProps) {
  const [isCopied, setIsCopied] = useState(false);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setIsCopied(true);
    } catch (error) {
      console.error(error);
      setIsCopied(false);
    }
  }

  useEffect(() => {
    if (!isCopied) return;
    setTimeout(() => setIsCopied(false), 1000)
  }, [isCopied])

  return <div className="flex items-center space-x-2">
    <Input className="border-2 border-my-green bg-my-green-100 text-my-purple" placeholder={text} readOnly />
    
    <Button type="button" onClick={copyToClipboard}>
      {isCopied ? <Check /> : <Copy />}
    </Button>
  </div>
}