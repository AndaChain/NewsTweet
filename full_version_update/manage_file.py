import csv
import os
from datetime import datetime
import pandas
import sys

class ManageFile:
    def __init__(self, fold_name="", file_name="", column_data=[], mode="a", depend=[]):
        """
            fold_name is folder_name.

            file_name is file name there is .csv at last.
            
            column_data is list that follow by data if it's same index it's mean that data contant in that column.
            
            mode is file mode there is "a", "r". (We don't use "w" because it's can replace older data.)        

            depend is list of the column that hasn't to same during writing files
        """
        csv.field_size_limit(256<<20)
        self.fold_name = fold_name
        self.file_name = file_name
        self.column_data = column_data
        self.mode = mode
        self.depend = depend

        # Current Directory path
        current_dir = os.getcwd()

        # Path 
        self.path = os.path.join(current_dir, self.fold_name)
        
        try:
            os.mkdir(self.path)
        except FileExistsError:
            pass
            #print("FileExists")

        self.reader = None
        self.writer = None
        self.do_it = False
        self.array = []

        if( file_name != "" ):
            if( mode == "r" ):
                try:
                    self.file_ = open(f"{self.path}\{self.file_name}.csv", mode='r', encoding="utf-8")
                    self.reader = csv.reader((line.replace('\0','') for line in self.file_), delimiter=",")
                except FileNotFoundError:
                    self.do_it = True
                    # create file
                    self.file = open(f"{self.path}\{self.file_name}.csv", mode='a', newline='')
                    temp_write = csv.DictWriter(self.file, fieldnames=self.column_data)
                    temp_write.writeheader()

                    # give value reader file
                    self.file_ = open(f"{self.path}\{self.file_name}.csv", mode='r', encoding="utf-8")
                    self.reader = csv.reader((line.replace('\0','') for line in self.file_), delimiter=",")
                    self.file.flush()
            elif( mode == "a" ):
                try:
                    self.file_ = open(f"{self.path}\{self.file_name}.csv", mode='r', encoding="utf-8")
                    self.reader = csv.reader((line.replace('\0','') for line in self.file_), delimiter=",")

                    self.file = open(f"{self.path}\{self.file_name}.csv", mode='a', newline='')
                    self.writer = csv.DictWriter(self.file, fieldnames=self.column_data)

                except FileNotFoundError:
                    self.do_it = True
                    self.file = open(f"{self.path}\{self.file_name}.csv", mode='a', newline='')
                    self.writer = csv.DictWriter(self.file, fieldnames=self.column_data)
                    self.writer.writeheader()

                    self.file_ = open(f"{self.path}\{self.file_name}.csv", mode='r', encoding="utf-8")
                    self.reader = csv.reader((line.replace('\0','') for line in self.file_), delimiter=",")
                self.file.flush()
            elif( mode == "w" ):
                try:
                    self.file = open(f"{self.path}\{self.file_name}.csv", mode='w', newline='')
                    self.writer = csv.DictWriter(self.file, fieldnames=self.column_data)
                    self.writer.writeheader()

                    self.file_ = open(f"{self.path}\{self.file_name}.csv", mode='r', encoding="utf-8")
                    self.reader = csv.reader((line.replace('\0','') for line in self.file_), delimiter=",")
                except FileNotFoundError:
                    self.do_it = True
                    self.file = open(f"{self.path}\{self.file_name}.csv", mode='w', newline='')
                    self.writer = csv.DictWriter(self.file, fieldnames=self.column_data)
                    self.writer.writeheader()

                    self.file_ = open(f"{self.path}\{self.file_name}.csv", mode='r', encoding="utf-8")
                    self.reader = csv.reader((line.replace('\0','') for line in self.file_), delimiter=",")
                self.file.flush()
            self.file_.flush()

    def managefile_main(self, data=''):
        """
            data is data input that is list and mapping depend on index column. if mode is "a" or "w" no need write data but is "r" need to write it
        """
        #print(data)
        if( self.mode == "a" or self.mode == "w" and type(data) == type(list()) ):
            dict_write = {}
            check = []
            for col in range(len(data)):
                dict_write[self.column_data[col]] = str(data[col])
                check.append(str(data[col]))

            if( check not in self.array ):
                self.array.append(check)
                s = self.checking(check)
                #print(s)
                
                if( s ):
                    self.writer.writerow(dict_write)

                    # fix delay writing file
                    self.file.flush()
                    self.file_.flush()
                    #self.writer = csv.DictWriter(self.file, fieldnames=self.column_data)
                    #self.reader = csv.reader((line.replace('\0','') for line in self.file_), delimiter=",")

                    # temporary file
        elif(self.mode == "r"):
            # mode r will be return reader by csv object class that can forloop to access to data 
            return self.reader

    def checking(self, check):
        try:
            check_df = pandas.read_csv(self.path+"\\"+self.file_name+".csv", engine="c", encoding="ISO-8859-1")
            #print("-............",len(self.depend) > 0,"'''''''''''''''''''")
            if( type(self.depend) == type([]) and len(self.depend) > 0 ):
                for j in self.depend:
                    k = self.column_data.index(j)
                    temp = (check_df[j] == check[k]).any()
                    if(bool(temp) == False):
                        return True
            else:
                for i in range(len(check)):
                    #print(self.check_df[i], check[i])
                    temp = (check_df[self.column_data[i]] == check[i]).any()
                    if(bool(temp) == False):
                        return True
        except pandas.errors.EmptyDataError:
            return True
        return False          

    def find_copy_to(self, keyword, reader, condition=[""],  column=[""], nlp=None):

        """
        that file must be same folder and write file that same column name and colmun count.

        keyword will write by file name of "usefull" infor to show by GUI.

        reader is file name that be a source file.

        condition is list that content word or list would like to search in a reader file

        column is list that follow by reader file if it's same index it's mean that data contant in that column and target is also same column.

        nlp is NLP object from NLP class that input is string and out put is list

        ###### return DataFrame ######

        """

        read = ManageFile(self.fold_name, reader, self.column_data, "r") # ดึงข้อมูลจากไฟล์ที่ต้องการ
        df = pandas.DataFrame(data=read.managefile_main(), columns=self.column_data)
        #print(df)
        keyword = [""]
        csv_str_temp = ""

        for col in range(len(column)):
            if(read.do_it):
                csv_str_temp = df.copy()
                break
            if(col != 0):
                df = csv_str_temp.copy(True)
            if(type(condition[col]) == type(list())):
                keyword = condition[col]
                s = "|".join(keyword)
                try:
                    csv_str_temp = df[df.stack().str.contains(s).any(level=0)]
                except:
                    sys.exit()

            elif(type(condition[col]) == type(str())):
                keyword = [condition[col]]

                temp = df[column[col]].str.lower().apply(nlp.main_nlp) # using NLP by each row of that column
                temp_df = df.copy(True)

                temp_df[column[col]] = temp
                temp_df[column[col]][0] = column[col]
                temp_2 = temp_df.copy(True)

                temp_2['found'] = temp_2[column[col]].fillna('').apply(lambda x: len(set(x) & set(keyword)) >= len(keyword))
                csv_str_temp = df[temp_2["found"]]

        return csv_str_temp # return do_it for checking statu of file is new or old file

    def close(self):
        if(self.mode == "r"):
            self.file_.close() # close file, just that
        else:
            self.file.close()
            self.file_.close() # close file, just that

if(__name__ == "__main__"):
    #from NLP_4test import NLP
    #nlp = NLP()
    obj = ManageFile( "WebCrawler/Database", "2021-04-18", ["time","header","content","link"], "r", ["link"])
    print(obj.checking(["1","2","3","4"]))
    """keyword = "bts"
    condition_list = ['www.sanook.com', 'thestandard.co', 'www.thairath.co.th', 'www.bangkokbiznews.com', 'thestandard.co']
    obj.find_copy_to(keyword=keyword, reader="DataBase_DBNcut", target=keyword+"_one", column=["header"], condition=[keyword], nlp=nlp)"""
    """for i in range(1000):
        obj.managefile_main([str(10), str(10), str(10), str(10)])"""
    """for i in obj.reader:
        print(i)"""
# ref: https://python-reference.readthedocs.io/en/latest/docs/file/flush.html
# ref: https://www.raspberrypi.org/forums/viewtopic.php?t=274885
# ref: https://medium.com/analytics-vidhya/filter-pandas-dataframe-rows-by-a-list-of-strings-e95c225822fa