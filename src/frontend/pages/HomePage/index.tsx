import { useUserContext } from "contexts/UserContext";
import { CupSoda } from "lucide-react"

function HomePage() {
  const { user } = useUserContext();

  return <div className="flex flex-col justify-center items-center h-full w-2/3 gap-16">
    <div className="flex gap-3 justify-center">
      <CupSoda size={64} />
      <h1 className="text-7xl font-serif">Blendify</h1>
    </div>

    <p className="text-white text-center text-xl">Combine your and your friends' favorite Spotify songs into one awesome playlist.
      Connect your accounts, merge your top tracks, and enjoy a shared music experience.
      Perfect for parties or hangouts!</p>


  </div>
}

export default HomePage;