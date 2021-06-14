from Twitter_API_4_test import Twitter_API
from Website_crawler_15_test import websites_crawler
from NLP_4test import NLP
from manage_file import ManageFile

import csv
import pandas
import re
from collections import Counter
import sys
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import geopy

from datetime import timedelta
from datetime import datetime
import time

import os

class main(Twitter_API, websites_crawler, NLP):
    def __init__(self):
        self.nlp_main = NLP()
        Twitter_API.__init__(self, self.nlp_main)
        websites_crawler.__init__(self, self.nlp_main)
        csv.field_size_limit(256<<10)

        self.geolocator = Nominatim(user_agent="Chain_Anda")

    # run combin twitter and website
    def run_all(self, lang, count, keyword, since, until):

        keyword = keyword.lower()
        self.lang = lang
        self.count = count
        self.keyword = keyword
        self.since = since
        self.until = until

        # ตรงนี้กะว่าจะเอาไว้ตรวจสอบคำแต่พอทำไปทำมา method go_twitter ทำได้ดีกว่า
        check = self.check_keyword(keyword)
        
        self.array_sentiment = []
        self.array_sentiment_twi = []
        self.array_sentiment_web = []

        a = time.time()
        # Go search twitter and check that keyword has search yet
        self.go_twitter(lang, count, keyword, since, until)
        print("Time: ", time.time() - a)
        print("="*10+"End Find Twitter"+"="*10)

        # run search crawler
        self.main_crawler(keyword, lang, since, until)

        # bring file that main_twitter and main_crawler has wrote before to cut text by NLP and sorting word for show on GUI 
        self.cut_text("WebCrawler", keyword, ["time","header","content","link"], lang, since, until)

        self.cut_text("Twitter", keyword, ["time","content","places"], lang, since, until)

    # run twitter
    def run_twitter(self, lang, count, keyword, since, until):

        keyword = keyword.lower()
        self.lang = lang
        self.count = count
        self.keyword = keyword
        self.since = since
        self.until = until

        # ตรงนี้กะว่าจะเอาไว้ตรวจสอบคำแต่พอทำไปทำมา method go_twitter ทำได้ดีกว่า
        check = self.check_keyword(keyword)

        self.array_sentiment = []
        self.array_sentiment_twi = []
        self.array_sentiment_web = []

        a = time.time()
        # Go search twitter
        self.go_twitter(lang, count, keyword, since, until)
        print(print("Time: ", time.time() - a))
        print("="*10+"End Find Twitter"+"="*10)

        # bring file that main_twitter has wrote before to cut text by NLP and sorting word for show on GUI 
        self.cut_text("Twitter", keyword, ["time","content","places"], lang, since, until)
        print("Time: ", time.time() - a)

    # run webcrawler
    def run_webcrawler(self, lang, keyword, since, until):

        keyword = keyword.lower()
        self.lang = lang
        self.keyword = keyword
        self.since = since
        self.until = until

        # ตรงนี้กะว่าจะเอาไว้ตรวจสอบคำแต่พอทำไปทำมา method go_twitter ทำได้ดีกว่า
        check = self.check_keyword(keyword)

        self.array_sentiment = []
        self.array_sentiment_twi = []
        self.array_sentiment_web = []

        # run search crawler
        a = time.time()
        self.main_crawler(keyword, lang, since, until)
        print(print("Time: ", time.time() - a))

        # bring file that main_crawler has wrote before to cut text by NLP and sorting word for show on GUI 
        self.cut_text("WebCrawler", keyword, ["time","header","content","link"], lang, since, until)
        print("Time: ", time.time() - a)

    # find twitter แบบ update ขัอมูลเองได้
    def go_twitter(self, lang, count, keyword, since, until):
        try:
            print("="*10+"Start Find Twitter"+"="*10)
            read_data = ManageFile("Twitter", keyword+"_Ncut"+lang, ["time","content","places"], "r")

            csv_data = read_data.managefile_main()
            df_in = pandas.DataFrame(csv_data)

            # มีของวันไหนบ้าง
            condition1 = (df_in[0] >= f"{since} 00:00:00")
            condition2 = (df_in[0] <= f"{until} 23:59:59")
            
            temp = [] # temp เก็บวันที่มีในไฟล์นั้นๆ
            df_out = df_in[0][ condition1 & condition2 ].str.split(" ").apply( lambda x: temp.append(x[0]) if x[0] not in temp else None )
            for i in range(len(temp)):
                temp[i] = datetime.strptime(str(temp[i]), "%Y-%m-%d")
            temp.sort(reverse=True)

            # -------------------- set since and until time -----------------------
            now = datetime.now()
            past = now - timedelta(days=7)
            now = datetime.strptime(str(now).split(" ")[0], "%Y-%m-%d")
            past = datetime.strptime(str(past).split(" ")[0], "%Y-%m-%d")

            until_new = until
            since_new = since
            temp_until = datetime.strptime(until_new, "%Y-%m-%d")
            temp_since = datetime.strptime(since_new, "%Y-%m-%d")
            if(temp_until >= temp_since ):
                # set until date
                if(temp_until > now and temp_since > now):
                    return None
                else:
                    if(now > temp_until):
                        until_new = until_new
                    else:
                        until_new = str(now).split(" ")[0]
                # set since date
                if(temp_until < past and temp_since < past):
                    return None
                else:
                    if(past < temp_since):
                        since_new = since_new
                    else:
                        since_new = str(past).split(" ")[0]
            else:
                return None
            # ---------------------------------------------------------------------

            # --------------------- if can't find data ------------------
            if(temp == []):
                #print(since_new, until_new, "DO IT",3)
                print(since_new, until_new, "DO IT")
                self.main_twitter(lang, count, keyword, since_new, until_new)
                return None
            # --------------------------------------------------------

            ######################### only Time period that programe can search #############################
            new_array = []
            end = None
            for k in temp:
                if(k <= now and k >= now - timedelta(days=7)):
                    new_array.append(k)
            #print(new_array,4)
            ##################################################################################################

            # -------------------------------- find starting time -------------------
            point = None
            if(datetime.strptime(until_new, "%Y-%m-%d") not in new_array):
                # บวก 1 วันเป็นช่วงอ้างอิงให้หาวันเมื่อวาน
                point = datetime.strptime(until_new, "%Y-%m-%d") + timedelta(days=1)
            else:
                point = datetime.strptime(until_new, "%Y-%m-%d")
            point = point.strftime("%Y-%m-%d")
            point = datetime.strptime(point, "%Y-%m-%d")
            #print(point,5)
            # -----------------------------------------------------------------------

            # ------------------------------- find ending time ---------------------
            if(since_new not in new_array):
                # กลับไปวันนึงคือการเอาวันพรุ่งนี้
                end = datetime.strptime(since_new, "%Y-%m-%d") - timedelta(days=1)
                new_array.append(end)
            #print(new_array,6)
            # ----------------------------------------------------------------------

            # ------------------------ find specific time --------------------------
            for point_stop in new_array:

                start = point-timedelta(days=1)
                stop = point_stop+timedelta(days=1)
                if(start >= stop):
                    start = str(start).split(" ")[0]
                    stop = str(stop).split(" ")[0]
                    print(start, stop, "DO IT")
                    self.main_twitter(lang, count, keyword, stop, start)
                else:
                    print(start, stop, "DO NOT DO IT")

                point = point_stop
            # ----------------------------------------------------------------------
        except IndexError:
            pass

    def update_program(self, lang, count, keyword, since, until):
        keyword = keyword.lower()

        now = datetime.now()
        date_since = datetime.strptime(str(since), "%Y-%m-%d")
        date_until = datetime.strptime(str(until), "%Y-%m-%d")
        since_t = ""
        until_t = ""
        if(date_since < now-timedelta(days=7)):
            since_t = str(now-timedelta(days=7)).split(" ")[0]
        else:
            since_t = since
        if(date_until > now):
            until_t = str(now).split(" ")[0]
        else:
            until_t = until
        self.main_twitter(lang, count, keyword, since_t, until_t)
        self.main_crawler(keyword, lang, since, until)

        self.cut_text("WebCrawler", keyword, ["time","header","content","link"], lang, since, until)
        self.cut_text("Twitter", keyword, ["time","content","places"], lang, since, until)

    def update_program_twitter(self, lang, count, keyword):
        keyword = keyword.lower()
        until = datetime.now()
        since = until - timedelta(days=7)
        self.main_twitter(lang, count, keyword, str(since).split(" ")[0], str(until).split(" ")[0])

    def update_program_crawler(self, lang, keyword):
        keyword = keyword.lower()
        self.main_crawler(keyword, lang, "", "", True)

    def cut_text(self, folder, keyword, column, lang, since, until):
        # -----------------------read file for content-----------------------
        # เอาไฟล์ที่เลือกเวลาแล้วมาตัวคำ
        read = None
        if(folder == "WebCrawler"):
            read = ManageFile(folder, keyword+"_cut"+lang, column, "r")
        elif(folder == "Twitter"):
            read_data = ManageFile(folder, keyword+"_Ncut"+lang, column, "r")

            # -----------------------อ่านไฟล์เป็น pandas-----------------------
            csv_data = read_data.managefile_main()
            pd_data = pandas.DataFrame(csv_data)
            # --------------------------------------------------------------

            # -----------------------เลือกเวลา-----------------------
            data_ = self.read_time(folder, pd_data, since, until)
            # -----------------------------------------------------

            # -----------------------เขียนไฟล์ชั่วคราว-----------------------
            data_str = data_.to_csv(index = False)
            #print(data_str)
            write_file = open(read_data.path+"\\"+keyword+"_cut"+lang+".csv", "w", newline="")
            write_file.write(data_str)
            write_file.close()
            # -----------------------------------------------------------
            read = ManageFile(folder, keyword+"_cut"+lang, column, "r")
        else:
            read = ManageFile(folder, keyword+"_cut"+lang, column, "r")  

        data = read.managefile_main()
        write_sort_text = ManageFile("GUI_show", keyword+"_ranking_"+str(folder).lower()+lang, ["keyword", "number"], "w")
        write_sort_text_all = ManageFile("GUI_show", keyword+"_ranking_all"+lang, ["keyword", "number"], "w")

        # -------------------------------------------------------------------

        # ------------------------------column-------------------------------
        column_section = 0
        if(folder == "WebCrawler"):
            column_section = 2
        elif(folder == "Twitter"):
            column_section = 1
        # -------------------------------------------------------------------
        print("*****************************************"+folder+" Start SENTIMENT & NLP*****************************************")
        sort_dict = Counter()
        first = 0
        start = time.time()
        for i in data:
            # (1) cut text by nlp and do sentiment in the same time
            if(first > 0):
                cut1 = self.nlp_main.main_nlp(i[column_section])

                if(folder == "WebCrawler"):
                    self.array_sentiment_web.append(self.sentiment_text(cut1, i[column_section], lang))
                elif(folder == "Twitter"):
                    self.array_sentiment_twi.append(self.sentiment_text(cut1, i[column_section], lang))
                self.array_sentiment.append(self.sentiment_text(cut1, i[column_section], lang))
                print(len(self.array_sentiment))
                sort_dict += Counter(cut1)
            first += 1
        print(first,time.time()-start, "*****************************************"+folder+" END SENTIMENT & NLP*****************************************")
        print("ALL: "+str(len(self.array_sentiment))+", Twitter:"+str(len(self.array_sentiment_twi))+", WebCrawler:"+str(len(self.array_sentiment_web)))
        # (2) sort word and write file that can use for show in GUI
        for w in sorted(sort_dict, key=sort_dict.get, reverse=True)[:11]:
            if(w.lower() != keyword):
                write_sort_text.managefile_main( [w, sort_dict[w]] )
                write_sort_text_all.managefile_main( [w, sort_dict[w]] )
        
        #write_sort_text.close()
        #write_sort_text_all.close()
        #os.remove(read_data.path+"\\"+keyword+"_cut"+lang+".csv")
        #os.remove('E:/Work/Documents/term2/main_group/WebCrawler/valentine_cuten.csv')

    def check_keyword(self, keyword):
        file_name = 'list_keywords.csv'
        file_name_Ncsv = 'list_keywords'
        try:
            save = open(file_name, "r")
            df = pandas.read_csv(save) # check that this lists has got search.
            condition = (df["keywords"]==keyword) # check that this lists has got search.
            num = len(df[condition])

            # if num > 0 is True it's mean that keyword has got search already.
            twitter = ManageFile("Twitter", keyword+"_Ncut"+self.lang, ["time","content","places"], "r")
            crawler = ManageFile("WebCrawler", keyword+"_Ncut"+self.lang, ["time","header","content","link"], "r")

            if( num > 0 and (not twitter.do_it or not crawler.do_it) ):
                return True

            twitter.close()
            crawler.close()

            save.close()

            save = ManageFile("", file_name_Ncsv, ["keywords"], "a")
            save.managefile_main([keyword])

        except FileNotFoundError:
            # first time to run.
            temp = open(file_name,"w", newline='')
            temp.write("keywords\n")
            temp.write(f"{keyword}\n")
            temp.close()

        return False

    def ranking(self, keyword, lang):
        # return dataframe ranking word in twitter and crawler
        read_data = ManageFile("GUI_show", keyword+"_ranking_all"+lang, ["keyword", "number"], "r")
        reader_path = read_data.path+"\\"+keyword+"_ranking_all"+lang+".csv"
        df = pandas.read_csv(reader_path)

        return df

    def ranking_twitter(self, keyword, lang):
        # return dataframe ranking word in twitter
        read_data = ManageFile("GUI_show", keyword+"_ranking_twitter"+lang, ["keyword", "number"], "r")
        reader_path = read_data.path+"\\"+keyword+"_ranking_twitter"+lang+".csv"
        df = pandas.read_csv(reader_path)

        return df

    def ranking_webcrawler(self, keyword, lang):
        # return dataframe ranking word in crawler
        read_data = ManageFile("GUI_show", keyword+"_ranking_webcrawler"+lang, ["keyword", "number"], "r")
        reader_path = read_data.path+"\\"+keyword+"_ranking_webcrawler"+lang+".csv"
        df = pandas.read_csv(reader_path)

        return df

    def hit_trends_show(self):
        self.hit_trends()
        # return dataframe hit trends twitter
        writer = ManageFile("Hit_Trends", "Hit_Trends", [], "r")
        reader_path = writer.path+"\\"+"Hit_Trends.csv"
        df = pandas.read_csv(reader_path)

        return df

    def read_time(self, folder, df_in, since, until):
        # return dataframe time
        try:
            condition1 = (df_in[0] >= f"{since} 00:00:00")
            condition2 = (df_in[0] <= f"{until} 23:59:59")

            df_out = df_in[ condition1 & condition2 ]
        except KeyError:
            df_out = df_in

        return df_out

    def ranking_domain(self, keyword, lang):
        # return dataframe domain that exist keyword

        read_data = ManageFile("WebCrawler", keyword+"_cut"+lang, [], "r")
        df = pandas.DataFrame(read_data.managefile_main())

        csv_ = ""
        array = []
        temp = df[3].str.lower()
        if(lang == "en"):
            csv_ = df[temp.str.contains("|".join(self.DOMAIN_en))]
            array = self.DOMAIN_en
        elif(lang == "th"):
            csv_ = df[temp.str.contains("|".join(self.DOMAIN_th))]
            array = self.DOMAIN_th
        elif(lang == "all"):
            csv_ = df[temp.str.contains("|".join(self.DOMAIN))]
            array = self.DOMAIN

        write = ManageFile("Hit_Trends", "top_domain", ["keyword", "number"], "w")

        # sorting domain by number of link has that keyword
        sorted_dict = {}
        for i in array:
            sorted_dict[i] = temp.str.contains(i).sum()
        a = {}
        for i in sorted(sorted_dict, key=sorted_dict.get, reverse=True):
            write.managefile_main( [i, sorted_dict[i]] )
            a[i] = sorted_dict[i]

        df_out = pandas.DataFrame({"keyword":a.keys(),"number":a.values()})

        return df_out

    def sentiment_text(self, dataTh, dataEn, lang):
        # return sentiment type pos,neg and neu
        if(lang == "en"):
            return self.nlp_main.sentiment_eng(dataEn)
        elif(lang == "th"):
            return self.nlp_main.sentiment_thai(dataTh)
        elif(lang == "all"):
            temp = self.nlp_main.detection_lang(dataEn)
            if(temp == "en"):
                return self.nlp_main.sentiment_eng(dataEn)
            elif(temp == "th"):
                return self.nlp_main.sentiment_thai(dataTh)

    def sentiment_show(self):
        # return dataframe sentiment twitter and crawler for show on GUI
        out = Counter(self.array_sentiment)
        df_out = pandas.DataFrame({"sentiment":out.keys(),"number":out.values()})

        return df_out

    def sentiment_show_twi(self):
        # return dataframe sentiment twitter for show on GUI
        out = Counter(self.array_sentiment_twi)
        df_out = pandas.DataFrame({"sentiment":out.keys(),"number":out.values()})

        return df_out

    def sentiment_show_web(self):
        # return dataframe sentiment crawler for show on GUI
        out = Counter(self.array_sentiment_web)
        df_out = pandas.DataFrame({"sentiment":out.keys(),"number":out.values()})

        return df_out

    def stock(self, stock, start, end):
        # return dataframe date and adj close price
        array_x = []
        array_y = []
        
        path = ManageFile("GUI_show").path
        try:
            # write data from yahoo
            ptt = pdr.get_data_yahoo(stock, start=start, end=end)
            writer = open(path+"\\"+"stock.csv","w",newline="")
            writer.write(ptt.to_csv())
            writer.close()
        except:
            print("Error:", sys.exc_info()[0])
            print("Description:", sys.exc_info()[1])

        # read data from file
        df = pandas.read_csv(path+"\\"+"stock.csv")

        return (df["Date"], df["Adj Close"])

    def geometry_map(self, keyword, lang):
        # ------------------------------------Read file------------------------------------
        read = ManageFile("Twitter", keyword+"_cut"+lang, ["time","content","places"], "r")
        read_2 = ManageFile("GUI_show", "location_lati_long", ["places","lati","long"], "r")
        read_3 = ManageFile("GUI_show", "non_exist_lati_long", ["places","lati","long"], "r")
        # ---------------------------------------------------------------------------------

        # ------------------------------------write file------------------------------------
        write_exist = ManageFile("GUI_show", "location_lati_long", ["places","lati","long"], "a")
        write_non_exist = ManageFile("GUI_show", "non_exist_lati_long", ["places","lati","long"], "a")
        write_data_show = ManageFile("GUI_show", "map_lati_long", ["places","lati","long"], "w")
        # ---------------------------------------------------------------------------------

        location = "" # variable that use for checking that location is exist in database location
        lati = ""
        longi = ""

        # temp array variable that use for checking that location is exist in array location
        # use temp array becouse file sometime isn't wrote finished yet
        # data is location name that exist & non_exist is location name that nonexistent
        non_exist = []
        data = []

        # data form database
        data_exist = []
        data_non_exist = []



        count = 0 # Counter number of address that new and old


        # data_exist is location name that geopy can search
        first = 0
        for i in read_2.managefile_main():
            i[0] = self.nlp_main.clear_name_places(i[0]).lower()
            if(first > 0):
                data_exist.append(i)
            first += 1
        first = 0
        # data_exist is location name that geopy can't search
        for i in read_3.managefile_main():
            i[0] = self.nlp_main.clear_name_places(i[0]).lower()
            if(first > 0):
                data_non_exist.append(i)
            first += 1

        # read data form twitter database for find latitude & longitude by geopy
        first = 0
        for i in read.managefile_main():
            i[2] = self.nlp_main.clear_name_places(i[2]).lower()
            if(first > 0):
                if(i[2] == ""):
                    first += 1
                    continue
                try:
                    for j in data_exist: # is it exist in DataBase (file)?
                        if(i[2] == j[0]):
                            location = "exist1"
                            lati = j[1]
                            longi = j[2]
                            write_data_show.managefile_main([i[2], str(lati), str(longi)])
                            data.append([i[2], str(lati), str(longi)])
                            print("exist1")

                    if(location != "exist1"): # is it exist in DataBase (temp array)?
                        for k in data:
                                if(i[2] == k[0]):
                                    location = "exist2"
                                    lati = k[1]
                                    longi = k[2]
                                    print("exist2")
                        if(location == "exist2"):
                            write_data_show.managefile_main([i[2], str(lati), str(longi)])
                            data.append([i[2], str(lati), str(longi)])

                    if( location != "exist1" and location != "exist2"): # it's non_exist in DataBase.

                        for p in data_non_exist: # is it can use Geopy without error by data in file?
                            if(i[2] == p[0]):
                                location = "non_exist"
                                print("non_exist")

                        if(i[2] in non_exist):
                            first += 1
                            continue

                        if( location != "non_exist" ): # is it a new address?
                            location2 = self.geolocator.geocode(i[2])
                            lati = location2.latitude
                            longi = location2.longitude
                            print("Geopy")
                            write_data_show.managefile_main([i[2], str(lati), str(longi)])
                            write_exist.managefile_main([i[2], str(lati), str(longi)])
                            data.append([i[2], str(lati), str(longi)])
                            count += 1

                    location = ""
                except AttributeError:
                    write_non_exist.managefile_main([i[2], str(lati), str(longi)])
                    non_exist.append(i[2])
                except geopy.exc.GeocoderUnavailable:
                    write_non_exist.managefile_main([i[2], str(lati), str(longi)])
                    non_exist.append(i[2])
                except geopy.exc.GeocoderServiceError:
                    pass
            first += 1

        print(len(data), count) # counting location & counting using geopy

        # ----------------return dataframe location by latitude & longitude & name places----------------
        dict_ = {}
        places_array = []
        lati_array = []
        long_array = []

        for i in data:
            places_array.append(i[0])
            lati_array.append(i[1])
            long_array.append(i[2])

            dict_["places"] = places_array
            dict_["lati"] =  lati_array
            dict_["long"] = long_array

        if(data == []):
            dict_ = { "places":[], "lati":[], "long":[] }

        df = pandas.DataFrame(dict_)
        # ------------------------------------------------------------------------------------------------
        return df

if __name__ == "__main__":
    import time
    clock = time.time()
    obj = main()
    print( str(int(time.time())-int(clock)) + " sec" )
    obj.run_webcrawler("en", "covid", "2021-03-01", "2021-03-31")
    print( str(int(time.time())-int(clock)) + " sec" )