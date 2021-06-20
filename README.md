<div align="center">
  <img src="spotify.svg" width="100" align="center">
  <h1>Spotify Readme</h1>

  [![Badge](https://img.shields.io/github/issues/itstommi/Spotify-Readme?style=for-the-badge)](https://github.com/itstommi/Spotify-Readme/issues)
  [![Badge](https://img.shields.io/github/forks/itstommi/Spotify-Readme?style=for-the-badge)](https://github.com/itstommi/Spotify-Readme/network)
  [![Badge](https://img.shields.io/github/stars/itstommi/Spotify-Readme?style=for-the-badge)](https://github.com/itstommi/Spotify-Readme/stargazers)

</div>

<p align="center">
  A dynamic, customizable, and real-time Spotify now-playing widget for your README files. If you're not currently playing a song, it'll display one of your recent songs! It's width is sized like other common README widgets, so can be uniformly paired (<a href="https://github.com/itstommi/itstommi">see it in action</a> on my own README). Feel free to ask for help or make any PRs/issues/suggestions 😄
</p>

## Customization Previews

<p>
  Just add query parameters to the endpoint, there are many possible combinations! (If you're on mobile and your screen is small, please use a desktop browser or change the zoom level to zoom out)
</p>

| Parameter   | Default    | Values          |
| :--------   | :-------   | :-------------- |
| `spin`      | `false`    | `false`, `true` |
| `scan`      | `false`    | `false`, `true` |
| `theme`     | `light`    | `light`, `dark` |
| `rainbow`   | `false`    | `false`, `true` |

#### Default
```
/api
```
![Preview](https://itstommi.vercel.app/api)

#### Spinning CD Effect
```
/api?spin=true
```
![Preview](https://itstommi.vercel.app/api?spin=true)

#### Include Scan Code
```
/api?scan=true
```
![Preview](https://itstommi.vercel.app/api?scan=true)

#### Rainbow Equalizer
```
/api?rainbow=true
```
![Preview](https://itstommi.vercel.app/api?rainbow=true)

#### Dark Theme
```
/api?theme=dark
```
![Preview](https://itstommi.vercel.app/api?theme=dark)

## Notes

This wasn't a completely original idea. This is my own version of <a href="https://github.com/novatorem/novatorem">novatorem's project</a> that was supposed to be for me only, but others have asked for the source code so I made this repo. I also incorporated the latest two PR's from the orignal project into this one and made it easy to customize. I also excluded the <a href="https://github.com/novatorem/novatorem/blob/master/SetUp.md#hide-the-eq-bar">Hide the EQ bar</a> and <a href="https://github.com/novatorem/novatorem/blob/master/SetUp.md#status-string">Status String</a> customizations (sorry). 

## Setup

The setup is slightly different from the original. Please refer to <a href="https://github.com/novatorem/novatorem/blob/master/SetUp.md">this page</a> for the setup, but take notice of these differences:

- Use the <code>/api</code> endpoint as opposed to <code>/api/spotify</code>
- The environment variables are different:
  - `SPOTIFY_CLIENT_ID` ➠ `CLIENT_ID`
  - `SPOTIFY_SECRET_ID` ➠ `CLIENT_SECRET`
  - `SPOTIFY_REFRESH_TOKEN` ➠ `REFRESH_TOKEN`