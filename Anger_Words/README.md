
The anger words are keywords and phrases to identify angry tweets with high precision. These anger words are intended as a relative, not absolute, measure of the anger expressed in a sample of tweets. Therefore, they can be used to compare the level of anger between samples (for different keywords, in different locations, or at different times) or to compare against a baseline level of anger for a given population. For example, all tweets in San Diego containing the word "Republicans" on a given day could be compared to tweets containing "Democrats" and/or to tweets collected in San Diego for some neutral keywords such as "a" and "the."

The anger words are: liar(s), lying, lies, hypocrite(s), hypocrisy, hypocritical, asshole(s), bullshit, fuck AND off, “fuck you”, disgrace(s), disgraced, disgraceful, “piece of shit”, “the fuck up”, piss(ed) AND off, STFU, disgusting, disgusted, disgusts, “go fuck yourself”, scum, infuriate(s), infuriating, infuriated.

This folder contains four scripts applying these anger words to Twitter data. Each takes as input an XLSX file or a folder of XLSX files. Each input file must at least have one column containing tweet text with the header TEXT, with each tweet in a separate row.

General-Anger-Check: Counts occurrences of the anger words in a sample of Twitter data as a percentage of the total number of tweets.  Returns one CSV file per input file showing number and percent for each keyword and in total.

Anger-Filter: This code can mark angry tweets while saving all tweets, save all tweets with a column showing which anger words occur in each tweet, or save only angry tweets. Note that because these are high precision but low recall keywords, this is expected to be only a representative subset of total anger, not every tweet containing anger.

Angry-Tweets-vs-Time: Counts angry tweets (tweets containing at least one anger keyword) per day in a sample collected over time. Be aware that the calculated ratio (angry tweets/total tweets) may overestimate relative anger when the total number of tweets drops significantly. In addition to the TEXT column in input files, this code requires a column titled CREATED_AT_LOCAL containing the date and time of each tweet.

Anger-PMI: Calculates PMI, a measure of word association, for angry tweets compared to total tweets in a sample. A high PMI score means that words occur more often in angry tweets than in the overall sample, while a low PMI means that words occur less often in angry tweets than overall.
