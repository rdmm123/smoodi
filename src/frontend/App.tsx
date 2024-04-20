export default function App() {
  return (
    <>
      <h1>Hello blendify!</h1>
      <h2><a href={BACKEND_HOST + '/auth/login'}>Log In</a></h2>
      <h2><a href={BACKEND_HOST + '/auth/logout'}>Log Out</a></h2>
      <h1 className="text-3xl font-bold underline">
        Hello world!
      </h1>
    </>
  )
}
