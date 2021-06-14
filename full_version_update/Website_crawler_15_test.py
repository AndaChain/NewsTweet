import requests
from bs4 import BeautifulSoup, SoupStrainer

import time
from datetime import datetime
from datetime import timedelta
from win10toast import ToastNotifier

import pandas
import csv
import re
import sys
import traceback
from collections import Counter

import concurrent.futures
import threading

from manage_file import ManageFile
from NLP_4test import NLP

# 3132.5305066108704 seconds to download 40 stories.
# time: 2820.2496247291565 seconds, length: 718 links.4714
# time: 1492.7347793579102 seconds, length: 350 link

class websites_crawler:
    def __init__(self, nlp):
        self.URL_en = []
        self.URL_th = []

        read_url_en = open("website_crawler_en.txt", "r")
        read_url_th = open("website_crawler_th.txt", "r")

        for lib in read_url_en:
            self.URL_en.append(lib.split("\n")[0])

        for lib in read_url_th:
            self.URL_th.append(lib.split("\n")[0])

        self.DOMAIN_en = []
        self.DOMAIN_th = []
        for ie in self.URL_en:
            self.DOMAIN_en.append(ie.split("/")[2])
        for it in self.URL_th:
            self.DOMAIN_th.append(it.split("/")[2])

        # value ของ set_pattern คือ ระดับความสำคัญ ยิ่งมากคือสำคัญดังนั้นจะลำดับตามนั้น
        set_pattern = {("meta","property","og:type"):3, ("meta","name","og:type"):2, ("meta","property","og:url"):1, ("meta","name","og:url"):0} 
        self.pattern_list = sorted(set_pattern, key=set_pattern.get, reverse=True)

        self.DOMAIN = self.DOMAIN_en + self.DOMAIN_th
        self.nlp_web = nlp

        self.MAX_THREADS = len(self.DOMAIN) #จะ thread ทีละชั้น
        self.thread_local = threading.local()
        self.output = []
        self.output2 = []
        self.output3 = []
        self.output4 =[]

    def download_url(self, url, domain, count):
        links = Counter()
        try:
            # checking whice thread is running
            print(str(self.DOMAIN.index(domain))+"_A"+domain+"\n")
            self.check_thread.write(str(self.DOMAIN.index(domain))+"_A"+domain+"\n")
            self.check_thread.flush()
            tage_a_all = []
            html_code = []
            
            # requests html code from server
            if(type(url) == type(str())):
                session = self.get_session()
                resp = session.get(url)
                html_code = resp.content
                html_page = BeautifulSoup(html_code, "html.parser")
                tage_a_all = html_page.find_all("a")
            elif(type(url) == type(bytes())):
                html_code = url
                html_page = BeautifulSoup(html_code, "html.parser")
                tage_a_all = html_page.find_all("a")
            
            # find topic for denied link that same in topic
            topic = self.find_topic(html_code, domain)
            
            # find link in tage "a" all page
            for x in tage_a_all:
                try:
                    if(x["href"]):
                        temp = self.link_format(x["href"], domain)
                        # same domain can do
                        same = temp.split("/")[2]
                        if( domain == same ):
                            # first round is find all link that found
                            if(count == self.count):
                                links += Counter([temp])
                            else:
                                # since secound round is find denied a link that in output and topic
                                if( temp not in topic and temp not in self.output):
                                    links += Counter([temp])
                except IndexError:
                    pass
                except KeyError:
                    pass
            perfect = []
            for i in links.keys():
                perfect.append(i)
                self.check_data_a.write( str(i)+"\n" )
                self.check_data_a.flush()
            self.output += perfect
            self.output4 += perfect
            print( "length:",len(perfect)," output:",len(self.output)," topic:",len(topic), " round:",str(count)+"\n")
        except:
            error = traceback.format_exc()
            print(error)
            self.check_bug.write( str(error)+"\n"+" "+str(url) )
            self.check_bug.flush()
            pass
        return 1

    def analytics_url(self, link, topic, domain):
        t__0 = time.time()
        try: 
            # checking whice thread is running
            print(str(self.DOMAIN.index(domain))+"_B")
            self.check_thread.write(str(self.DOMAIN.index(domain))+"_B"+domain+"\n")
            self.check_thread.flush()

            # requests html code from server
            session = self.get_session()
            res = session.get(link, timeout=20)
            html_code = res.content
            soup = BeautifulSoup(html_code, "html.parser")
            topic = self.find_topic(html_code, domain)

            # if a link is one of the link in topic, it's mean time to denied!!
            if(link in topic):
                tage_a_all = soup.find_all("a")
                self.output2.append(link)
                self.output3.append(html_code)
                print(time.time()-t__0)
                self.check_done.write( str(link)+"\n" )
                self.check_done.flush()
                return "No" 

            # tage meta pattern
            type_ = None
            for pattern in self.pattern_list:
                type_ = soup.find(pattern[0], {pattern[1]:pattern[2]})
                if(type_ != None):
                    break
            
            try:
                # tage meta pattern Rarely!! case
                if(type_["content"] == ""):
                    # og:type is empty string
                    print(time.time()-t__0)
                    self.check_done.write( str(link)+"\n" )
                    self.check_done.flush()
                    return "website"
                elif(type_["content"] == link):
                    # has same link in og:url meta tags
                    self.find_message(html_code, link)
                    #self.output_write[0].append(link)
                    #self.output_write[1].append(html_code)
                    self.output2.append(link)
                    self.output3.append(html_code)
                    print(time.time()-t__0)
                    self.check_done.write( str(link)+"\n" )
                    self.check_done.flush()
                    return "article"
            except TypeError:
                pass
            except:
                print("UnkonwError", link)
                self.check_bug.write( str(traceback.format_exc())+"\n"+" "+str(link) )
                self.check_bug.flush()
            
            # if meta tage have "article" that mean can write down on files
            if(type_):
                x = type_["content"]
                if(x == "article"):
                    self.find_message(html_code, link)
                    #self.output_write[0].append(link)
                    #self.output_write[1].append(html_code)
                    self.output2.append(link)
                    self.output3.append(html_code)
                print(time.time()-t__0)
                self.check_done.write( str(link)+"\n" )
                self.check_done.flush()
                return x
            else:
                print(time.time()-t__0)
                self.check_done.write( str(link)+"\n" )
                self.check_done.flush()
                return "No meta type"

        # --------------------- it's not a real link ---------------------
        except requests.exceptions.MissingSchema:
            print("MissingSchema",link)
            return "No"
        except requests.exceptions.InvalidSchema:
            print("InvalidSchema",link)
            return "No"
        except requests.exceptions.SSLError:
            print("SSLError",link)
            return "No"
        except requests.exceptions.ConnectionError:
            print("ConnectionError",link)
            return "No"
        except requests.exceptions.ReadTimeout:
            print("ReadTimeout",link)
            return "No"
        except requests.exceptions.TooManyRedirects:
            print("TooManyRedirects",link)
            return "No"
        except requests.exceptions.ChunkedEncodingError:
            print("ChunkedEncodingError", link)
            return "No"
        except:
            print("UnkonwError", link)
            self.check_bug.write( str(traceback.format_exc())+"\n"+" "+str(link) )
            self.check_bug.flush()
            return "No"
        # ----------------------------------------------------------------

    def find_message(self, html_code, url):
        t_0 = time.time()
        soup = BeautifulSoup(html_code, 'html.parser', parse_only=SoupStrainer("div"))
        tit = BeautifulSoup(html_code, 'html.parser')

        title = tit.find("meta",  property="og:title") # find title
        title = title["content"] if title else "" # find title

        message = soup.find_all(name="p") # find message 

        temp_message = ""
        output = []

        for i in message:
            temp_message += i.text+"\n"

        time_ = self.find_time(html_code)
        try:
            data = [ time_[0]+" "+time_[1], str(title), str(temp_message), str(url) ]
            # =========================== This point is writing ===========================
            column = ['time','header', 'content', 'link']
            self.write = ManageFile("WebCrawler/Database", time_[0], column, "a", ["link"])
            # =============================================================================
            self.write.managefile_main(  data  ) # write file
            #print("Write file")
            self.check_data.write( str(url)+" "+str(time.time()-t_0)+"\n" )
            self.check_data.flush()
        except TypeError:
            str(datetime.now()).split(" ")[0]

    def find_time(self, html_code):
        # find time from website
        try:
            soup = BeautifulSoup(html_code, 'html.parser', parse_only=SoupStrainer("script"))
            date = soup.find_all(name="script")

            reg = re.compile(r'(?P<date>202\d-\d\d-\d\d)(?P<time>T\d\d:\d\d:\d\d| \d\d:\d\d)')
            ou = reg.search(str(date))
            date_output = ou.group("date")
            time_output = ou.group("time")[1:]

            return [str(date_output), str(time_output)]
        except AttributeError:
            # Ex:: Jan 27 2021 06:31:00:000PM+07:00 ==> 2021-01-27 18:31:00
            try:
                reg = re.compile(r'(?P<date>\w\w\w \d\d \d\d\d\d)(?P<time> \d\d:\d\d:\d\d:000AM| \d\d:\d\d:\d\d:000PM)')
                ou = reg.search(str(date))
                date_output = ou.group("date")
                time_output = ou.group("time")[1:]

                temp1=datetime.strptime(date_output,"%b %d %Y")
                temp2=datetime.strptime(time_output,"%I:%M:%S:000%p")

                return [str(temp1).split(" ")[0], str(temp2).split(" ")[1]]
            except AttributeError:
                # it isn't Jan 27 2021 06:31:00:000PM+07:00 
                date_now = str(datetime.now()).split(" ")
                reg = re.compile(r'(?P<date>202\d-\d\d-\d\d)(?P<time> \d\d:\d\d:\d\d)')
                ou = reg.search(str(datetime.now()))
                date_output = ou.group("date")
                time_output = ou.group("time")[1:]
                
                return [str(date_output), str(time_output)]

    def find_topic(self, html_code, domain):
        try:
            # find link in tag nav or header or div
            #res = requests.get(url, timeout=20)
            #html_page = res.content
            set_html_tag = ["nav", "header", "div"] # เอาไปใส่ text ทีหลัง
            data = []
            count = 0
            # -------------------------------------- header --------------------------------------
            while( data == [] and (count != len(set_html_tag)) ):
                # if data is empty list it's still change html_tag to find
                soup = BeautifulSoup(html_code, 'html.parser', parse_only=SoupStrainer(set_html_tag[count]))
                data = soup.find_all(name="ul")
                count += 1
            storage = []
            for i in data:
                temp = i.find_all("li")
                for j in temp:
                    try:
                        g = j.find("a")["href"]
                        g = self.link_format(g, domain)
                        if(g == ""):
                            continue
                        storage.append(g)
                    except TypeError:
                        #print(g)
                        pass
                    except KeyError:
                        #print(g)
                        pass
            # -------------------------------------------------------------------------------------

            # -------------------------------------- tail --------------------------------------
            soup1 = BeautifulSoup(html_code, 'html.parser', parse_only=SoupStrainer("footer"))
            sub_footer = []
            for i in soup1.find_all("a"):
                if(i.get("href") == None):
                    continue
                footer = self.link_format(i.get("href"), domain)
                if(footer == ""):
                    continue
                sub_footer.append(footer)

            return storage+["*"*10]+sub_footer
        except requests.exceptions.ReadTimeout:
            return []
        except requests.exceptions.TooManyRedirects:
            return []
            # ---------------------------------------------------------------------------------

    def find_domain(self, url):
        temp = []
        for i in url:
            temp.append(i.split("/")[2])
        return temp

    def link_format(self, str_input, domain):

        # if it's empty string str_out set to empty string it's mean it's not link
        if(str_input == ""):
            str_out = ""
        else:
            str_out = re.search(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", str_input)

            # if str_out is None go to forming link to correct full link
            if(str_out == None):
                if( str_input[0:2] == "//" and len(str_input) > 3 ):
                    str_out = "https:"+str_input
                elif(str_input[0] == "/" and len(str_input) > 3):
                    str_out = "https://"+domain+str_input
                elif(str_input[0:2] == "./" and len(str_input) > 3):
                    str_out = "https://"+domain+"/"+str_input[2:]
                    #print(str_out)
                else:
                    str_out = ""
            else:
                # if str_out isn't None it's mean str_out is a link can be search
                str_out = str_out.group()
                # but some values of str_out isn't exist https:// or http://
                if("https://" in str_out or "http://" in str_out):
                    pass
                else:
                    str_out = "https://"+str_out
            
        return str(str_out)

    def concurrent_futures(self, func, arg1, arg2, arg3):
        threads = len(arg1)+1
        r = None
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(func, arg1, arg2, arg3)

    def get_session(self):
        if not hasattr(self.thread_local, "session"):
            self.thread_local.session = requests.Session()
        return self.thread_local.session

    def searching(self, keyword, lang, since, until):
        print("Start Crawler")
        column = ['time','header', 'content', 'link']
        check = ManageFile(fold_name="WebCrawler", file_name="", column_data=column, mode="a") # file_name="" it's mean do not create file before.
        temp_until = datetime.strptime(until, "%Y-%m-%d")
        temp_since = datetime.strptime(since, "%Y-%m-%d")

        dif = temp_until - temp_since

        if(dif == timedelta(days=0)):
            dif = "0 day"
        print(dif)
        day = int(str(dif).split(" ")[0]) + 1
        array = []

        for i in range(day):
            date = str(temp_since+timedelta(days=i)).split(" ")[0]
            print(date)
            df = None
            if(lang == "en"):
                df = check.find_copy_to(keyword=keyword, reader="Database\\"+date, column=["link", "header"], condition=[self.DOMAIN_en, keyword], nlp=self.nlp_web)
            elif(lang == "th"):
                df = check.find_copy_to(keyword=keyword, reader="Database\\"+date, column=["link", "header"], condition=[self.DOMAIN_th, keyword], nlp=self.nlp_web)
            elif(lang == "all"):
                df = check.find_copy_to(keyword=keyword, reader="Database\\"+date, column=["link", "header"], condition=[self.DOMAIN, keyword], nlp=self.nlp_web)
            array.append(df)
        if(dif == "0 day"):
            array.append(pandas.DataFrame(columns=column))

        result = pandas.concat(array)
        target_file = open(check.path+"\\"+keyword+"_cut"+lang+".csv", "w", newline="")
        target_file.write(result.to_csv(index=False))

    def main_crawler(self, keyword, lang, since, until, update=False):
        if(update):
            self.check_bug = open("check_bug.txt","w",newline="\n")
            self.check_thread = open("check_thread.txt","w",newline="\n")
            self.check_data = open("check_data.txt","w",newline="\n")
            self.check_data_a = open("check_data_a.txt","w",newline="\n")
            self.check_done = open("check_done.txt","w",newline="\n")

            self.check_data.write("Start: "+str(datetime.now())+"\n")
            self.check_data.flush()
            self.URL = self.URL_en + self.URL_th
            self.count = 2
            url = self.URL.copy()
            domain = self.DOMAIN.copy()
            
            all_time0 = time.time()
            
            for count in range(self.count, 0, -1):
                all_t0 = time.time()
                # download_url all page
                t0 = time.time()
                self.concurrent_futures(self.download_url, url, domain, [count]*len(url))
                t1 = time.time()
                print(f"time: {t1-t0} seconds, length: {len(self.output4)} links. 1")

                # go to thread used for analytics_url method
                t0 = time.time()
                domain = self.find_domain(self.output4)
                self.concurrent_futures(self.analytics_url, self.output4, ["s"]*len(self.output4), domain)
                t1 = time.time()
                print(f"time: {t1-t0} seconds, length: {len(self.output4)} links. 3")

                # for new round
                url = self.output3.copy()
                domain = self.find_domain(self.output2)
                self.output2 = []
                self.output3 = []
                self.output4 = []
                #self.output_write = [[],[]]
                
                all_t1 = time.time()
                cou = len(open("check_data.txt").readlines())
                print(f"time: {all_t1-all_t0} seconds, length: {cou-1} links. 4")
            
            all_time1 = time.time()
            cou = len(open("check_data.txt").readlines())
            self.check_data.write( "time: "+str(all_time1-all_time0)+" seconds, length: "+str(cou-1)+" link" )
            self.check_data.flush()
            print(f"time: {all_time1-all_time0} seconds, length: {cou-1} links.")
        else:
            self.searching(keyword, lang, since, until)

if __name__ == "__main__":
    obj = websites_crawler(NLP())
    obj.main_crawler("covid", "all", "2021-01-01", "2021-01-01", True)
    #get_ = requests.get("https://www.reuters.com/investigates/section/climate-change-scientists/")
    #html = get_.content
    #obj.find_message(html,"https://www.reuters.com/investigates/section/climate-change-scientists/")
    #obj.download_url("https://www.reuters.com/", "www.reuters.com", 2)

# ref: https://realpython.com/python-concurrency/