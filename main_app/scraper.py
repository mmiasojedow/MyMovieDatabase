import requests
from bs4 import BeautifulSoup
from main_app.models import Movie
from django.contrib.auth import get_user_model

User = get_user_model()


def get_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_movies(soup, user):
    movies = soup.find_all("div", attrs={"class": "lister-item-content"})
    for movie in movies:
        title = movie.find(
            "h3", attrs={"class": "lister-item-header"}).find("a").text
        rating = int(movie.find("div", attrs={"class": "ipl-rating-star--other-user"}).find(
            "span", attrs={"class": "ipl-rating-star__rating"}).text)
        link = "https://www.imdb.com" + \
            movie.find(
                "h3", attrs={"class": "lister-item-header"}).find("a")["href"]
        Movie.objects.create(title=title, rating=rating,
                             link=link, user_id=user.id)


def get_next_url(soup):
    if soup.find("a", attrs={"class": "next-page"})["href"] != "#":
        url = "https://www.imdb.com" + \
            soup.find("a", attrs={"class": "next-page"})["href"]
        return url
    else:
        return False


def get_movies_quantity(soup):
    result = int(soup.find("span", attrs={
                 "id": "lister-header-current-size"}).text)
    return result


def get_all_movies(user):
    url = user.imdb_link
    while True:
        soup = get_page(url)
        get_movies(soup, user)
        url = get_next_url(soup)
        if not url:
            break


def get_new_movies(user):
    url = user.imdb_link
    soup = get_page(url)
    try:
        get_movies(soup, user)
    except:
        pass
