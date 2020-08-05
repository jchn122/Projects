
Our Chinese News Corpus was built to analyze Chinese news articles from The New York Times. 

The whole corpus includes Chinese bussiness news articles from May 2018 to March 2020. Articles from Jan 2020 to Feb 2020 are annotated.


To get started,

- Please git clone and navigate to this repo.
- On the command line navigate to the directory: `cd interface`
- Run python on the command line followed by the backend.py file. `python backend.py`
- On your internet explorer (eg Chrome or Safari) open local host to port 9998 `localhost:9998`
- Once this is loaded, the interface would be loaded 🥳


The link below the header could be used to download the corpus.

Please note, since our corpus is in Simplified Chinese, the keyword search also has to be in Simplified Chinese. Some example words you can search for include ((病毒, virus), (经济, economic), (疫情, epidemic))
This search can be done on either all the articles (both annotated and non-annotated) or just the annotated ones with the dropdown in the interface.

Also, the buttons (Positive, Negative, Neutral) would take you directly to the annotated articles respectively.

There are summary statistics on the interface that shows some information about our corpus (i.e. the word counts, the number of paragraphs, the polarity distribution).

Finally, when you navigate to any given annotated article, each paragraph has been coloured to represent the polarities and a graph that shows how the polarities change within an article. 

What the interface should look like:
![Interface Example](https://github.com/jchn122/Projects/blob/master/Chinese_News_Corpus/interface_example.png)
