import os
import shutil
import pywintypes
from win10toast import ToastNotifier
from main_backend_test6nof import main
from manage_file import ManageFile
from datetime import datetime
from datetime import timedelta
import time
import csv

current_dir = os.getcwd()
toast = ToastNotifier()
toast.show_toast("File Organizer", "The process has been started", duration=5)
os.chdir(r"E:\\Work\Documents\\term2\\main_group")

MAIN = main()
def fool():
    file_name = 'list_keywords.csv'
    while(True):
        print(3)

        now = datetime.now()
        H = now.strftime("%H")
        M = now.strftime("%M")
        fa = timedelta(hours=int(H),minutes=int(M))

        read = open("config.txt","r")
        set_time = ""
        twitter_update = ""
        crawler_update = ""
        for i in read:
            temp = i.split(" ")
            if(temp[0] == "setTimeUpdate"):
                set_time = temp[1].split(":")
            if(temp[0] == "twitterUpdate"):
                twitter_update = temp[1]
            if(temp[0] == "crawlerUpdate"):
                crawler_update = temp[1]
        reset = timedelta( hours=int(set_time[0]),minutes=int(set_time[1]) )
        check = fa==reset

        if(check):
            start = time.time()
            if(crawler_update == "True"):
                print("1")
                toast.show_toast("File Organizer", "webcrawler "+"started update", duration=5)
                MAIN.update_program_crawler("all", '')
            toast.show_toast("File Organizer", "webcrawler "+"has been update "+str(int(time.time()-start)), duration=5)
            print(twitter_update, "True")
            start2 = time.time()
            if(twitter_update.split("\n")[0] == "True"):
                print("2")
                with open(file_name, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    print(reader)
                    first=0
                    for row in reader:
                        if( first > 0 ):
                            print(row)
                            toast.show_toast("File Organizer", f'"{row[0]}"'+"started update", duration=5)
                            MAIN.update_program_twitter("en", 50, row[0])
                            MAIN.update_program_twitter("th", 50, row[0])
                            toast.show_toast("File Organizer", f'"{row[0]}"'+"has been update", duration=5)

                        first += 1
            toast.show_toast("File Organizer "+str(int(time.time()-start2)), "end update", duration=5)
        else:
            time.sleep(1)

fool()