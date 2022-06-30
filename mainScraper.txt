
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.proxy import ProxyType, Proxy
import json
from bs4 import BeautifulSoup
import time
from typing import Optional
from fastapi import FastAPI
from config import connection, close_connection
import requests
from loggers import logger
import datetime
app = FastAPI()
# from lxml import *
scrap_obj = logger()
with open('configs.json', 'r') as c:
    handler = json.load(c)["handler"]
scraper_logger = scrap_obj.scrapper_logger()
main_logger = scrap_obj.main_logger()


def hotel_data(link):
    service = Service('chromedriver.exe')
    options = webdriver.ChromeOptions()
    proxy_address = '108.59.14.208:13040'
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = proxy_address
    proxy.ssl_proxy = proxy_address
    capabilities = webdriver.DesiredCapabilities.CHROME
    proxy.add_to_capabilities(capabilities)

    options.add_argument("--start-maximized")
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(
        desired_capabilities=capabilities, service=service, options=options)
    driver.implicitly_wait(1)
    driver.get(link)
    time.sleep(10)
    highlights = driver.find_elements(By.CLASS_NAME, 'KpoLkf')
    highlight_data = ''
    for highlight in highlights:
        highlight_data = highlight_data + highlight.text
        highlight_data = highlight_data + "#"
    try:
        driver.find_element(By.XPATH,
                            '/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span/span[2]/span[1]/button').click()
    except:
        try:
            driver.find_element(
                By.CSS_SELECTOR, "[aria-label*='review']").click()
        except:
            try:
                driver.find_element(
                    By.CSS_SELECTOR, "[jsan='7.Yr7JMd-pane-hSRGPd,0.aria-label,0.vet,0.jsaction']").click()
            except:
                try:
                    driver.find_element(
                        By.CSS_SELECTOR, "[jsaction*='pane.rating.moreReviews']").click()
                except:
                    pass
    time.sleep(5)
    category = ''
    try:
        categories = driver.find_elements(By.CLASS_NAME, 'b0GMvf')
        ratings = driver.find_elements(By.CLASS_NAME, 'rlvodb')
        j = 0
        for data in categories:
            category = category + data.text
            category = category + ','
            category = category + ratings[j].text
            category = category + "#"
            j = j + 1
    except:
        pass
    return highlight_data, category


def query(link, business_category):
    scraper_logger.info(f"link is {link}")
    main_logger.info(f"link is {link}")
    cursor, db = connection()
    cursor.execute(
        "SELECT * FROM query WHERE business_link=%s", (link,))
    query_data = cursor.fetchall()
    if query_data:
        scraper_logger.info(f"Data already exits in query table.")
        query_id = query_data[0][0]
    else:
        date_created = datetime.datetime.today()
        cursor.execute(
            "INSERT INTO query( business_link, business_category, date_created) VALUES ( %s, %s, %s)", (link, business_category, date_created,))
        db.commit()
        scraper_logger.info(f"Query data has been created successfully!")
        cursor.execute(
            "SELECT * FROM query WHERE business_link=%s", (link,))
        query_data = cursor.fetchall()
        query_id = query_data[0][0]
    close_connection(cursor, db)
    return query_id


@app.get('/maps_scraper/')
def scraper(*, link: str, option: str, limit: Optional[str] = None, business_category: str):

    if limit:
        limit = int(limit)
    else:
        limit = 0
    if option == "profile":
        choice = 1
    elif option == "reviews":
        choice = 2
    elif option == "both":
        choice = 3
    query_id = query(link, business_category)
    print(f"query id is {query_id}")
    if choice == 1:
        business_data(link, query_id, business_category)
    elif choice == 2:
        business_reviews(link, query_id, limit, business_category)
    elif choice == 3:
        business_data(link, query_id, business_category)
        business_reviews(link, query_id, limit, business_category)
    return query_id


def business_data(link, query_id, business_category):
    cursor, db = connection()
    cursor.execute(
        "SELECT * FROM business_data WHERE query_id=%s", (query_id,))
    profile_data = cursor.fetchone()
    if profile_data:
        business_data_id = profile_data[0]
    else:
        link2 = link.split('/')
        name = link2[5]
        new_data = link2[6]
        new_data = new_data.split(',')
        latitude = new_data[0]
        latitude = latitude.split('.')
        latitude = latitude[1]
        latitude = latitude[1]
        longitude = new_data[1]
        longitude = longitude.split('.')
        longitude = longitude[1]
        zindex = new_data[2]
        zindex = zindex.replace('z', '')
        all_data = link2[7]
        all_data = all_data.split('!')
        for i in all_data:
            if i.startswith('1s0'):
                s1s2 = i
                s1s2 = s1s2.split(':')
                s1 = s1s2[0]
                s2 = s1s2[1]
            elif i.startswith('3d'):
                d3 = i
            elif i.startswith('4d'):
                d4 = i
        s3 = ''
        author = '0'
        hl = "en"
        # link  = f"https://www.google.com/maps/place/Barq+Digital+Solution+-+Software+House+in+Islamabad/data=!4m6!3m5!1s0x38dfbf6f3b2594b1:0x6a674ab0890e1c6a!8m2!3d33.6886193!4d73.0017356!16s%2Fg%2F11rwx1fncy?authuser=0&hl=en&rclk=1"
        linkn = f"https://www.google.com/maps/preview/place?authuser={author}&hl={hl}&authuser={author}&pb=!1m14!{s1}%3A{s2}!3m8!1m3!1d.{zindex}!2d.{longitude}!3d.{latitude}!3m2!1i1024!2i768!4f13.1!4m2!3d.{latitude}!4d.{longitude}!11s{s3}!12m4!2m3!1i360!2i120!4i8!13m57!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240!7m42!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!2b1!4b1!9b0!14m3!1s!7e81!15i10112!15m89!1m35!13m8!2b1!3b1!4b1!6i1!8b1!9b1!14b1!20b1!15m1!1i2!17m9!1m3!1i2022!2i6!3i12!2m3!1i2022!2i6!3i13!5b1!18m12!3b1!4b1!5b1!6b1!9b1!12b1!13b1!14b1!15b1!17b1!20b1!21b1!19b0!2b1!5m5!2b1!3b1!5b1!6b1!7b1!10m1!8e3!14m1!3b1!17b1!20m4!1e3!1e6!1e3!1e6!24b1!25b1!26b1!29b1!30m1!2b1!36b1!39m3!2m2!2i1!3i1!43b1!52b1!54m1!1b1!55b1!56m2!1b1!3b1!65m9!3m8!1m3!1m2!1i224!2i298!1m3!1m2!1i224!2i298!71b1!72m4!1m2!3b1!5b1!4b1!89b1!21m28!1m6!1m2!1i0!2i0!2m2!1i458!2i768!1m6!1m2!1i974!2i0!2m2!1i1024!2i768!1m6!1m2!1i0!2i0!2m2!1i1024!2i20!1m6!1m2!1i0!2i748!2m2!1i1024!2i768!22m1!1e81!30m5!3b1!6m1!1b1!7m1!1e3!34m2!7b1!10b1!37i606&q={name}"
        cursor.execute(
            "SELECT * FROM business_data WHERE query_id=%s", (query_id,))
        profile_data = cursor.fetchone()
        if profile_data:
            business_data_id = profile_data[0]
        else:
            r = requests.get(linkn)
            data1 = r.text
            data1 = (data1.split(")]}'\n"))
            data1 = data1[1]
            ini_list = data1
            res = json.loads(ini_list)
            data = res[6]
            # business_data
            name = data[11]
            # j = 0
            # for i in data[52]:
            #     print(j)
            #     print(i)
            #     j = j + 1
            if business_category == 'hotel':
                subtext = data[101]
                if subtext is None or subtext == '':
                    subtext = 'none'
            else:
                subtext = data[13][0]
            total_rating = data[4]
            if not total_rating is None:
                rating = float(total_rating[7])
                review_num = total_rating[8]
            else:
                rating = 0.0
                review_num = 0
            addresses = data[2]
            address = ''
            for j in addresses:
                address = address + j
                address = address + ', '
            address = address[:-2]
            website = data[7]
            if not website is None:
                website = website[1]
            else:
                website = 'none'
            phone = data[178]
            if not phone is None:

                phone = phone[0][0]
            else:
                phone = 'none'
            date_created = datetime.datetime.now()
            cursor.execute("INSERT INTO business_data(query_id,name, subtext, rating,review_num, address, website, phone, date_created ) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s)",
                           (query_id, name, subtext, rating, review_num, address, website, phone, date_created,))
            db.commit()
            cursor.execute(
                "SELECT * FROM business_data WHERE query_id=%s", (query_id,))
            profile_data = cursor.fetchone()
            business_data_id = profile_data[0]
        # restaurant_data
        if business_category == 'restaurant':
            cursor.execute(
                "SELECT * FROM restaurant_data where business_data_id = %s", (business_data_id,))
            restaurant_data = cursor.fetchone()
            if not restaurant_data:
                price = len(data[4][2])
                service = ''
                try:
                    services = data[100][3]
                    for i in services:
                        service = service + i[1]
                        service = service + "#"
                    service = service[:-1]
                except:
                    service = 'none'
                cursor.execute("INSERT INTO restaurant_data(business_data_id,price,service ) VALUES (%s, %s, %s)",
                               (business_data_id, price, service,))
                db.commit()
            aspects = data[153][0]
            for i in aspects:
                aspect = str(i[1])
                mention_num = int(i[3][4])
                cursor.execute("INSERT INTO restaurant_aspects(restaurant_data_id, aspect, mention_num) VALUES ( %s, %s, %s)",
                               (business_data_id, aspect, mention_num,))
                db.commit()
    # hotel_data
        if business_category == 'hotel':
            cursor.execute(
                "SELECT * FROM hotel_data where business_data_id = %s", (business_data_id,))
            hotel_dataa = cursor.fetchone()
            if not hotel_dataa:
                hotel_type = data[64]
                if hotel_type is None or hotel_type == '':
                    hotel_type = ''
                else:
                    hotel_type = hotel_type[3]
                print(data[161])
                print(data[64])
                environment = data[161]
                # print(environment)
                if not environment is None:
                    environment_desc = environment[1]

                    print(environment_desc)
                    environment_rating = environment[3][0][0]
                    print(environment_rating)
                    environment_rating = float(environment_rating)
                    environment_rating = format(environment_rating, '.1f')
                else:
                    environment_desc = 'none'
                    environment_rating = 0.0
                amenity = ''
                amenities = data[64]
                if not amenities is None:
                    amenities = amenities[2]
                    j = 0
                    for i in amenities:
                        amenity_type = i[2]
                        amenity_value = i[3]
                        if amenity_value == 1:
                            amenity = amenity + amenity_type
                            amenity = amenity + "#"
                    amenity = amenity[:-1]
                hotel_description = ''
                try:
                    hotel_details = data[32][2][7][0]
                    if hotel_details is None or hotel_details == '':
                        hotel_description = 'none'
                    else:
                        for hotel_detail in hotel_details:
                            hotel_description = hotel_description + hotel_detail
                            hotel_description = hotel_description + ' '
                except:
                    hotel_description = 'none'
                highlights, categoriess = hotel_data(link)
                cursor.execute("INSERT INTO hotel_data(business_data_id,type, highlights,environment_rating, environment_desc,amenities,categories,description ) VALUES ( %s, %s, %s, %s, %s, %s, %s,%s)",
                               (business_data_id, hotel_type, highlights, environment_rating, environment_desc, amenity, categoriess, hotel_description,))
                db.commit()
# business_reviews 1


def business_reviews(link, query_id, limit, business_category):
    cursor, db = connection()
    cursor.execute(
        "SELECT COUNT(*) FROM business_reviews where query_id = %s", (query_id,))
    records = cursor.fetchall()
    total_records = records[0][0]

    print(total_records)
    cursor.execute(
        "SELECT * FROM business_reviews where query_id=%s", (query_id,))
    records = cursor.fetchall()
    if total_records > 0:
        first_reviewer_name = records[0][2]
        check = 1
        # last_reviewer_name = records[-1][2]
    else:
        check = 0
    proxy = '108.59.14.203:13040'
    # r = requests.get(link)
    r = requests.get(link, proxies={
        'http': proxy, 'https': proxy}, timeout=15)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find_all('script')[6].text.strip()
    with open('reviews_details.txt', 'w', encoding="utf-8") as f:
        f.write(data)
    data = data.split("window.APP_OPTIONS=")
    data = data[1]
    data = data.split(";window.APP_INITIALIZATION_STATE=")
    data = data[1]
    data = data.split(";window.APP_FLAGS=")
    data = data[0]
    res = json.loads(data)
    new_data = str(res[3][6])
    new_data = new_data[5:]
    with open('reviews_details.txt', 'w', encoding="utf-8") as f:
        f.write(new_data)
    res = json.loads(new_data)
    code1 = res[6][72][0][0][29][0]
    code2 = res[6][72][0][0][29][1]
    print(code1)
    print(code2)

    limit1 = 0
    limit2 = 150
    temp = 0
    counter_review = 0
    new_check = 0
    while True:
        link_created = f"https://www.google.com/maps/preview/review/listentitiesreviews?authuser=0&hl=en&pb=!1m2!1y{code1}!2y{code2}!2m2!1i{limit1}!2i{limit2}!3e2!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1s!7e81"
        r1 = requests.get(link_created, proxies={
            'http': proxy, 'https': proxy}, timeout=25)
        print(f"link is {link_created}")
        # r1 = requests.get(link_created)
        data1 = r1.text
        data1 = (data1.split(")]}'\n"))
        data1 = data1[1]
        ini_list = data1
        res = json.loads(ini_list)
        new_data = res[2]
        j = 0
        try:
            length = len(new_data)
            print(len(new_data))
        except:
            print('in length except')
            break
        if length <= 0:
            break
        for j in new_data:
            reviewer_link = j[0][0]
            reviewer_name = j[0][1]
            if check == 1:
                print("in check 1")
                if reviewer_name == first_reviewer_name:
                    print("match reviewer_name")
                    check == 0
                    limit1 = temp + total_records
                    new_check = 2
                    break
            review_time = j[1]
            review_text = j[3]
            review_translation = ''
            review_texts = ''
            if not review_text is None:
                if '(Translated by Google)' and '(Original)' in review_text:
                    description = review_text.split('(Original)')
                    review_texts = description[0]
                    review_texts = review_texts.replace(
                        '(Translated by Google)', '')
                    review_translation = description[1]
                elif '(Translated by Google)' in review_text:
                    description = review_text.split(
                        '(Translated by Google)')
                    review_texts = description[0]
                    review_texts = review_text.replace(
                        '(Translated by Google)', '')
                    review_translation = description[1]
                else:
                    review_texts = review_text
                    review_translation = 'none'
            else:
                review_translation = 'none'
                review_texts = 'none'

            rating = j[4]
            if rating is None:
                rating = 0
            photos = j[14]
            if photos is None:
                no_of_photos = 0
            else:
                no_of_photos = len(photos)

            review_likes = j[16]
            if business_category == 'hotel':
                trip_type = ''
                venue = "Google"
                rsl = j[49]
                review_location = 0
                review_room = 0
                review_service = 0
                if not rsl is None:
                    for k in rsl:
                        if 'Trip type' in k[5]:
                            trip_type = trip_type + str(k[2][0][0][1])
                        elif 'Rooms' in k[5]:
                            review_room = int(k[6])
                        elif 'Service' in k[5]:
                            review_service = int(k[6])
                        elif 'Location' in k[5]:
                            review_location = int(k[6])
                        else:
                            pass
                max_rating = 5
            if 'google.com' in reviewer_link:
                print("in google reviews insertion")
                scrape_time = datetime.datetime.now()
                cursor.execute(
                    "INSERT INTO business_reviews(query_id, reviewer_name, rating, review_time,review_text, review_photos, review_likes, scrape_time) VALUES (%s, %s, %s,%s,%s,%s,%s,%s)", (query_id, reviewer_name, rating, review_time, review_texts, no_of_photos,  review_likes, scrape_time,))
                db.commit()
                business_reviews_id = cursor.lastrowid
                cursor.execute("INSERT INTO review_translation(business_reviews_id,translated_text)VALUES(%s,%s)", (
                    business_reviews_id, review_translation))
                if business_category == 'hotel':
                    cursor.execute("INSERT INTO hotel_review(business_reviews_id, max_rating, venue, trip, review_location, review_service, review_room) VALUES ( %s, %s, %s, %s, %s, %s, %s)",
                                   (business_reviews_id, max_rating, venue, trip_type, review_location, review_service, review_room,))
                    db.commit()
                temp = temp + 1
            print(f'limit is  {limit}')
            print(f'temp is  {temp}')
            if temp == limit:
                print('limit and temp are equal')
                new_check = 1
                break

            # if not limit == -1:
            #     counter_review += 1
            # if limit == counter_review:
            #     break
        if new_check == 1:
            break
        elif new_check == 2:
            continue
        print(f'no of records inserted are: {temp}')
        limit = limit + 150


def g_reviewers():
    pass
