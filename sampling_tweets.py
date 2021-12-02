# Modified version of the notebook of the same name allowing program to be easily called from other programs

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections

def getTweetAssignments(n_tweets, n_participants, tweets_per_person):
    tweets = {i:[] for i in range(n_tweets)} # We can replace this with a list of the tweets themselves (or tweet IDs)
    participants = {i:[] for i in range(n_participants)}

    tweets_complete = {}
    participants_complete = {}

    sample_quota_each = int(n_participants*tweets_per_person/n_tweets) # or replace with an appropriate number if desired
    # i.e. maybe we want each tweet seen a minimum of 5 times.

    for _ in range(n_tweets):
        random_tweet = np.random.choice(list(tweets.keys())) # start with a random tweet
        
        for __ in range(sample_quota_each): # We need to assign this tweet to the quota number of people
            random_participant = np.random.choice(list(participants.keys()))

            while random_tweet in participants.get(random_participant, []):   # If this randomly selected person has already been assigned this tweet...
                random_participant = np.random.choice(list(participants.keys())) # Find a new person
            participants.setdefault(random_participant, []).append(random_tweet)

            if len(participants.get(random_participant, [])) >= tweets_per_person: # Remove people from the sample list if they have the max number we want anyone to answer
                participants_complete[random_participant] = participants[random_participant]
                del participants[random_participant]
                
            tweets.setdefault(random_tweet, []).append(random_participant)    
        
        tweets_complete[random_tweet] = tweets[random_tweet]
        del tweets[random_tweet]

    for person in participants:
        n_missing = tweets_per_person - len(participants.get(person, []))
        added_tweets = list(np.random.choice(list(tweets_complete.keys()), n_missing, replace=False))
        participants.setdefault(person, []).extend(added_tweets)
        for each in added_tweets:
            tweets_complete.setdefault(each, []).append(person)
        participants_complete[person] = participants[person]

    output_df = pd.DataFrame(sorted(participants_complete.items()), columns = ("Participant_ID", "tweets_assigned"))
    return(output_df)

def getUniparkInputs(output_df):
    # Calling this function with the dataframe created by getTweetAssignments() will produce two text files:
    # groupings.txt: contains a formatted list of the tweets to be assigned to each user
    # quotas.txt: contains a formatted list of quotas necessary for our Unipark setup
    with open("groupings.txt", "a+") as groupings_txt, open("quotas.txt", "a+") as quota_txt:
        for grouping in range(len(output_df)):
            groupings_txt.write(str(grouping) + ';,' + ','.join([str(tweet) for tweet in output_df.tweets_assigned[grouping]]) + ',\n')
            quota_txt.write('q_' + str(grouping) + "_;1;language = '1'\n")
