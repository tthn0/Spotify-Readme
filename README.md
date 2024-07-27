<div align="center">
  <img src="Images/Spotify.svg" width="100" align="center">
  <h1>Spotify Readme</h1>

[![Badge](https://img.shields.io/github/issues/tthn0/Spotify-Readme?style=for-the-badge)](https://github.com/tthn0/Spotify-Readme/issues)
[![Badge](https://img.shields.io/github/forks/tthn0/Spotify-Readme?style=for-the-badge)](https://github.com/tthn0/Spotify-Readme/network)
[![Badge](https://img.shields.io/github/stars/tthn0/Spotify-Readme?style=for-the-badge)](https://github.com/tthn0/Spotify-Readme/stargazers)

</div>

<p align="center">
  A dynamic, customizable, and real-time Spotify now-playing widget for your markdown files that syncs with the song you’re currently playing. If you're not currently playing a song, it'll display one of your recent songs! Feel free to ask for help or make any pull requests, issues, or suggestions 😄
</p>

## Previews

#### Default

```
/
```

![Preview](https://tthn.pythonanywhere.com)

#### Spinning CD Effect

```
?spin=true
```

![Preview](https://tthn.pythonanywhere.com?spin=true)

#### Include Scan Code

```
?scan=true
```

![Preview](https://tthn.pythonanywhere.com?scan=true)

#### Dark Theme

```
?theme=dark
```

![Preview](https://tthn.pythonanywhere.com?theme=dark)

#### Custom Equalizer

```
?eq_color=0995e0
```

![Preview](https://tthn.pythonanywhere.com?eq_color=0995e0)

#### Rainbow Equalizer

```
?eq_color=rainbow
```

![Preview](https://tthn.pythonanywhere.com?eq_color=rainbow)

#### Combination

```
?spin=true&scan=true&eq_color=rainbow&theme=dark
```

![Preview](https://tthn.pythonanywhere.com?spin=true&scan=true&eq_color=rainbow&theme=dark)

## Setup/Deployment

> [!WARNING]  
> This guide was last updated on Jul 27, 2024. The steps might differ slightly in the future if Spotify or PythonAnywhere update their website interfaces.

> [!NOTE]  
> This will take approximately 5 minutes to set up.

#### 0. Star This Repo (Mandatory) 🌟

- Yes, this step is required.

#### 1. Spotify's API 🎶

- Head over to <a href="https://developer.spotify.com/dashboard/">Spotify for Developers</a>.
  - Accept the Terms of Service if necessary.
  - Verify your email address if you haven't done so already.
  - Click on the **Create app** button.
    - In the **App name** & **App description** fields, you may put whatever you want.
    - In the **Redirect URI** field, add `http://localhost/callback/`.
    - Agree with Spotify's TOS and click **Save**.
  - Click on the **Settings** button.
  - Take note of the **Client ID** & **Client Secret**.

#### 2. Intermediary Steps 🛠️

```
https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&scope=user-read-currently-playing,user-read-recently-played&redirect_uri=http://localhost/callback/
```

- Copy and paste the above link into your browser.
  - Replace `{CLIENT_ID}` with the **Client ID** you got from your Spotify application.
  - Vist the URL.
    - Log in if you're not already signed in.
    - Click **Agree**.
- After you get redirected to a blank page, retrieve the URL from your browser's URL bar. It should be in the following format: `http://localhost/callback/?code={CODE}`.
  - Take note of the `{CODE}` portion of the URL.
- Head over to <a href="https://base64.io">base64.io</a>.
  - Create a string in the form of `{CLIENT_ID}:{CLIENT_SECRET}` and encode it to base 64.
  - Take note of the encoded Base64 string. We'll call this `{BASE_64}`.
- If you're on Windows or don't have the `curl` command, head over to <a href="https://httpie.io/cli/run">httpie.io/cli/run</a>.
  - Press enter.
  - Clear the pre-filled command.
- If you're on Linux or Mac with the `curl` command, open up your preferred terminal.
- Run the following command (replace `{BASE_64}` and `{CODE}` with their respective values):

  ```bash
  curl \
    -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Authorization: Basic {BASE_64}" \
    -d "grant_type=authorization_code&redirect_uri=http://localhost/callback/&code={CODE}" \
    https://accounts.spotify.com/api/token
  ```

- If you did everything correctly, you should get a response in the form of a JSON object.
  - Take note of the `refresh_token`'s value. We'll call this `{REFRESH_TOKEN}`.

#### 3. Host on PythonAnywhere 🐍

- <a href="https://github.com/tthn0/Spotify-Readme/fork">Fork</a> this repository. The new forked repository will be at `https://github.com/{GITHUB_USERNAME}/Spotify-Readme`, where `{GITHUB_USERNAME}` is your GitHub username.
- Head over to <a href="https://www.pythonanywhere.com/pricing/">PythonAnywhere</a>, and `Create a Beginner Account` if you don't already have one. Take note of your username. We'll call this `{PA_USERNAME}`.

  - Complete the PythonAnywhere tour if you'd like to (or skip it).
  - Under `New console:`, click on the `Bash` option.
  - Run the following commands:

    ```bash
    git clone https://github.com/{GITHUB_USERNAME}/Spotify-Readme
    mkvirtualenv --python=/usr/bin/python3.10 venv
    pip install -r Spotify-Readme/Source/requirements.txt
    nano Spotify-Readme/Source/.env
    ```

  - Paste in the following environment variables along with their appropriate values:

    ```bash
    CLIENT_ID="{CLIENT_ID}"
    CLIENT_SECRET="{CLIENT_SECRET}"
    REFRESH_TOKEN="{REFRESH_TOKEN}"
    ```

  - It should look something like this:

    ```bash
    CLIENT_ID="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    CLIENT_SECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    REFRESH_TOKEN="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ```

  - Press `Ctrl + X`, then `Y`, then `Enter` to save the file.
  - Click on the PythonAnywhere logo on the upper left corner to go back to the main dashboard.
  - Click on `Web` in the navigation bar.
  - Click `Add a new web app`.

    - Take note of your web app's domain name.
    - Click `Next »`.
    - Select `Manual configuration`.
    - Select `Python 3.10`.
    - Click `Next »`.

  - Scroll down to the `Code` section.

    - Change the `Source code` field to `/home/{PA_USERNAME}/Spotify-Readme/Source`.
    - Open the `WSGI configuration file` in a new tab and add the following to the bottom of the file:

      ```python
      import sys

      path = '/home/{PA_USERNAME}/Spotify-Readme/Source'
      if path not in sys.path:
          sys.path.append(path)

      from main import app as application
      ```

    - Click `Save` and close out the tab.

  - Back on the `Web` tab, click `Enter path to a virtualenv, if desired`.
    - Type `venv` and click the check mark.
    - This should automatically fill in the field with the correct path to the virtual environment we created earlier.
  - Enable `Force HTTPS`.
  - Scroll back up to the top of the page.
  - Click `Run until 3 months from today`.
  - Click `Reload {PA_USERNAME}.pythonanywhere.com`.
  - Now it's deployed and ready to be used!

<!--

<details>
  <summary>
    <h4>3. (Old) Host on Vercel 🌀</h4>
    <p>
      This project was formerly hosted on Vercel but has since been migrated to PythonAnywhere because there have been issues with deployment.
    </p>
  </summary>

- <a href="https://github.com/tthn0/Spotify-Readme/fork">Fork</a> this repository.
- Head over to <a href="https://vercel.com">Vercel</a> and create an account if you don't already have one.
  - Add a new project.
    - Link your GitHub account if you haven't done so already.
    - Make sure Vercel has access to the forked respository.
    - Import the forked respository into your project.
      - Give it a meaningful project name.
      - Change the Root Directory to `Source`.
      - Keep the default options for the other settings.
      - Add the following environment variables along with their appropriate values:
        - `CLIENT_ID` ⇒ `{CLIENT_ID}`.
        - `CLIENT_SECRET` ⇒ `{CLIENT_SECRET}`.
        - `REFRESH_TOKEN` ⇒ `{REFRESH_TOKEN}`.
      - Click **Deploy**.
      - Click **Continue to Dashboard**.
        - Find the **Domains** field and take note of the URL.
          - Example: `{PROJECT_NAME}.vercel.app`.
- In the next step, reaplce `{USERNAME}.pythonanywhere.com` with `{PROJECT_NAME}.vercel.app` in the markdown code provided.

</details>

-->

#### 4. Add to your GitHub 🚀

- In any markdown file, add the following code:

  ```html
  <a href="https://{PA_USERNAME}.pythonanywhere.com/link">
    <img
      src="https://{PA_USERNAME}.pythonanywhere.com"
      alt="Current Spotify Song"
    />
  </a>
  ```

- Of course, you can append query parameters to the URL to customize the widget!
- Please leave the anchor tag hyperlink reference if you'd to be able to dynamically link your current song, so people listen to the preview. Also, the link helps to retain creator credit and helps others find this project!

## Customization

<p>
  To customize the widget, add query parameters to the endpoint. There are many possible combinations! See how it pairs with other widgets on <a href="https://github.com/tthn0/tthn0">my own README</a>!
</p>

| Parameter  | Default  | Values                                 |
| :--------- | :------- | :------------------------------------- |
| `spin`     | `false`  | `false`, `true`                        |
| `scan`     | `false`  | `false`, `true`                        |
| `theme`    | `light`  | `light`, `dark`                        |
| `eq_color` | `1ED760` | `rainbow`, Any Hex Color w/o Hash Sign |

<!-- | `width` | `N/A` | Coming Soon! | -->

## Keep Your Fork Up To Date

You can keep your fork, and thus your private PythonAnywhere instance up to date, with the upstream using GitHub's <a href="https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork">Sync Fork button</a>! After doing so, log back into your PythonAnywhere account and open a new console to pull in the changes.

## Note

This wasn't a completely original idea. This was inspired by <a href="https://github.com/novatorem/novatorem">novatorem's project</a> that was supposed to be for me only. Since others have asked for the source code, I decided to make this a public repo. I also incorporated the latest two PR's from the orignal project into this one and made it easy to customize!
