import './App.css'

function App() {
  const backendUrl: string = import.meta.env.VITE_BACKEND_HOST;
  console.log(backendUrl)
  return (
    <>
      <h1>Hello blendify!</h1>
      <h2><a href={backendUrl + '/auth/login'}>Log In</a></h2>
      <h2><a href={backendUrl + '/auth/logout'}>Log Out</a></h2>
    </>
  )
}

export default App
