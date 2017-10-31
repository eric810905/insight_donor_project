import sys
import collections
import heapq
import datetime

"""
author: Po-En Tsai
email: pt369@cornell.edu
"""

"""
This script reads a input txt file and output two txt files. This script should be
executed along with a path of input file and two paths of output files.
"""

"""
The following five methods define the valid values of each feilds from the input file.
The feilds are CMTE_ID, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, and OTHER_ID
"""
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

def other_id_valid(other_id):
    return other_id == ""

def cmte_id_valid(cmte_id):
    return cmte_id != ""

def transaction_amt_valid(amt):
    return amt.isdigit()

class median_container( object ):
    """
    A container to track the median, sum, and number of transactions given a stream 
    of transaction amount (integer). Median is tracked using a min heap and
    a max heap.
    """
    def __init__(self):
        self.__max_heap = []
        self.__min_heap = []
        self.__total_amount = 0
        self.__num_transaction = 0

    def add_donation(self, amount):
        """
        Add a new transaction. Store the amount into the heaps.
        @amount: integer. The amount of transaction.
        """
        self.__total_amount += amount
        self.__num_transaction += 1
        
        # push the amount into the heap
        if not self.__max_heap:
            heapq.heappush(self.__max_heap, (-amount, amount))
        elif amount>self.__max_heap[0]:
            heapq.heappush(self.__min_heap, (amount, amount))
        else:
            heapq.heappush(self.__max_heap, (-amount, amount))

        # maintain the size of the heap
        # either sizes of two heaps are equal or max heap has one more elements 
        # than min heap
        while len(self.__max_heap) + 1 > len(self.__min_heap):
            _, temp = heapq.heappop(self.__max_heap)
            heapq.heappush(self.__min_heap, (temp, temp))
        while len(self.__max_heap) < len(self.__min_heap):
            _, temp = heapq.heappop(self.__min_heap)
            heapq.heappush(self.__max_heap, (-temp, temp))

    def get_median(self):
        """
        return the median. Median is rounded up if the number of transactions is even
        """
        if len(self.__max_heap) == len(self.__min_heap):
            return int(round((self.__max_heap[0][1] + self.__min_heap[0][1]) / 2.0))
        else:
            return self.__max_heap[0][1]

    def get_num_transaction(self):
        """
        retrun the number of transactions
        """
        return self.__num_transaction

    def get_total_amount(self):
        """
        return the total amount of transactions
        """
        return self.__total_amount

class generate_donors( object ):
    """
    The main object to handle the transformation from the input file to the output 
    files.
    """
    def __init__(self, inFilePath, outFilePath1, outFilePath2):
        self.outFile1 = open(outFilePath1, "w")
        self.outFile2 = open(outFilePath2, "w")
        self.inFilePath = inFilePath
        self.zipDict = collections.defaultdict(dict)
        self.dateDict = collections.defaultdict(dict)

    def __del__(self):
        self.outFile1.close()
        self.outFile2.close()

    def add_donation_zip(self, rec_id, zipcode, amount):
        """
        add a donation and aggregate it by rec_id and zipcode.
        """
        if zipcode not in self.zipDict[rec_id]:
            self.zipDict[rec_id][zipcode] = median_container()
        self.zipDict[rec_id][zipcode].add_donation(amount)

    def output_donation_zip(self, rec_id, zipcode):
        """
        write a line of statistics aggregated by rec_id and zipcode to the output file.
        """
        data = self.zipDict[rec_id][zipcode]
        fields = [ rec_id, zipcode, str(data.get_median()), 
            str(data.get_num_transaction()), str(data.get_total_amount())]
        self.outFile1.write( "|".join(fields) + "\n" )

    def add_donation_date(self, rec_id, date, amount):
        """
        add a donation and aggregate it by rec_id and date
        """
        if date not in self.dateDict[rec_id]:
            self.dateDict[rec_id][date] = median_container()
        self.dateDict[rec_id][date].add_donation(amount)

    def output_donation_date(self):
        """
        write a line of statistics aggregated by rec_id and date to the output file.
        """
        for rec_id in sorted(self.dateDict):
            for date in sorted(self.dateDict[rec_id]):
                data = self.dateDict[rec_id][date]
                fields = [ rec_id, date, str(data.get_median()), str(data.get_num_transaction()), str(data.get_total_amount())]
                self.outFile2.write( "|".join(fields) + "\n" )

    def parse_line(self, line):
        """
        parse a line of input and return the feilds in the string format. The feilds 
        includes CMTE_ID, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, and OTHER_ID.
        """
        fields = line.split("|")
        return fields[0], fields[10][:5], fields[13], fields[14], fields[15]

    def start(self):
        """
        The method to start the operation of this object. Read input file and write 
        output files.
        """
        with open(self.inFilePath) as f:
            for line in f:
                CMTE_ID, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID = \
                    self.parse_line(line)
                if other_id_valid(OTHER_ID) and cmte_id_valid(CMTE_ID) and \
                    transaction_amt_valid(TRANSACTION_AMT):
                    if zipcode_valid(ZIP_CODE):
                        # aggregate by zipcode
                        self.add_donation_zip(CMTE_ID, ZIP_CODE, int(TRANSACTION_AMT))
                        self.output_donation_zip(CMTE_ID, ZIP_CODE)

                    if date_valid(TRANSACTION_DT):
                        # aggregate by date
                        self.add_donation_date(CMTE_ID, TRANSACTION_DT, 
                            int(TRANSACTION_AMT))
            self.output_donation_date()

if __name__ == "__main__":
    generator = generate_donors( sys.argv[1], sys.argv[2], sys.argv[3] )
    generator.start()
