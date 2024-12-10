---
categories:
- Workflows
description: Explore the SearchPipeline class for efficient web data retrieval and
  summarization based on specific topics.
tags:
- SearchPipeline
- Data Retrieval
- Web Summarization
- AI Workflows
- Artificial Intelligence
---

I'll create a markdown documentation file for the SearchWeb singleton implementation you provided.

# SearchWeb

## Overview
SearchWeb is a singleton template that performs web searches and returns structured results. It allows users to search the web with specific queries, language preferences, and control over the number of results returned. Each search result includes the original query, link, snippet, and title of the found web pages.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| query | str | Query to search for |
| lang | str | Language to search in (defaults to "en") |
| n_results | int | Number of results to return (range: 1-25, default: 5) |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| query | str | Query used for search |
| link | str | Link of the search result |
| snippet | str | Snippet of the search result |
| title | str | Title of the search result |

#### Usage

SearchWeb instance can be used in data generation as follows:

```python
from dria import DriaDataset, DatasetGenerator
from dria.factory.search import SearchWeb
import asyncio

my_dataset = DriaDataset(
    name="searches",
    description="A dataset for pages",
    schema=SearchWeb.OutputSchema,
)

generator = DatasetGenerator(dataset=my_dataset)


instructions = [
    {"query": "Istanbul'daki en iyi kebapçılar", "lang": "tr", "n_results": 5},
    {"query": "Best kebap places in Istanbul", "lang": "en", "n_results": 5},
]

asyncio.run(
    generator.generate(
        instructions=instructions,
        singletons=SearchWeb,
    )
)
```

Expected output:

```json
[
  {
    "query": "Istanbul'daki en iyi kebapçılar",
    "link": "yemek.com/en-iyi-kebapcilar/",
    "snippet": "Lakin İstanbul'daki en iyi kebapçılar listemizde yer alan kebapların da \"Ah bu kebabı Adana'da yemek vardı!\" dedirtmeyeceğinin de sözünü verebiliriz. Sözün kısası, canınız her kebap yemek istediğinde gönül rahatlığıyla, büyük bir iştahla gidebileceğiniz İstanbul'daki en iyi kebapçılar karşınızda!",
    "title": "İstanbul'da Kebap Yiyebileceğiniz En İyi 10 Mekan - Yemek.com"
  },
  {
    "query": "Istanbul'daki en iyi kebapçılar",
    "link": "onedio.com/haber/kokusuyla-bile-sizi-mest-etmeye-yetecek-istanbul-daki-en-iyi-18-kebap-mekani-1011496",
    "snippet": "Kokusuyla Bile Sizi Mest Etmeye Yetecek! İstanbul'daki En İyi 23 Kebap Mekanı ... Avrupa Yakası'ndaki kebapçılar ise modern sunumları ve geniş menü seçenekleriyle konuklarına kapılarını açıyor. Haliyle İstanbul'un her iki yakası da kebap severler için adeta bir cennete dönüşüyor. Peki, İstanbul'da kebap nerede yenir?",
    "title": "Kokusuyla Bile Sizi Mest Etmeye Yetecek! İstanbul'daki En İyi 23 Kebap ..."
  },
  {
    "query": "Istanbul'daki en iyi kebapçılar",
    "link": "blog.obilet.com/istanbulun-en-iyi-kebapcilari/",
    "snippet": "Gaziantep mutfağının en lezzetli mezelerini, kebaplarını tadabileceğiniz mekanlardan biri de Çanak Kebap & Katmer. İstanbul'daki en iyi kebapçılardan olan Çanak Kebap & Katmer'e giderseniz mezelerden zeytin piyazı, acılı peynir ezmesini, kebap olarak ise mekanın spesiyali olan Çanak Acılı Kebabı tatmanızı tavsiye ederim.",
    "title": "İstanbul'daki En İyi 14 Kebapçı - İstanbul Lezzet Rehberi - obilet"
  },
  {
    "query": "Istanbul'daki en iyi kebapçılar",
    "link": "gezilinki.com/istanbulun-en-iyi-kebapcilari-istanbulun-en-basarili-10-kebapcisi/",
    "snippet": "Türk ve Orta Doğu mutfağının İstanbul'daki en eski temsilcilerinden biri olan mekanda onlarca kebap çeşidi bulabilirsiniz. Adres: Orman Caddesi No: 8, Florya, İstanbul. 1924 İstanbul - Beyoğlu. ... Eminönü'nde bulunan bu mekan İstanbul'un en iyi kebapçılar ...",
    "title": "İstanbul'un En İyi Kebapçıları - İstanbul'un En ... - GeziLinki"
  },
  {
    "query": "Istanbul'daki en iyi kebapçılar",
    "link": "www.yasemin.com/yasam/haber/2982424-istanbulda-kebap-nerede-yenir-en-iyi-kebapcilarin-adresleri-2022",
    "snippet": "ADRES: Koca Mustafa Paşa M. Gümüşyüzük S. No: 5/A Samatya / Fatih / İstanbul; HARBİ ADANA OCAKBAŞI Ortaköy'de yer alan Harbi Adana Ocakbaşı, kebap yemek isteyenlerin en sık gittiği yerler arasında yer almaktadır.Kebaplarında kullandıkları et seçimi ve yanında servis edilen birçok alternatifle Harbi Adana Ocakbaşı Vedat Milor'dan tam not almayı başarmıştır.",
    "title": "İstanbul'da kebap nerede yenir? En iyi kebapçıların adresleri 2022"
  },
  {
    "query": "Best kebap places in Istanbul",
    "link": "yummyistanbul.com/kebab-istanbul/",
    "snippet": "There are at least 110 different kebabs only in Turkey, and each one has its unique taste. Almost every city in Turkey has its own style of köfte and kebab.. You may find yourself stumped when it comes to choosing a kebab from dozens of different kebabs, so having a peek at our blog article on the popular types of Turkish kebabs might be useful: 20 Best & Most Famous Turkish Kebabs /w Photos",
    "title": "Best Kebab in Istanbul: Top 12 Kebab Restaurants Right Now"
  },
  {
    "query": "Best kebap places in Istanbul",
    "link": "istanbulclues.com/best-kebab-restaurants-in-istanbul/",
    "snippet": "Best Turkish Kebab Restaurants in Istanbul 2024. The best Turkish kebab restaurants in Istanbul are mostly found in historical districts. Most of the famous kebab restaurants are located in Fatih, which covers Sultanahmet and its surroundings. On the other hand, there are good restaurants in Beyoglu (aka Taksim) and on the shores of the Bosphorus.. The top 10 kebab restaurants in this article ...",
    "title": "12 Best TURKISH KEBAB Restaurants in Istanbul (2024)"
  },
  {
    "query": "Best kebap places in Istanbul",
    "link": "yummyistanbul.com/best-doner-kebab-in-istanbul/",
    "snippet": "One of the best doner kebab in Istanbul is also served up here and it is very close to Sultanahmet hotels district. If you're staying at a hotel near Eminonu, or Sultanahmet your location is very accessible and should be reachable within 20 minutes!",
    "title": "8 Places With The Absolute Best Doner Kebab In Istanbul"
  },
  {
    "query": "Best kebap places in Istanbul",
    "link": "turkeythings.com/istanbul-kebab-restaurants/",
    "snippet": "1 - Bayramoğlu Döner Kebab. Located on the Asian side, Bayramoğlu Döner is an affordable restaurant that exclusively serves döners. It is unquestionably the premier döner kebab spot in Istanbul, with visitors going as far as taking a road trip to queue for a table or a takeaway sandwich.Despite its lack of sophistication, local celebrities and travelers frequently choose to dine there ...",
    "title": "11 Best Kebab Restaurants in Istanbul in 2024 - Turkey Things"
  },
  {
    "query": "Best kebap places in Istanbul",
    "link": "www.yelp.com/search?cflt=kebab&find_loc=Istanbul",
    "snippet": "Best Kebab near you in Istanbul, Turkey - Fikret Adana Ocakbaşı, Dürümzade, Old Ottoman Cafe & Restaurant, Şehzade Cağ Kebap, Taç Mahal Kebap Pide Lahmacun, Ziya Baba, Bahçeşehir Kebab Evi, Karadeniz Pide Salonu, Abooov Kebap, İskender Nişantaşı ... Thi sis the best doner in Istanbul. I have tried many doner places since i used to ...",
    "title": "THE BEST 10 Kebab in ISTANBUL, TURKEY - Updated 2024 - Yelp"
  }
]
```