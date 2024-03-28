# Py GogoAnime API
A flask based Python API which extracts data from GogoAnime and serves it. It is heavily inspired from [this](https://github.com/riimuru/gogoanime-api/) similar nodejs project.
## Disclaimer
This is just a small part time project which I created in my free time and I do not support piracy. Please do not use it to create streaming websites as it is also not very efficient, Because for each API call, one or more request goes to GogoAnime server (A lot of traffic might result in GogoAnime blocking requests from your API server's IP). Only use this repo to learn flask and how bs4 library may be used for web scraping, **If you do otherwise, you will be the only person responsible for it.**

## Table of Contents

- [Installation](#installation)
  - [Windows & Linux](#Windows--Linux)
  - [Android (Termux)](#android-termux)
- [Routes](#routes)
  - [Get Recent Episodes](#get-recent-episodes)
  - [Get Popular Anime](#get-popular-anime)
  - [Get Anime Search](#get-anime-search)
  - [Get Anime Movies](#get-anime-movies)
  - [Get Anime Details](#get-anime-details)
  - [Get Streaming URLs](#get-streaming-urls)



## Installation

### Windows & Linux
Download and install Python, make sure to add it to PATH. Now, if you have git installed, run the command below, or you can simply download the project as a zip file from [here](https://github.com/SMDevJi/py-gogoanime-api/archive/refs/heads/master.zip) and extract it. Then go to the root directory of the project.

```sh
git clone https://github.com/SMDevJi/py-gogoanime-api.git

```

Now, run the command below to install all dependencies of the project, if you have multiple python versions installed, use pip3 instead of pip.

```sh
pip install -r requirements.txt
```
Now open `config.json` in your favourite text editor, Change the values of `browse_url` and `ajax_url` if necessary. GogoAnime frequently changes their domain, You have to do it only if they change it, otherwise no need to change it.

```json
{
    "browse_url":"https://example1.com/",
    "ajax_url":"https://example2.net/"
}
```

Now run the following command to start the API server. if you have multiple python versions installed, use python3 instead of python.

```sh
python main.py
```

Now the server is started on http://localhost:5000

## Android (Termux)

Download and install f-droid app store from [here](https://f-droid.org/en/packages/org.fdroid.fdroid/) and install latest termux APK from there. Now run the command below to update & upgrade all packages. If it asks for yes/no, keep pressing enter.

```sh
apt update && apt upgrade
```

Now install python3 with the following command.

```sh
pkg install python3
```
Now you need to seperately install python's cryptography module using the following command.

```sh
apt install python-cryptography
```
Now install git with the following command.

```sh
pkg install git
```
Now, clone the repo and go to the project's root directory using the commands below.

```sh
git clone https://github.com/SMDevJi/py-gogoanime-api.git
cd py-gogoanime-api
```
Now, install the remaining python modules using the below command.

```sh
pip3 install -r requirements.txt
```
Now, start the server using the command below.

```sh
python3 main.py
```
Now the server is started on http://localhost:5000
## Routes
Details about all routes are provided below, examples are shown using **Fetch API**.

### Get Recent Episodes
Get details about recently released anime episodes. `page_data` property contains details about the animes. if `type` and `page` parameters are not provided, both will default to 1.

| Parameter    | Description                                                                                                                                                                                   |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type` (int) | (optional) **type 1: japanese with subtitle. type 2: english dub with no subtitles. type 3: chinese with english subtitles.** |
| `page` (int) | (optional) **page number (`last_page` is the maximum value).**                                                                                                                              |

```js
fetch("http://localhost:5000/recent-releases?page=5&type=1")
  .then((response) => response.json())
  .then((animelist) => console.log(animelist));
```

Output >>

```json
{
  "last_page": "227",
  "page_data": [
    {
      "anime_id": "example-anime",
      "ep_id": "example-anime-episode-49",
      "ep_num": "49",
      "img": "https://example.com/images/anime/example-anime.png",
      "title": "Example Anime",
      "type": "sub"
    },
    {...},
    ...
  ]
}
```

### Get Popular Anime
Get popular ongoing anime details. If page number is not provided, defaults to 1. `page_data` property contains data of current page.

| Parameter    | Description         |
| ------------ | ------------------- |
| `page` (int) | (optional) page number (`last_page` is max value). |

```js
fetch("http://localhost:5000/popular?page=2")
  .then((response) => response.json())
  .then((animelist) => console.log(animelist));
```

Output >>

```json
{
  "last_page": "46",
  "page_data": [
    {
      "anime_id": "example-anime",
      "ep_id": "example-anime-episode-4",
      "ep_num": "4",
      "genres": [
        "Action",
        "Adventure"
      ],
      "img": "https://example.com/images/anime/example-anime.png",
      "title": "Example Anime"
    },
    {...},
    ...
  ]
}
```

### Get Anime Search
Search anime with keyword. `page_data` property contains details of current page, `current_pages` property contains currently available page numbers. `sort` parameter defaults to `title_az` if not provided and `page` defaults to `1` if not provided. All possible values of the optional filter parameters are provided below the table. Except `sort` and `page`, multiple values can be provided for all other parameters

| Parameter       | Description         |
| --------------- | ------------------- |
| `keyword` (string) | search query         |
| `sort` (string)    | (optional) sorting order |
| `page` (int)    | (optional) page number |
| `status` (string)    | (optional) status of anime |
| `type` (int)    | (optional) type of anime |
| `language` (string)    | (optional) anime audio language type |
| `year` (int)    | (optional) release year |
| `season` (string)    | (optional) release season |
| `country` (int)    | (optional) country of origin |
| `genre` (string)    | (optional) genre of anime |


#### Genres
All valid values of `genre` parameter
<details>
<summary>Genres list</summary>

| Genres           |
| --------------- |
| `action`        |
| `adult-cast`    |
| `adventure`     |
| `anthropomorphic`|
| `avant-garde`   |
| `shounen-ai`    |
| `cars`          |
| `cgdct`         |
| `childcare`     |
| `comedy`        |
| `comic`         |
| `crime`         |
| `crossdressing` |
| `delinquents`   |
| `dementia`      |
| `demons`        |
| `detective`     |
| `drama`         |
| `dub`           |
| `ecchi`         |
| `erotica`       |
| `family`        |
| `fantasy`       |
| `gag-humor`     |
| `game`          |
| `gender-bender` |
| `gore`          |
| `gourmet`       |
| `harem`         |
| `high-stakes-game`|
| `historical`    |
| `horror`        |
| `isekai`        |
| `iyashikei`     |
| `josei`         |
| `kids`          |
| `love-polygon`  |
| `magic`         |
| `magical-sex-shift`|
| `mahou-shoujo`  |
| `martial-arts`  |
| `mecha`         |
| `medical`       |
| `military`      |
| `music`         |
| `mystery`       |
| `mythology`     |
| `organized-crime`|
| `parody`        |
| `performing-arts`|
| `pets`          |
| `police`        |
| `psychological` |
| `racing`        |
| `reincarnation` |
| `romance`       |
| `romantic-subtext`|
| `samurai`       |
| `school`        |
| `sci-fi`        |
| `seinen`        |
| `shoujo`        |
| `shoujo-ai`     |
| `shounen`       |
| `showbiz`       |
| `slice-of-life` |
| `space`         |
| `sports`        |
| `strategy-game` |
| `super-power`   |
| `supernatural`  |
| `survival`      |
| `suspense`      |
| `team-sports`   |
| `thriller`      |
| `time-travel`   |
| `vampire`       |
| `video-game`    |
| `visual-arts`   |
| `work-life`     |
| `workplace`     |
| `yaoi`          |
| `yuri`          |

 In python list format:
```python
 ['action', 'adult-cast', 'adventure', 'anthropomorphic', 'avant-garde', 'shounen-ai', 'cars', 'cgdct', 'childcare', 'comedy', 'comic', 'crime', 'crossdressing', 'delinquents', 'dementia', 'demons', 'detective', 'drama', 'dub', 'ecchi', 'erotica', 'family', 'fantasy', 'gag-humor', 'game', 'gender-bender', 'gore', 'gourmet', 'harem', 'high-stakes-game', 'historical', 'horror', 'isekai', 'iyashikei', 'josei', 'kids', 'love-polygon', 'magic', 'magical-sex-shift', 'mahou-shoujo', 'martial-arts', 'mecha', 'medical', 'military', 'music', 'mystery', 'mythology', 'organized-crime', 'parody', 'performing-arts', 'pets', 'police', 'psychological', 'racing', 'reincarnation', 'romance', 'romantic-subtext', 'samurai', 'school', 'sci-fi', 'seinen', 'shoujo', 'shoujo-ai', 'shounen', 'showbiz', 'slice-of-life', 'space', 'sports', 'strategy-game', 'super-power', 'supernatural', 'survival', 'suspense', 'team-sports', 'thriller', 'time-travel', 'vampire', 'video-game', 'visual-arts', 'work-life', 'workplace', 'yaoi', 'yuri']
```


</details>

#### Sort
All valid values of `sort` parameter
<details>
<summary>Sort Parameter Values</summary>

| Values           |
| --------------- |
| `title_az`      |
| `recently_updated`  |
| `recently_added`  |
| `release_date`  |

</details>

#### Status
All valid values of `status` parameter
<details>
<summary>Status Parameter Values</summary>

| Values           |
| --------------- |
| `Upcoming`      |
| `Ongoing`       |
| `Completed`     |

</details>

#### Type
All valid values of `type` parameter
<details>
<summary>Type Parameter Values</summary>

| Value           | Meaning |
| --------------- |---------|
| `3`             |  Movie  |
| `1`             |  TV     |
| `26`            |  OVA    |
| `30`            |  ONA    |
| `2`             | Special |
| `32`            |  Music  |

</details>

#### Language
All valid values of `language` parameter
<details>
<summary>Language Parameter Values</summary>

| Languages       |
| --------------- |
| `subdub`        |
| `sub`           |
| `dub`           |

</details>

#### Year
All valid values of `year` parameter
<details>
<summary>Year Parameter Values</summary>

`1999` to current year.

</details>

#### Season
All valid values of `season` parameter
<details>
<summary>Season Parameter Values</summary>

| Seasons         |
| --------------- |
| `fall`          |
| `summer`        |
| `spring`        |
| `winter`        |

</details>

#### Country
All valid values of `country` parameter
<details>
<summary>Country Parameter Values</summary>

| Value     | Meaning |
| --------- |---------|
| `5`       | China   |
| `2`       | Japan   |

</details>




```js
fetch("http://localhost:5000/search?keyword=example&language=subdub&language=sub&language=dub&page=3")
  .then((response) => response.json())
  .then((animelist) => console.log(animelist));
```

Output >>

```json
{
  "current_pages": [
    "1",
    "2"
  ], 
  "page_data": [
    {
      "id": "example-anime", 
      "img": "https://example.com/images/anime/example-anime.png", 
      "status": "Released: 2005", 
      "title": "Example Anime"
    },
    {...},
    ...
  ]
}
```

### Get Anime Movies
Get details of available anime movies. In `page_data` property, you will get details of anime movies in the current page (If `page` parameter not provided, it will default to 1), The `current_pages` property contains the currently available page numbers.

| Parameter      | Description                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `alpha` (string) | (optional) Filter for specific alphabet. **values are from [A-Z].** |
| `page` (int)   | (optional) page number (values in `current_pages` are available page numbers)                                                                                                           |

```js
fetch("http://localhost:5000/anime-movies?page=5&alpha=A")
  .then((response) => response.json())
  .then((animelist) => console.log(animelist));
```

Output >>

```json
{
  "current_pages": [ 
    "4", 
    "5", 
    "6"
  ], 
  "page_data": [
    {
      "id": "example-movie", 
      "img": "https://example.com/images/anime/example-movie.png", 
      "status": "Released:2002", 
      "title": "Example Anime Movie"
    }, 
    {...},
    ...
  ]
}
```




### Get Anime Details
Get details about an anime from it's anime ID. You can find the id of the Anime from [search results](#get-anime-search), [anime movies](#get-anime-movies),[recent episodes](#get-recent-episodes) and [popular anime](#get-popular-anime)


| Parameter  |  Description   |
|  ----------| -------------- |
| `:id` (string) | Anime ID   |

```js
fetch("http://localhost:5000/anime-details/example-anime")
  .then((response) => response.json())
  .then((animelist) => console.log(animelist));
```

Output >>

```json
{
  "description": "This is an example description of Example Anime.", 
  "episodesAvailable": "2", 
  "episodesList": [
    {
      "id": "example-anime-episode-2", 
      "num": "2", 
      "type": "sub"
    }, 
    {...},
        ...
  ], 
  "genres": [
    "Action", 
    "Comedy",  
    "Super Power"
  ], 
  "img": "https://example.com/images/anime/example.jpg", 
  "otherName": "アニメの例", 
  "releaseYear": "2000", 
  "status": "Completed", 
  "title": "Example Anime", 
  "type": "TV Series"
}
```

### Get Streaming URLs

Get streaming URLs from episode ID. You can get the id of an episode from [anime details](#get-anime-details), [popular anime](#get-popular-anime) and [recent episodes](#get-recent-episodes)

| Parameter      |Description  |
| -------------- | ----------- |
| `:id` (string) | episodeId.  |



```js
fetch("http://localhost:5000/stream/example-anime-episode-1")
  .then((response) => response.json())
  .then((animelist) => console.log(animelist));
```

Output >>

```json
{
  "source": {
    "file": "https://example-url.com/video.m3u8", 
    "type": "hls"
  }, 
  "source_backup": {
    "file": "https://example-url2.com/video.m3u8", 
    "type": "hls"
  }
}
```

