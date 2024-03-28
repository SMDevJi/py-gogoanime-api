import json
import requests
from base64 import b64encode, b64decode
from flask import Flask, jsonify, make_response, request


from scrapers.vidstreaming import *
from scrapers.streamwish import *

BROWSE_URL = json.loads(open("config.json").read())["browse_url"]
AJAX_URL = json.loads(open("config.json").read())["ajax_url"]

ep_list_url = AJAX_URL+"ajax/load-list-episode"
popular_url = AJAX_URL+"ajax/page-recent-release-ongoing.html"


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False


@app.errorhandler(404)
def not_found(e):
    return jsonify({"statusCode": 404, "message": "endpoint does not exist."}), 404


@app.route('/stream/<episode_id>')
def download(episode_id):
    try:
        browse_page_url = BROWSE_URL+episode_id
        browse_page_html = requests.get(browse_page_url).text

        try:
            vidstreaming_url = extract_vidstreaming_url(browse_page_html)
        except:
            response = {
                "statusCode": 404, "message": "Invalid episode ID provided or failed to extract URL."}
            return jsonify(response), 404

        vidstreaming_id = extract_vidstreaming_id(vidstreaming_url)
        vidstreaming_page_html = requests.get(vidstreaming_url).text
        episode_script = extract_episode_script(vidstreaming_page_html)

        encrypted_key = create_encrypted_key(
            vidstreaming_id, keys["key1"], keys["iv"])
        remaining_params = create_remaining_params(
            b64decode(episode_script), keys["key1"], keys["iv"])

        encrypt_ajax_url = vidstreaming_url.split("streaming.php?")[
            0]+f"encrypt-ajax.php?id={encrypted_key}&alias={remaining_params}"

        ENCRYPT_AJAX_REQUEST_HEADERS['Referer'] = vidstreaming_url

        encrypt_ajax_response = requests.get(
            encrypt_ajax_url, headers=ENCRYPT_AJAX_REQUEST_HEADERS).content.decode('utf-8')

        encrypt_ajax_response_json = json.loads(encrypt_ajax_response)["data"]

        final_result = str(decrypt_encrypt_ajax_response(
            encrypt_ajax_response_json, keys['key2'], keys['iv'])).replace('\\', "")

        source1 = json.loads(final_result)['source'][0]['file']
        source2 = json.loads(final_result)['source_bk'][0]['file']
        response = {
            "source":
                {
                    "file": f"{source1}",
                    "type": "hls"
                },
            "source_backup":
                {
                    "file": f"{source2}",
                    "type": "hls"
                },
        }
        return jsonify(response)
    except Exception as e:
        response = {"statusCode": 500, "message": f"{e}"}
        return jsonify(response), 500


@app.route('/search')
def search():
    try:
        queries = request.args.to_dict(flat=False)

        if "sort" not in queries.keys():
            queries["sort"] = ["title_az"]
        if "page" not in queries.keys():
            queries["page"] = ["1"]

        search_page_query = f"{BROWSE_URL}/filter.html?keyword={queries['keyword'][0]}&sort={queries['sort'][0]}&page={queries['page'][0]}"

        if "status" in queries.keys():
            for each in queries["status"]:
                search_page_query += f"&status[]={each}"
        if "type" in queries.keys():
            for each in queries["type"]:
                search_page_query += f"&type[]={each}"
        if "language" in queries.keys():
            for each in queries["language"]:
                search_page_query += f"&language[]={each}"
        if "year" in queries.keys():
            for each in queries["year"]:
                search_page_query += f"&year[]={each}"
        if "season" in queries.keys():
            for each in queries["season"]:
                search_page_query += f"&season[]={each}"
        if "country" in queries.keys():
            for each in queries["country"]:
                search_page_query += f"&country[]={each}"
        if "genre" in queries.keys():
            for each in queries["genre"]:
                search_page_query += f"&genre[]={each}"

        search_page_html = requests.get(search_page_query).text

        soup = BeautifulSoup(search_page_html, 'html.parser')

        anime_list = soup.find('ul', class_='items').find_all('li')
        if not anime_list:
            return jsonify({
                "current_pages": [],
                "page_data": []
            })

        final_json = {}

        # Current pages
        final_json["current_pages"] = []
        try:
            page_list = soup.find(
                "ul", class_="pagination-list").find_all("li")
            for page in page_list:
                final_json["current_pages"].append(page.find("a").text)
        except:
            final_json["current_pages"] = ["1"]

        # Page data
        final_json["page_data"] = []
        anime_data = []
        for anime_item in anime_list:
            anime_info = {}

            anime_info['img'] = anime_item.find('img')['src']

            anime_info['title'] = anime_item.find(
                'p', class_='name').find('a').text

            anime_info['id'] = (BROWSE_URL + anime_item.find(
                'a', title=anime_info['title'])['href']).split("/category/")[1]

            released_text = anime_item.find('p', class_='released').text
            anime_info['status'] = released_text.replace(
                "\n", "").replace("\t ", "").replace("\t", "")[:-1]

            anime_data.append(anime_info)
        final_json["page_data"] = anime_data
    except Exception as e:
        response = {"statusCode": 500, "message": f"{e}"}
        return jsonify(response), 500

    return jsonify(final_json)


@app.route('/anime-details/<anime_id>')
def anime_details(anime_id):

    genres = []
    episodesList = []

    try:
        category_page_html = requests.get(
            f"{BROWSE_URL}/category/{anime_id}").text
        soup = BeautifulSoup(category_page_html, "html.parser")
        anime_data = {}
        anime_data['title'] = soup.find(
            'div', class_="anime_info_body_bg").find("h1").text

        anime_data['img'] = soup.find(
            'div', class_="anime_info_body_bg").find("img")["src"]

        all_class_type_elements = soup.find(
            'div', class_="anime_info_body_bg").findAll("p", class_="type")
        for each in all_class_type_elements:
            if "Type" in each.find("span").text:
                anime_data['type'] = each.find("a").text
            if "Released" in each.find("span").text:
                anime_data['releaseYear'] = each.text.replace("Released: ", "")
            if "Status" in each.find("span").text:
                anime_data['status'] = each.find("a").text
            if "Genre" in each.find("span").text:
                genreAnchorTags = each.findAll("a")
                for genreAnchor in genreAnchorTags:
                    genres.append(genreAnchor.text.replace(", ", ""))
        try:
            anime_data['description'] = soup.find('div', class_="anime_info_body_bg").find(
                "div", class_="description").find("p").text
        except:
            anime_data['description'] = soup.find('div', class_="anime_info_body_bg").find(
                "div", class_="description").text.replace("\r", "").replace("\n", "")

        anime_data['otherName'] = soup.find('div', class_="anime_info_body_bg").find(
            "p", class_="other-name").find("a").text

        anime_data['genres'] = genres

        start_ep = soup.find("ul", id="episode_page").findAll("li")[
            0].find("a")["ep_start"]
        end_ep = soup.find("ul", id="episode_page").findAll(
            "li")[-1].find("a")["ep_end"]
        anime_data['episodesAvailable'] = end_ep

        movie_id = soup.find("input", id="movie_id")["value"]
        alias = soup.find("input", id="alias_anime")["value"]
        # print(f"{ep_list_url}?ep_start={start_ep}&ep_end={end_ep}&id={movie_id}&default_ep={0}&alias={alias}")
        ep_list_html = requests.get(
            f"{ep_list_url}?ep_start={start_ep}&ep_end={end_ep}&id={movie_id}&default_ep={0}&alias={alias}").text
        ep_list_obj = BeautifulSoup(ep_list_html, "html.parser").findAll("li")

        for each in ep_list_obj:
            ep_data = {}

            ep_data["id"] = each.find("a")["href"].replace(
                "/", "").replace(" ", "")
            ep_data["num"] = each.find(
                "div", class_="name").text.replace("EP ", "")
            '''
            ep_data["url"]=f"{BROWSE_URL}/{ep_data['id']}".replace(" ","")
            '''

            type_data = each.find("div", class_="cate").text
            if "SUB" in type_data:
                ep_data["type"] = "sub"
            if "DUB" in type_data:
                ep_data["type"] = "dub"
            episodesList.append(ep_data)

        anime_data["episodesList"] = episodesList
    except Exception as e:
        response = {"statusCode": 500, "message": f"{e}"}
        return jsonify(response), 500

    return jsonify(anime_data)


@app.route('/popular')
def popular():
    page_no = request.args.get('page')
    if not page_no:
        page_no = 1
    try:
        # Find last page number
        last_page_html = requests.get(f"{popular_url}?page=999999").text
        last_page_soup = BeautifulSoup(last_page_html, "html.parser")
        last_page = last_page_soup.find_all("li")[-1].text

        if int(page_no) > int(last_page):
            return jsonify({"statusCode": 404, "message": "Invalid page number provided"}), 404

        final_json = {
            "last_page": f"{last_page}",
        }

        # Page data
        current_page = []
        popular_page_html = requests.get(f"{popular_url}?page={page_no}").text
        popular_page_soup = BeautifulSoup(popular_page_html, "html.parser")
        anime_details_list = popular_page_soup.find(
            "div", class_="added_series_body popular").find_all("li")

        for each_anime_detail in anime_details_list:
            anime_data = {}
            anime_data["title"] = each_anime_detail.find_all("a")[1]["title"]
            anime_data["anime_id"] = each_anime_detail.find_all(
                "a")[1]["href"].split("/category/")[1]
            anime_data["ep_id"] = each_anime_detail.find_all(
                "p")[1].find("a")["href"].replace("/", "")

            genres = []
            genre_html = each_anime_detail.find(
                "p", class_="genres").find_all("a")
            for each in genre_html:
                genre = each.text.replace(", ", "")
                genres.append(genre)
            anime_data["genres"] = genres

            anime_data["img"] = each_anime_detail.find(
                "div", class_="thumbnail-popular")["style"].replace("background: url('", "").replace("');", "")
            anime_data["ep_num"] = each_anime_detail.find(
                "a", title=anime_data["ep_id"]).text.replace("Episode ", "")
            current_page.append(anime_data)

        final_json["page_data"] = current_page
    except Exception as e:
        response = {"statusCode": 500, "message": f"{e}"}
        return jsonify(response), 500
    return jsonify(final_json)


@app.route('/anime-movies')
def movies():
    page_no = request.args.get('page')
    alpha = request.args.get('alpha')

    final_json = {}

    movies_page_url = f"{BROWSE_URL}/anime-movies.html?"
    if page_no:
        movies_page_url += f"page={page_no}&"
    if alpha:
        movies_page_url += f"aph={alpha}"

    try:
        movies_page_html = requests.get(movies_page_url).text
        movie_soup = BeautifulSoup(movies_page_html, "html.parser")

        # Handle 404
        try:
            if "404" in movie_soup.find("h1", class_="entry-title").text:
                return jsonify({"statusCode": 404, "message": "Invalid page number provided"}), 404
        except:
            pass

        # Available pages
        available_pages = movie_soup.find(
            "ul", class_="pagination-list").find_all("li")
        current_pages = []
        for page in available_pages:
            current_pages.append(page.find("a").text)
        final_json["current_pages"] = current_pages

        # Page data
        all_movies = movie_soup.find(
            "div", class_="last_episodes").find_all("li")
        final_json["page_data"] = []
        for movie in all_movies:
            data = {}

            data["title"] = movie.find("p", class_="name").find("a").text
            data["img"] = movie.find("div", class_="img").find("img")["src"]
            data["id"] = movie.find("div", class_="img").find("a")[
                "href"].replace("/category/", "")
            data["status"] = movie.find("p", class_="released").text.replace(
                " ", "").replace("\n", "")

            final_json["page_data"].append(data)
    except Exception as e:
        response = {"statusCode": 500, "message": f"{e}"}
        return jsonify(response), 500

    return jsonify(final_json)


@app.route('/recent-releases')
def recent():
    page_no = request.args.get('page')
    type = request.args.get('type')

    if not page_no:
        page_no = 1
    if not type:
        type = 1
    try:
        # Find last page number
        last_page_html = requests.get(
            f"{AJAX_URL}/ajax/page-recent-release.html?page=999999&type={type}").text
        last_page_soup = BeautifulSoup(last_page_html, "html.parser")
        last_page = last_page_soup.find_all("li")[-1].text

        if int(page_no) > int(last_page):
            return jsonify({"statusCode": 404, "message": "Invalid page number provided"}), 404
        if int(type) > 3 or int(type) < 1:
            return jsonify({"statusCode": 404, "message": "Invalid anime type provided"}), 404

        final_json = {
            "last_page": f"{last_page}",
        }

        # Page data
        final_json["page_data"] = []
        recent_page_url = f"{AJAX_URL}/ajax/page-recent-release.html?page={page_no}&type={type}"
        recent_page_html = requests.get(recent_page_url).text
        recent_soup = BeautifulSoup(recent_page_html, "html.parser")

        anime_details_list = recent_soup.find(
            "div", class_="last_episodes loaddub").find_all("li")
        for each_anime in anime_details_list:
            data = {}
            data["img"] = each_anime.find(
                "div", class_="img").find("img")["src"]
            data["title"] = each_anime.find(
                "div", class_="img").find("a")["title"]
            data["ep_id"] = each_anime.find("div", class_="img").find("a")[
                "href"].replace("/", "")
            data["ep_num"] = each_anime.find(
                "p", class_="episode").text.replace("Episode ", "")

            type = each_anime.find("div", class_="img").find("div")["class"][1]
            if "SUB" in type:
                data["type"] = "sub"
            if "DUB" in type:
                data["type"] = "dub"

            data["anime_id"] = data["ep_id"].replace(
                f"-episode-{data['ep_num']}", "")

            final_json["page_data"].append(data)
    except Exception as e:
        response = {"statusCode": 500, "message": f"{e}"}
        return jsonify(response), 500

    return jsonify(final_json)


if __name__ == '__main__':
    app.run(debug=True)
