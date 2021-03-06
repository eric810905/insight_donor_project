# Introduction
This is my solution for the coding challenge from https://github.com/InsightDataScience/find-political-donors

# Approach
The technical components and the approaches:
1. read file: process the input file line by line
2. data aggregation: use two dictionaries to store the statistical information of the data aggregated by either the zip code or the date
3. write to medianvals_by_zip.txt: write to file when reading each line of the input file
4. write to medianvals_by_date.txt: write to file after finished reading the whole input file
5. calculate median: use a min heap and a max heap to store a set of values and keep the median values at the top of the heaps

# Discussion
Assume the number of transactions is N

Space complexity is O(N) to store the data of each transaction. 

Time complexity is O(NlogN) in total. Reading the transactions takes O(N), and maintaining the heaps structure takes O(logN).

If the range of the amount of the donation is within a small range of integer number, it is possible to use counting sort (not implemented in this solution) to maintain the statisitcal information of the data instead of using heaps. Using counting sort can reach constant time complexity for tracking the median value. This will lead to O(N) time complexity in total.

# Dependencies
All packages used are python built-in packages: sys, collections, heapq, datetime

# Run Instructions
To run the script:

    insight_donor_project~$ ./run_tests.sh

or run the following with the specific file paths:

    insight_donor_project~$ python ./src/donors_analysis.py {path of the input file} {path of the output file aggregated by zipcode} {path of the output file aggregated by date}

To run the tests:

    insight_testsuite~$ ./run_tests.sh
    
# Tests Coverage
test_1: test case provided by Insight. Test the case that a transaction has other_id. Such transaction should be ignored.

test_date_format: test the case that the format of the date is invalid. Such transaction should not be calculated for medianvals_by_date.txt

test_zipcode_format: test the case that the format of the zip code is invalid. Such transaction should not be calculated for medianvals_by_zip.txt

test_invalid_amount: test the case that the amount of the transaction is invalid. Such transaction should be discarded.

test_invalid_cmte_id: test the case that the cmte_id of the transaction is empty. Such transaction should be discarded.
