#!/usr/local/bin/python

import sys
import numpy
from pandas import read_csv
import matplotlib.pyplot as plt

def main(argv):
    file_ngram = argv[0]
    file_happy = argv[1]
    year_start = 1900
    year_end   = 2000
    
    print 'File containing ngram data: ', file_ngram
    print 'File containing information on happiness value of each word: ', file_happy
    print 'Data will be generated for year between %d and %d' % (year_start, year_end)

    # Read in the data in the file and store it in a dataframe
    df_ngram = read_csv(file_ngram)
    df_happy = read_csv(file_happy)
    
    # Change each word in the ngram data to be lower case and
    #    exclude all unwanted suffixes
    for index, row in df_ngram.iterrows():
        df_ngram.ix[index,'word'] = row['word'].split("_")[0].lower()
        
    years  = range(year_start, year_end+1)  # Index of the year
    scores = [0.0]*len(years)                 # Store the final happiness score for each year
    total_counts = [0]*len(years)           # Store the number of words used in a particular year
    
    # For each year find the total number of words used
    for yy in years:
        total_counts[years.index(yy)] = numpy.sum(df_ngram[df_ngram['year'].isin([yy])]['count'])
    
    # Store the average happiness score
    h_avg   = numpy.mean(df_happy['happiness_average'])
    
    for index, row in df_happy.iterrows():
        h_word  = row['word']
        h_level = row['happiness_average']
    
        # Sanity check, print to terminal out current position
        print "Current word: %s (%d of %d) ->  %.3f" % (h_word, index+1, df_happy.shape[0], h_level)
    
        # Find the indecies of the rows of the word of interest
        word_info = df_ngram[df_ngram['word'].isin([h_word])]
        
        for yy in years:
            count = numpy.sum(word_info[word_info['year'].isin([yy])]['count'])
            scores[years.index(yy)] = scores[years.index(yy)] + (h_level-h_avg)*count/total_counts[years.index(yy)]
            
    # Smooth the scores
    temp = scores
    for ii in range(1,len(years)-1):
        temp[ii] = sum(scores[ii-1:ii+2])/3
    scores = temp
    
    print scores
    
    plt.plot(years,scores,'r-')
    plt.ylabel('score')
    plt.xlabel('year')
    plt.show()
 
if __name__ == "__main__":
    main(sys.argv[1:])
