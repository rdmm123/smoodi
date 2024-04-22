import LinkButton from "components/Button/LinkButton";
import { useUserContext } from "contexts/UserContext";

function HomePage() {
  const { user } = useUserContext();
  
  return user
  ? <>
      <h1 className="text-7xl">Ready to start blendin'?</h1>
      <LinkButton to="/blender" color="green" light={false} className="text-3xl mt-5">Get Started</LinkButton>
    </>
  : <>
      <h1 className="text-7xl">Log in to get started.</h1>
    </>
}

export default HomePage;