import sys
import collections
import heapq
import datetime

inFile = sys.argv[1]
outFilePath1 = sys.argv[2]
outFilePath2 = sys.argv[3]
outFile1 = None
outFile2 = None

def parse_line(line):
    """
    parse a line of input and return CMTE_ID, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID
    """
    fields = line.split("|")
    return fields[0], fields[10][:5], fields[13], fields[14], fields[15]

class median_container( object ):
    def __init__(self):
        self.__max_heap = []
        self.__min_heap = []
        self.__total_amount = 0
        self.__num_transaction = 0

    def add_donation(self, amount):
        self.__total_amount += amount
        self.__num_transaction += 1
        
        if not self.__max_heap:
            heapq.heappush(self.__max_heap, (-amount, amount))
        elif amount>self.__max_heap[0]:
            heapq.heappush(self.__min_heap, (amount, amount))
        else:
            heapq.heappush(self.__max_heap, (-amount, amount))
        while len(self.__max_heap) + 1 > len(self.__min_heap):
            _, temp = heapq.heappop(self.__max_heap)
            heapq.heappush(self.__min_heap, (temp, temp))
        while len(self.__max_heap) < len(self.__min_heap):
            _, temp = heapq.heappop(self.__min_heap)
            heapq.heappush(self.__max_heap, (-temp, temp))

    def get_median(self):
        if len(self.__max_heap) == len(self.__min_heap):
            return int(round((self.__max_heap[0][1] + self.__min_heap[0][1]) / 2.0))
        else:
            return self.__max_heap[0][1]

    def get_num_transaction(self):
        return self.__num_transaction

    def get_total_amount(self):
        return self.__total_amount

class generate_donors( object ):
    def __init__(self):
        self.zipDict
zipDict = collections.defaultdict(dict)
def add_donation_zip(rec_id, zipcode, amount):
    if zipcode not in zipDict[rec_id]:
        zipDict[rec_id][zipcode] = median_container()
    zipDict[rec_id][zipcode].add_donation(amount)

def output_donation_zip(rec_id, zipcode):
    data = zipDict[rec_id][zipcode]
    fields = [ rec_id, zipcode, str(data.get_median()), str(data.get_num_transaction()), str(data.get_total_amount())]
    outFile1.write( "|".join(fields) + "\n" )
    #print( "|".join(fields) + "\n" )

dateDict = collections.defaultdict(dict)
def add_donation_date(rec_id, date, amount):
    if date not in dateDict[rec_id]:
        dateDict[rec_id][date] = median_container()
    dateDict[rec_id][date].add_donation(amount)

def output_donation_date():
    for rec_id in sorted(dateDict):
        for date in sorted(dateDict[rec_id]):
            data = dateDict[rec_id][date]
            fields = [ rec_id, date, str(data.get_median()), str(data.get_num_transaction()), str(data.get_total_amount())]
            outFile2.write( "|".join(fields) + "\n" )
            
def zipcode_valid(zipcode):
    if not len(zipcode) == 5 or not zipcode.isdigit():
        return False
    return True

def date_valid(date):
    try:
        datetime.datetime.strptime(date, "%m%d%Y")
    except ValueError:
        return False
    return True

def get_donors():
    with open(inFile) as f:
        for line in f:
            CMTE_ID, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID = parse_line(line)
            #print(CMTE_ID, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID)
            if OTHER_ID == "" and CMTE_ID != "" and TRANSACTION_AMT != "":
                if zipcode_valid(ZIP_CODE):
                    # write to medianvals_by_zip.txt
                    add_donation_zip(CMTE_ID, ZIP_CODE, int(TRANSACTION_AMT))
                    #print("here", CMTE_ID, ZIP_CODE)
                    output_donation_zip(CMTE_ID, ZIP_CODE)

                if date_valid(TRANSACTION_DT):
                    # aggregate by date
                    add_donation_date(CMTE_ID, TRANSACTION_DT, int(TRANSACTION_AMT))
        # write to medianvals_by_date
        output_donation_date()

if __name__ == "__main__":
    outFile1 = open(outFilePath1, "w")
    outFile2 = open(outFilePath2, "w")
    generate_donors( sys.argv[1], sys.argv[2], sys.argv[3] )
    get_donors()
    outFile1.close()
    outFile2.close()
