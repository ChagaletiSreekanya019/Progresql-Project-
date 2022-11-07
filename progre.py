import psycopg2
import psycopg2.extras
from bs4 import BeautifulSoup
import requests

hostname="localhost"
database="postgres"
username="postgres"
pwd="sunitha123"
port_id=5432
#to avoid the error of varable not exist....... 
con=None
cur=None

try:
    con=psycopg2.connect(
    host=hostname,
    dbname=database,
    user=username,
    password=pwd,
    port=port_id,
    )

    cur=con.cursor()

#inserting data.......
    url="https://www.imdb.com/india/top-rated-indian-movies/"
    page=requests.get(url)
    soup=BeautifulSoup(page.text,"html.parser")
    tbody=soup.find("tbody",class_="lister-list")
    b=tbody.find_all("tr")
    m=[]
    for i in b:
        d=[]
        movie=[]
        movie_name=i.find("td",class_="titleColumn").a.get_text()
        d.append(movie_name)
        movie_link=i.find('td',class_="titleColumn").a["href"]
        link='https://www.imdb.com'+movie_link
        movie.append(link)
        for i in movie:
            page=requests.get(i)
            soup=BeautifulSoup(page.text,"html.parser")
            Detail=soup.find("section",cel_widget_id="StaticFeature_Details")
            s=Detail.find("div",class_="sc-f65f65be-0 ktSkVi")
            li_=s.find('li',class_="ipc-inline-list__item").a.get_text()
            w=li_[0:-7]
            d.append(w)
            m.append(d)

#inserting the multiple reagardins........
    for d in m:
        cur.execute("INSERT INTO Movie_Details(movies_name,release_date) VALUES (%s,%s)", d)
    print("List has been inserted to sree table successfully...")
    con.commit()
#creating database table........
    create_script="""CREATE TABLE IF NOT EXISTS Movie_Details(
        movies_name varchar(50),
        release_date varchar(30))"""
    cur.execute(create_script)
    con.commit()
    cur.execute('''SELECT * from Movie_Details''')
#to take two rows......
    # result = cur.fetchone()
    # print(result)
    result = cur.fetchall()
## fetching the data harizontally......
    # print(result)

#to get details one by one .......   
    for row in result:
        print("movie_name = ", row[0], )
        print("realease_date = ", row[1])
except Exception as error:
    print(error)
#lastly closing connections......
finally:
    if cur is not None:
        cur.close()
    if con is not None:
        con.close()