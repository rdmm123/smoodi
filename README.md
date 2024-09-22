# Smoodi
Smoodi is a web aplication built using Spotify’s API. This app allows the users to combine their and their friends top tracks into a single playlist for shared listening. It is designed for users that constantly have shared listening experiences and would like to have a consistent playlist to listen to.

## How it works
Smoodi is built using a React frontend in front of a Flask web server. It uses Oauth 2.0 for user authentication and all of the user information like API tokens is stored safely on the server. The information is stored in a Redis database and is set to be automatically deleted in an hour, so nothing ends up being stored in the backend after the user is done using it.

## How to run it locally
### Requirements
- [Python 3.11 or later](https://www.python.org/downloads/)
- [Node 18 or later](https://nodejs.org/en/download/package-manager)
- [Docker and compose](https://docs.docker.com/engine/install/)
- [Spotify Developer account](https://developer.spotify.com/)

### Spotify API set up steps
Once you have logged in to your spotify developer account, you must:
- [Create a new app](https://developer.spotify.com/dashboard/create) (the big blue button that says create)
- Feel free to use the name you want, although I suggest something remotely related to Smoodi to be able to recognize it
- Set up the redirect uri `http://127.0.0.1:5000/auth/callback`
- Under 'Which API/SDKs are you planning to use?' select 'Web API'
- Accept TOS and create!
- Once your app is created (it will redirect you to the app page), go into the Settings
- Copy your client ID and your client secret (this one will be under 'View client secret') for using it later
- Go into the 'User Management' tab
- Here, you'll want to add the emails of all the users that you're
going to use for testing. I suggest adding at least two, you can use your account and
steal your mom's account or something :p
- That's it! you should be ready to go!

### Ok now how do I run this???!!!
Not so fast! Now you have to do the local set up!

Don't worry, it's not so bad, you simply have to go into [`docker-compose.yml`](./docker-compose.yml) and under the `blendify` service's `environment` and paste your client id and secret that you have (hopefully) stored somewhere safe. 

**NOTE:** Please for anything you love DON'T COMMIT THESE CHANGES. Also please someone else come up with a better way of storing this that doesn't involve manually updating a file that can't be ignored by git. (An .env file does not work since AFAIK Vite will auto-detect it and think it's for the frontend to use.)

### Running the project!

Simply go into your local directory and run `docker compose up`.
It should spin up a development Flask instance and React vite server
on ports 5000 and 5001, respectively.

If you want to use a debugger for the backend, you can change the `target` of the `smoodi` service in [`docker-compose.yml`](./docker-compose.yml) to `debugpy` and set your debugger to remote connection in port 5678. [Here's how to do it in VSCode](https://code.visualstudio.com/docs/python/debugging#_remote-script-debugging-with-ssh), ignore all of the SSH stuff and just do step 3.

### Misc
- To run unit tests simply run `pytest`. There are no js unit tests as of right now.
- To lint you can use `ruff`.
- For JS-related stuff you can use the regular `npm` scripts: `dev`, `build`, `lint`, `preview`

## TODOs and nice to haves
These are things that I think are missing or would be nice to add to the project in the future.
- Serve JS content using a CDN.
- Remove previous Smoodi generated playlists when generating a new one.
- Increase Python's recursion limit to be able to create playlists bigger than 500 songs (this would be a really easy fix).
- Add cool animations and pretty stuff to the UI.
- Add the ability to live-edit the playlist before creating it (re-arrange and remove songs).
- Make the Session page use a web socket to notify of people joining instead of polling the server every 2 seconds.
- Add unit tests for the rest of the backend (only `Blender` has right now).
- Add unit tests for the front end.
- Add a local mock Spotify API service to not depend on an actual Spotify Developer account for local development.
- Implement all the TODOs commented in the code.
- TODO add more TODOs.