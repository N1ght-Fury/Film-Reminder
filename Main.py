import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale
import Inform_User as mail
import time
import User_Mail_Database
import Database_Films
import Database_Backup
import Colors

mail_data = User_Mail_Database.Mail_Database()
cinema_data = Database_Films.Film_Database()
film_backup =   Database_Backup.Film_Database_Backup()
clr = Colors.bcolors

locale.setlocale(locale.LC_ALL, "")

print("""
Press '1' to organize user database.
Press '2' to start the program.
Press 'q' to exit.
""")

while True:

    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year
    today = datetime(year, month, day)

    number = input("Start Command: ")

    if (number == "1"):

        print("""
        Enter '1' to see all users.
        Enter '2' to update a specific user status or mail adress.
        Enter '3' to delete a user.
        Enter '4' to add a new user.
        Enter '5' to back to main menu.
        Enter 'q' to exit program. 
        """)

        while True:

            command = input("Command for mail: ")

            #See Users
            if (command == "1"):

                #Shows All Users on Database If There Are Any
                if (not mail_data.any_user()):
                    print("\nNo user found on database.\n")
                    continue

                mail_data.show_users()

            #Update User
            elif (command == "2"):

                #Checking If There Are Any Users On Database
                if (not mail_data.any_user()):
                    print("\nNo user found on database.\n")
                    continue

                mail = input("Enter a mail adress you want to change: ").lower()

                if (mail_data.check_if_user_exsits(mail) == 0):
                    print("No mail found as '" + mail + "'. Please try again.")
                else:
                    print("What would you want to change? "
                          "To go back, enter 'q' , to change mail, "
                          "enter M, to change status, enter S:")

                    change_what = input().upper()

                    #Updating User Mail
                    if (change_what == "M"):
                        new_mail = input("Enter a new mail adress: ")
                        mail_data.update_user_status_and_mail(mail, True, new_mail)
                        print(mail, "changed to", new_mail + ".")

                    #Updating Status (if 0, wont receive mails, else will)
                    elif (change_what == "S"):
                        print("Would you want to get mails or not? (Y/N)")
                        yes_no = input().upper()
                        if (yes_no == "Y"):
                            mail_data.update_user_status_and_mail(mail, True, mail)
                            print(mail ,"will now receive mails.")
                        elif (yes_no == "N"):
                            mail_data.update_user_status_and_mail(mail, False, mail)
                            print(mail ,"will not receive mails anymore.")
                        else:
                            print(clr.RED + "Wrong command. Please try again." + clr.ENDC)
                            continue


                    elif (change_what == "Q"):
                        print("You are back to menu.")


            #Delete User
            elif (command == "3"):

                #Checking If There Are Any Users On Database
                if (not mail_data.any_user()):
                    print("\nNo user found on database.\n")
                    continue

                mail = input("Enter a mail address you want to delete: ").lower()
                if (mail_data.check_if_user_exsits(mail) == 0):
                    print("No mail address found as '" + mail + "'. Please try again.")
                else:
                    print("Are you sure you want to delete this address? Y/N")

                    #Deleting Mail Address From Database
                    yes_no = input().upper()
                    if (yes_no == "Y"):
                        mail_data.delete_user(mail)
                        print(mail,"successfully deleted.")
                    elif (yes_no == "N"):
                        print("Process canceled.")
                        continue
                    else:
                        print("Please try again.")

            #New User
            elif (command == "4"):
                print("Enter a new mail address:")
                mail = input().lower()
                print("Would you want to get mails? Y/N:")
                yes_no = input().upper()

                #Adding New Mail Address to Database
                if (yes_no == "Y"):
                    user = User_Mail_Database.User(mail, True)
                    mail_data.add_user(user)
                    print(mail,"successfully added to database.")
                elif (yes_no == "N"):
                    user = User_Mail_Database.User(mail, False)
                    mail_data.add_user(user)
                    print(mail, "successfully added to database. Be aware that you wont receive any mails.")
                else:
                    print(clr.RED + "Wrong command. Please try again." + clr.ENDC)

            elif (command == "5"):
                #Going Back to Main Menu
                print("You are on main menu right now.")
                break
            elif (command == "q"):
                quit()
            else:
                print(clr.RED + "Wrong command. Please try again." + clr.ENDC)


    elif (number == "2"):

        while True:


            now = datetime.now()
            h = now.hour
            m = now.minute
            s = now.second
            
            print("Run time: {}:{}:{}".format(h,m,s))
            
            #Getting HTML content of cinemaximum/akasya
            #You can select a specific movie theater from here: https://www.cinemaximum.com.tr/sinemalar
            try:
                url = "https://www.cinemaximum.com.tr/akasya-sinema-salonu?tarih=25-01-2019"
                response = requests.get(url)
                html_content = response.content
                soup = BeautifulSoup(html_content, "html.parser")

            except:
                print("Something unexpected happened!")
                time.sleep(300)
                continue

            total_user = mail_data.any_user()

            #Check if there are users on database
            if (total_user == 0):
                print("No user found on databse. You have to add atleast one user to continue.")
                user_mail_adress = input("Mail: ").lower()
                print("Would you want to receive mails?")
                print(clr.RED + "(If you are running this program for the first time, \nwe recommend "
                      "turning notifications off if you don't\nwant get several mails"
                      " in your first run.\nAfter first run, movies will be added to database"
                      " and you can turn notifications on.)" + clr.ENDC)

                stat = input("Y/N: ").upper()

                #Checking Stat
                if (stat == "Y"):
                    stat = True
                elif (stat == "N"):
                    stat = False
                else:
                    print("Wrong command.")
                    continue

                user = User_Mail_Database.User(user_mail_adress, stat)

                #Adding Mail to Database
                mail_data.add_user(user)
                print(user_mail_adress,"successfully added to database")

            #Add movie links to a list
            link_of_films = soup.find_all("a",{"class":"movie-image"})
            list_of_films = list()
            for i in link_of_films:
                list_of_films.append("https://www.cinemaximum.com.tr" + i['href'])

            #Getting Posters
            picture_of_films = soup.find_all("img",{"class":"img-responsive"})
            list_of_pictures = list()
            for i in picture_of_films:
                list_of_pictures.append(i['src'])

            #Deleting last item of film list
            del list_of_pictures[-1]

            #Analysing every link
            for link,index in zip(list_of_films,range(0,len(list_of_films))):

                url = link
                response = requests.get(url)
                html_content = response.content
                soup = BeautifulSoup(html_content, "html.parser")

                film_information = soup.find_all("strong")

                #Film Informations
                film_release_date = ""
                film_time = ""
                film_summary = ""
                film_genre = ""
                film_score = ""
                film_age_rate = ""
                film_en_name = ""
                film_formats = ""
                film_director = ""
                film_players = ""

                for info in film_information:

                    #Getting info
                    info = info.parent.text
                    info = str(info)

                    if ("Formatlar: " in info):
                        info = info.replace("Formatlar: ", "")
                        film_formats = info

                    elif ("Vizyon Tarihi: " in info):
                        info = info.replace("Vizyon Tarihi: ", "")
                        film_release_date = info

                    elif ("Süre: " in info):
                        info = info.replace("Süre: ", "")
                        film_time = info

                    elif ("Tür: " in info):
                        info = info.replace("Tür: ", "")
                        film_genre = info

                    elif ("Özet : " in info):
                        info = info.replace("Özet : ", "")
                        film_summary = info

                    elif ("Yönetmen: " in info):
                        info = info.replace("Yönetmen: ", "")
                        film_director = info

                    elif ("Oyuncular: " in info):
                        info = info.replace("Oyuncular: ", "")
                        film_players = info



                #Getting Film Score
                film_score_html = soup.find_all("span", {"class": "icon icon-star"})
                film_score = ""

                for score in film_score_html:
                    score = score.parent.text
                    score = str(score)
                    score = score.replace(" ", "")
                    film_score = score

                #Getting Film Age Rate
                if ("icon icon-ai-genel" in str(html_content)):
                    film_age_rate = "Genel İzleyici"

                elif ("icon icon-ai-7" in str(html_content)):
                    film_age_rate = "7+"

                elif ("icon icon-ai-13" in str(html_content)):
                    film_age_rate = "13+"

                elif ("icon icon-ai-15" in str(html_content)):
                    film_age_rate = "15+"

                elif ("icon icon-ai-18" in str(html_content)):
                    film_age_rate = "18+"

                #Getting English Name
                film_en_name_html = soup.find_all("div", {"class": "movie-title"})
                for en in film_en_name_html:
                    en = en.h3.text
                    en = str(en)

                    if (en == ""):
                        film_en_name = "Not Found"
                    else:
                        film_en_name = en


                #Getting Film Turkish Name
                original_name = str()
                for tr in soup.find_all("h1"):
                    original_name = tr.text

                if (film_players == ""):
                    film_players = "Animasyon Filmi"


                #Adding Film To Database and Sending Mail
                if (cinema_data.check_if_film_exists(original_name) == 0):

                    film_details = Database_Films.Film(original_name, url, film_release_date, film_time, film_genre,
                                                       film_score, film_summary, film_age_rate, film_en_name,
                                                       film_formats)
                    #Adding Film to Main Database
                    cinema_data.add_movie(film_details)
                    print(film_details)

                    #Adding Film to Backup Database
                    film_backup.add_movie(film_details)

                    picture = list_of_pictures[index]

                    #Sending Mail
                    mail_addresses = mail_data.get_user_mail()
                    for user, stat in mail_addresses:
                        if (stat == 1):
                            mail.send_mail(user, film_details.text_of_mail(film_en_name,original_name,picture,
                                                                           film_director,film_players))


                    #Downloading poster
                    try:
                        response = requests.get(list_of_pictures[index])
                    except:
                        print("Something unexpected happened while getting to download poster.")

                    if (film_en_name != "Not Found"):
                        original_name = film_en_name
                        original_name = original_name.replace("?","")

                    original_name = original_name.replace("?","")
                    original_name = original_name.replace(":","")
                    original_name = original_name.replace("*","")
                    original_name = original_name.replace("?","")

                    try:

                        with open("C:\\Users\\Talha\\Desktop\\Python Files"
                                  "\\Film_Project"
                                  "\\Film_Posters\\" + original_name + ".png",
                                  'wb') as f:
                            f.write(response.content)
                    except:
                        print("Something unexpected happened while trying to download poster.")

                else:

                    #Updating Film Score for Backup Database
                    film_backup.update_movie_score(film_score,original_name)


            #Check if 50 days has passed since movie released
            all_movies = cinema_data.get_movie_info()

            for movie_name, s, movie_date, f, g, h, j, k, l, i in all_movies:

                #Converting Date of Film to Datetime
                movie_date = list(movie_date)
                day = int(movie_date[0] + movie_date[1])
                month = int(movie_date[3] + movie_date[4])
                year = int(movie_date[6] + movie_date[7] + movie_date[8] + movie_date[9])

                movie_date = datetime(year, month, day)

                #Finding days
                day = (today - movie_date).days
                #print(movie_name, day)
                if (day >= 90):
                    cinema_data.delete_movie(movie_name)
                    print(movie_name, "deleted from database.")

            #Waiting for One Day

            now = datetime.now()
            h = now.hour
            m = now.minute
            s = now.second

            if (m != 0):
                h += 1

            if (m != 0):
                wm = 60 - m
            else:
                wm = 0

            if (s != 0):
                ws = 60 - s
            else:
                ws = 0

            wh = 9 - h
            wh = wh + 24
            
            print("Process finished. Waiting for {} hours, {} mins, {} secs.".format(wh,wm,ws))
            
            wh = 3600 * wh
            wm = wm * 60

            waiting_time = wh + wm + ws
            
            print("End time: {}:{}:{}\n".format(h - 1,m,s))
            
            time.sleep(waiting_time)

    elif (number == "q"):
        exit()

    else:
        print("\nWrong command. Please try again.\n")
