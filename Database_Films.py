import sqlite3
import Colors

clr = Colors.bcolors

class Film():

    def __init__(self,Film_Name,Film_Link,Film_Release_Date,Film_Time,Film_Genre,Film_Score,Film_Summary,Film_Age_Rate,Film_EN_Name,Film_Formats):
        self.Film_Name = Film_Name
        self.Film_Link = Film_Link
        self.Film_Formats = Film_Formats
        self.Film_Time = Film_Time
        self.Film_Genre = Film_Genre
        self.Film_Score = Film_Score
        self.Film_Summary = Film_Summary
        self.Film_Age_Rate = Film_Age_Rate
        self.Film_EN_Name = Film_EN_Name
        self.Film_Release_Date = Film_Release_Date


    def __str__(self):

        return ("""
                Hey there!
                """ + """
                {} released today!

                Here is some information below:

                Release Date: {}

                Formats: {}

                Total Time: {}

                Genre: {}

                Score: {}

                Age Rate: {}

                Summary: {}

                Would you want to get ticket for it? Here is the link below to do so!

                Link: {}

                """).format(clr.BOLD + clr.OKBLUE + self.Film_Name + clr.ENDC,
                            clr.BOLD + clr.YELLOW + self.Film_Release_Date + clr.ENDC,
                            clr.BOLD + self.Film_Formats + clr.ENDC, clr.BOLD + clr.OKGREEN + self.Film_Time + clr.ENDC,
                            clr.BOLD + clr.MAGENTA + self.Film_Genre + clr.ENDC, clr.BOLD + self.Film_Score + clr.ENDC,
                            clr.BOLD + clr.RED + self.Film_Age_Rate + clr.ENDC, clr.BOLD + self.Film_Summary + clr.ENDC,
                            self.Film_Link)
        



    def text_of_mail(self,en_name,tr_name,picture_link,film_director,film_players):

        tag = "h1"

        if (en_name != "Not Found"):
            name = en_name
        else:
            name = tr_name

        if (len(name) > 29):
            tag = "h2"

        return """
        <html>
        <head>
            <title></title>
        </head>
        <body>

            <div id="main-div" style="width: 675px; background-color: rgb(237, 237, 237); border: 4px solid black;">
                
                <div id="cinemaximum-pic" style="border-bottom: 4px solid black;">
                    <a href="https://www.cinemaximum.com.tr/"><img src="https://www.cinemaximum.com.tr/Assets/Cgv/assets/images/cinemaximum-logo.png" width="200" height="50" style="margin-left: auto; margin-right: auto; margin-top: 6px; margin-bottom: 6px; display: block;"></a>
                </div>

                <div id="all-content" style="margin-top: 5px; margin-left: 5px; margin-bottom: 5px; overflow: hidden;">
                    
                    <div id="image-poster" style="width: 205px; height: 313px; float: left;">
                        <a href='""" + self.Film_Link + """'><img src='""" + picture_link + """' width="205" height="313"></a>
                    </div>

                    <div id="all-movie-info" style="float: left; margin-left: 24px; width: 430px; text-decoration: none;">
                        
                        <div id="movie-name" style="height: 40px; width: 400px;">
                            <""" + tag + """>""" + name + """</""" + tag + """>
                        </div>

                        <div id="border-set" style="border: 0.5px solid black;"></div>

                        <div id="movie-info" style="margin-top: 10px; font-size: 17px;">
                            <div id="yonetmen">
                                <span>
                                    <strong>Yönetmen: </strong>
                                </span>
                                <span>
                                    """ + film_director + """
                                </span>
                            </div>

                            <div id="oyuncular" style="margin-top: 2px;">
                                <span>
                                    <strong>Oyuncular: </strong>
                                </span>
                                <span>
                                    """ + film_players + """
                                </span>
                            </div>

                            <div id="vizyon-tarihi" style="margin-top: 12px;">
                                <span>
                                    <strong>Vizyon Tarihi: </strong>
                                </span>
                                <span>
                                    """ + self.Film_Release_Date + """
                                </span>
                            </div>

                            <div id="sure" style="margin-top: 2px;">
                                <span>
                                    <strong>Süre: </strong>
                                </span>
                                <span>
                                    """ + self.Film_Time + """
                                </span>
                            </div>

                            <div id="tur" style="margin-top: 2px;">
                                <span>
                                    <strong>Tür: </strong>
                                </span>
                                <span>
                                    """ + self.Film_Genre + """
                                </span>
                            </div>

                        </div>

                        <div id="buy-ticket-button" style="margin-top: 25px; margin-left: 80px;">
                            <a href='""" + self.Film_Link + """'><button type="button" id="button-settings" style="background-color: white; height: 48px; width: 255px; padding: 11px 26px; font-size: 18px; font-weight: 400; cursor: pointer; display: inline-block; background-color: #F966B0; color: #000; border-radius: 4px; text-align: center; outline: none; box-shadow: none; border: none;">Bilet Al</button></a>
                        </div>

                    </div>

                </div>

            </div>

        </body>
        </html>
        """


class Film_Database():

    def __init__(self):

        self.connect_databse()

    def connect_databse(self):

        self.connection = sqlite3.connect("Cinemaximum.db")
        self.cursor = self.connection.cursor()
        query = "create table if not exists Tbl_Film (" \
                "Film_Name text," \
                "Film_Link text," \
                "Film_Release_Date text," \
                "Film_Time text," \
                "Film_Genre text," \
                "Film_Score text," \
                "Film_Summary text," \
                "Film_Age_Rate text," \
                "Film_EN_Name text," \
                "Film_Formats text)"

        self.cursor.execute(query)
        self.connection.commit()


    def print_movies(self):

        query = "select * from tbl_film"
        self.cursor.execute(query)
        films = self.cursor.fetchall()

        if (len(films) != 0):

            for i in films:
                film = Film(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9])
                print(film)

        else:
            print("No film found on databse.")


    def add_movie(self,film):

        query = "insert into tbl_film values (@p1,@p2,@p3,@p4,@p5,@p6,@p7,@p8,@p9,@p10)"
        self.cursor.execute(query,(film.Film_Name,film.Film_Link,film.Film_Release_Date,film.Film_Time,film.Film_Genre,film.Film_Score,film.Film_Summary,film.Film_Age_Rate,film.Film_EN_Name,film.Film_Formats))
        self.connection.commit()

    def delete_movie(self,name_of_film):

        query = "delete from tbl_film where film_name = @p1"
        self.cursor.execute(query, (name_of_film,))
        self.connection.commit()

    def check_if_film_exists(self,name):

        query = "select * from tbl_film where film_name = @p1"
        self.cursor.execute(query,(name,))
        film = self.cursor.fetchall()

        if (len(film) == 0):
            return 0
        else:
            return 1

    def get_movie_info(self):

        query = "select * from tbl_film"
        self.cursor.execute(query)
        films = self.cursor.fetchall()
        return films
