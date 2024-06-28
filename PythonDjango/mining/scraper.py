import requests
from bs4 import BeautifulSoup
from .models import Advertisement
from datetime import datetime


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def scrape_website(url, purchase_type="Unknown", advertisement_type="Unknown"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    ads = []
    for ad in soup.find_all("a", href=True):
        ad_url = ad["href"]
        ad_title = ad.text.strip()

        # Follow the link to get advertisement details
        ad_response = requests.get(f"https://cvpp.eviesiejipirkimai.lt{ad_url}")
        ad_soup = BeautifulSoup(ad_response.text, "html.parser")

        # Extract details from the advertisement page
        advertiser_name = ad_soup.find("div", class_="eps-text").text.strip()
        advertiser_link = f"https://cvpp.eviesiejipirkimai.lt{ad_url}"

        publication_date_tag = ad_soup.find("div", string="Paskelbimo data")
        publication_date_str = (
            publication_date_tag.find_next_sibling("div").text.strip()
            if publication_date_tag
            else None
        )
        publication_date = (
            parse_date(publication_date_str) if publication_date_str else None
        )

        submission_deadline_tag = ad_soup.find(
            "div", string="Pasiūlymų pateikimo terminas"
        )
        submission_deadline_str = (
            submission_deadline_tag.find_next_sibling("div").text.strip()
            if submission_deadline_tag
            else None
        )
        submission_deadline = (
            parse_date(submission_deadline_str) if submission_deadline_str else None
        )

        bvpz_code_tag = ad_soup.find("div", string="Pirkimo numeris")
        bvpz_code = (
            bvpz_code_tag.find_next_sibling("div").text.strip()
            if bvpz_code_tag
            else "No BVPZ code"
        )

        ads.append(
            {
                "title": ad_title,
                "advertiser_name": advertiser_name,
                "advertiser_link": advertiser_link,
                "publication_date": publication_date,
                "submission_deadline": submission_deadline,
                "bvpz_code": bvpz_code,
                "purchase_type": purchase_type,
                "advertisement_type": advertisement_type,
            }
        )

    for ad in ads:
        Advertisement.objects.create(**ad)


# Ensure to call the scraping function with the correct URL
scrape_website("https://cvpp.eviesiejipirkimai.lt/")
