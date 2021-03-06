# Stonks Only Go Up

With the events of /r/wallstreetbets hitting the mainstream over short squeezing of GME and AMC, there has been increased interest and scrutiny of social media's impact on retail investors and the larger market. Various subreddits for different types of investors, Tiktok traders, and Twitter feeds have become some of the more popular forms of information. We aim to scrape the information off certain subreddits, feeds, and popular social media trades to identify which individual stocks are trending. Then using live market data, we will create a paper trading account to simulate what happens if we trade on that information. We plan to set up several different strategies based on timing, whether sentiment is similar across platforms, whether there are any outliers which correlate stronger with positive trades, and whether there are particular financial vehicles (crypto, options, pennystocks, stonks) that are more susceptible.

## Vision

For individual hobbyists who are interested in the potential applications of data science when it comes to analyzing the impact of social media on the market, "Stonks Only Go Up" is a web-based application that provides sentiment analysis on trending stocks with a paper trading integration to test how reliable this information can predict market outcomes. Unlike many other trading applications that utilize machine-learning algorithms for market forecasting, Stonks Only Go Up will remain free and open-source.

## Personas

#### **1. Rita**

Rita, age 24, is a supervisor at her local Walmart in Bucks County. After graduating high school, she didn't go to college, and was instead eager to start climbing up the retail ladder. After having a rough time moving out of her parents house to live alone as soon as she turned 18, financial stability and independence became the primary concern in her life. She finally makes enough money to pay her own bills but has been growing increasingly anxious about her future and long-term financial growth. 

For this reason, Rita has been wanting to start investing her income for a while now, but she doesn't know how to start. She's been following the stock market for a while and wants to keep learning more about investment and trading strategies - she wants to paper-trade to be as prepared as possible before she starts to stake her own money. She is looking for software tools to help keep her updated on potential investments since she is busy working full-time. Rita doesn't have any particular technical expertise with computers, but she is definitely literate enough to use a web app.

#### **2. John**

John, age 23, is a junior at Temple University majoring Computer Science with a Data Science Minor. He was working as a waiter at a local pizzeria to earn some money to help pay for his tuition but lost his job due to the pandemic. John has been eyeing the stock market for some time now and realized it was a reasonable time to start investing due to the economic impact caused by Covid-19. 
  
John has developed a solid background in data science and machine learning and feels that he is ready to start a new chapter in the stock market industry. He is in search of a user-friendly platform where he can test out his studies and proceed with multiple demo runs before investing real funds. John is confident that with his previous education in data science might be beneficial with algorithm trading and testing. 

#### **3. Adam**

Adam, age 18, is a freshman at Temple university majoring in Business. He just graduated high school and was the starting quarterback for the last three years for his highschool. Aside from spending a few hours a week helping his dad out with the family business Adam likes to spend his time scrolling through TikTok and other social media applications to pass the time. Adam hopes to run his own business while also being a social media influencer.

Adam has been a hardcore reddit user since middle school and was always a part of the community. He's understood how it works and is a member of a few big groups. He is a member of the WallStreetBets subreddit and has been following the GameStop & AMC hype train since the beginning. He follows the Reddit page on a daily basis to know what's going on in the market and hold conversation with other people in his major. He is particularly interested in the next big short squeeze and sees the stock market more as a hobby than a career.

#### **4. Harold**

Harold, age 65, is a retired bank teller with a moderately-sized nest egg which he grew from long-term, traditional, investing practices. He had some trouble adapting when his bank went digital, but became proficient at using simple data entry and organization software. However, his computer skills do not extend much further, as the concept of the internet is a bit confusing for him. He prefers the paper and television-based news sources for obtaining the latest stock information. When in doubt, he'll call his broker.

Having worked at a bank for most of his career, Harold has heard his fair share of investment advice. With day-trading being faster-paced than ever, Harold feels that he needs to listen in on the online conversation to keep up with young investors. Wanting to keep busy and to grow his retirement fund without breaking his back, Harold seeks out a simplified way of keeping up with the social-media influence that has taken over the world of day-trading. He feels that if he can understand the impact that social media posts have on stocks, he can apply his conventional trading knowledge to make some money.

#### **5. Bobby**

Bobby age 25 is sick of his low paying job and is enamored with the Instagram lifestyle of those who are young and rich. He followed the crowd and went to college to obtain a degree but it has not resulted in a profitable career and he remains underemployed. Since Bobby is adept at social media or faking it until you make it he decides to create an online persona in order to manipulate the market. Using his savings, he hires a set of people to curate a fake life for himself, posing in front of private jets and luxury goods he builds up a following as a young guru of the stock market. 

Since Bobby is all about the quick cash grab he looks at low market cap stocks and what has positive sentiment but low volume of posts. He believes that he can purchase large amounts of shares of these stocks that people are positive on but are not hyping then use his social media following to drive the price up. This will make him seem like a prophet since the prices rise after posting and he can make a tidy profit as his investments rise. 

## Feature List

- Search for recent relevant posts on Reddit
- Perform sentiment analysis on recent relevant posts
- Store analyzed posts in a database
- Visualize recent and saved (historical) sentiment data with graphs

You can click [here](https://trello.com/b/mm51f6Tv/stonks-only-go-up) to see our full Trello project board.

## Getting Started

### Requirements

#### Programs

* Python 3
  * See "requirements.txt" for dependencies

#### Credentials

* Reddit API
  * praw.ini
* MySQL
  * databaseconfig.py
* Twitter API
  * IN DEVELOPMENT

### Installation

1. Clone the project into a new directory
2. Install Python3 for your platform from https://www.python.org/downloads/
3. Run the following commands in the project root directory
    ````
    pip install -r requirements.txt
    ````
4. Enter the python shell by running `python3` and do run the following commands
   1. `import nltk`
   2. `nltk.download('vader_lexicon')`
   3. `exit()`
5. Copy "databaseconfig.py" and "praw.ini" to the project root directory
   1. NOTE: API credentials are NOT stored on GitHub for security purposes
   (For demo purposes, please contact the team for credentials if needed)

### Running

To run a development version of the program, simply run 
````
python3 app.py
```` 
from the project's root directory and navigate to http://127.0.0.1:8050 in a web browser. 
