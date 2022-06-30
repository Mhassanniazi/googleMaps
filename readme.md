# API Fields for Scraper

There are four fields for scraping reviews

1. Link --> paste link here of business you want to scrape
2. option --> what you want to scrape (profile, reviews, both)
   if 'profile' ==> It will scrape data of business but not reviews
   if 'reviews' ==> It will scrape reviews but not business data
   if 'both' ==> It will scrape both reviews and business data

3. limit
   How many reviews you want to scrape required only when you are scraping reviews (option=='reviews' OR option=='both')
   if you don't put any limit in it. It will scrape all the reviews of this business
4. business_category
   Enter category of business you want to scrape (like==> hotel, restaurant, etc.)

# API fields for Database

There are also four fields for Fetching data from database

1.link--> paste link here to get data from database

2. option --> what you want to get (profile, reviews, both)
   if 'profile' ==> It will fetch data of business but not reviews
   if 'reviews' ==> It will fetch reviews but not business data
   if 'both' ==> It will fetch both reviews and business data
3. rating --> To fetch reviews of specific rating ()
   Of Which Rating Reviews you want to Fetch Required only when you are fetch reviews (option=='reviews' OR option=='both')
   if you don't put any limit in it. It will fetch all the reviews of this business
4. limit
   How many reviews you want to Fetch Required only when you are fetch reviews (option=='reviews' OR option=='both')
   if you don't put any limit in it. It will fetch all the reviews of this business
