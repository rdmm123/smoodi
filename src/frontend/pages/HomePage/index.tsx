import { Logo, LogoSize } from "components/Logo";
function HomePage() {
  return <div className="flex flex-col justify-center items-center gap-16 h-full">
    <Logo size={LogoSize.X_X_LARGE} />

    <p className="text-white text-center text-xl">Combine your and your friends' favorite Spotify songs into one awesome playlist.
      Connect your accounts, merge your top tracks, and enjoy a shared music experience.
      Perfect for parties or hangouts!</p>

  </div>
}

export default HomePage;