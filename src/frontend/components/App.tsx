import './App.css'

function App() {
  return (
    <>
      <h1>Hello blendify!</h1>
      <h2><a href={BACKEND_HOST + '/auth/login'}>Log In</a></h2>
      <h2><a href={BACKEND_HOST + '/auth/logout'}>Log Out</a></h2>
    </>
  )
}

export default App
