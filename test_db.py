import dbconn

f = open('gme_titles.txt', 'r', encoding='utf8')
for line in f:
    dbconn.insert_reddit_post('GME', line.strip())
print("DONE")
