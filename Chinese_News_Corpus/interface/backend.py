### Necessary Imports

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import os
from os import curdir, sep

### Functions Goes Here

## Search functionality (Rannie)

def search(query, option):
    '''
    Return a list of filenames related to the query
    '''

    if option == 'yes':
        corpus_dir = "annotated_corpus/"
    else:
        corpus_dir = "corpus/"
    
    results = defaultdict(int)
    query = query.title()
    for filename in os.listdir(corpus_dir):
        if filename.endswith("txt"):
            with open(corpus_dir + filename, 'r', encoding = 'utf-8') as f:
                c = f.read()
                if query in c:
                    results[filename] += c.count(query)

    if len(results) == 0:
        return ["No Results Found!!!"]

    sorted_results = sorted(results, key = results.get, reverse=True)
    return sorted_results

def search_list(query, option):
    '''
    Turn the sorted articles into a list of hyperlinks to the text
    '''
    if option == 'yes':
        corpus_dir = "annotated_corpus/"
    else:
        corpus_dir = "corpus/"
    
    s = "<ul style='list-style-type:disc;'>"
    results = search(query, option)
    for i, r in enumerate(results):

        # limit return links
        if i > 20:
            break
        
        # set excetional case
        if r == "No Results Found!!!":
            s += r
            break

        else:
            local_link = corpus_dir + r[:-4]
            show_title = "Article Title: " + " ".join(r.split("_")[1].split("-"))[:-4]
            to_s = "<li>" + f"<a href='{local_link}'>{show_title}</a>" +"</li>"
            s += to_s

    s += "</ul>"
    return s


## Visualization Functionality (Jon)
def get_polarity_graph(textfile, filename):
    """
    Takes an annotated text file and generates a line graph that shows the sentiment polarity of each paragraph.
    The color of the line changes depending on the text polarity.
    """
    with open(textfile) as f:
            paras = []
            polarities = []
            for line in f:
                line = line.split(" ")
                paras.append(line[0])
                polarities.append(line[-1])
            polarity = polarities[-1].split(':')[1]
            overall = '(Overall: '+ polarity+')'

            paras = [int(x) for x in paras[:-1]]
            polarities = [int(x[:-1]) for x in polarities[:-1]]

            avg = 'Text Polarity: '+str(round(sum(polarities)/len(paras),3))

            if polarity == 'Positive':
                color = 'tab:green'
            elif polarity == 'Neutral':
                color = 'tab:blue'
            else:
                color = 'tab:red'

            plt.figure(figsize=(11,5))
            plt.plot(paras, polarities, color, label = avg)
            plt.xlabel('Paragraph number')
            plt.ylabel('Polarity')
            plt.legend(fontsize=14)
            plt.title("Paragraph Polarity "+overall)
            if len(paras)>50:
                plt.xticks()
            else:
                plt.xticks(paras)
            plt.yticks([-1,0,1])
            
            plt.savefig("./images/"+filename, transparent=True)

## Categorize Functionality (Chidera)

def annotation_category(query):
    '''
    Returns articles from the selected category
    '''
    s = "<ul style='list-style-type:disc;'>"
    if "Pos" in query:
        annotation_dir = "Positive/"

    elif "Neu" in query:
        annotation_dir = "Neutral/"
        
    elif 'Neg' in query:
        annotation_dir = "Negative/"

    for filename in os.listdir(annotation_dir):
            
        local_link = "annotated_corpus/" + filename[:-5]
        show_title = "Article Title: " + " ".join(filename.split("_")[1].split("-"))
        to_s = "<li>" + f"<a href='{local_link}'>{show_title}</a>" +"</li>"
        s += to_s

    return s

### Web Server Goes Here

class MyWebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        query = parse.urlsplit(self.path).query
        query_dict = parse.parse_qs(query)

        # Read all png files
        if self.path.endswith("png"):
            self.send_header("Content-type", "image/jpg")
            self.end_headers()
            with open(curdir+sep+self.path,'rb') as f:
                self.wfile.write(f.read())

        # Read css file
        if "frontend.css" in self.path:
                self.send_header('Content-type','text/css; charset=utf-8') # what service we are sending over
                self.end_headers()
                f = open("frontend.css", encoding = 'utf-8')
                html = f.read()
                f.close()
                self.wfile.write(html.encode('utf-8'))

        # Read frontend file   
        elif "frontend.js" in self.path:
                self.send_header('Content-type','text/javascript; charset=utf-8') # what service we are sending over
                self.end_headers()
                f = open("frontend.js", encoding = 'utf-8')
                html = f.read()
                f.close()
                self.wfile.write(html.encode('utf-8'))

        # Read html file
        elif self.path == "/":
            self.send_header('Content-type','text/html; charset=utf-8') # what service we are sending over
            self.end_headers()

            f = open("frontend.html", encoding = 'utf-8')
            html = f.read()
            f.close()
            self.wfile.write(html.encode('utf-8'))


        # Add Categorization Functionality here
        elif "Pos" in self.path or  "Neu" in self.path or "Neg" in self.path:

            self.send_header('Content-type','text/html; charset=utf-8') # what service we are sending over
            self.end_headers()
            search_returns = annotation_category(query)
            self.wfile.write(b"<html>" + search_returns.encode("utf-8") + b"</html>")
            


        ## Add Search Part here

        # Get all result links
        elif "search_text" in query_dict:
            self.send_header('Content-type','text/html; charset=utf-8') # what service we are sending over
            self.end_headers()
            view_option = query_dict['view'][0]
            search_query = query_dict['search_text'][0]
            search_returns = search_list(search_query, view_option)
            self.wfile.write(b"<html>" + search_returns.encode("utf-8") + b"</html>")

        # Open a new page to display the selected article
        elif "corpus" in self.path:

            # set option for annotated/non-annotated results
            annotated = False

            self.send_header('Content-type','text/html; charset=utf-8') # what service we are sending over
            self.end_headers()

            file_path = "." + self.path + ".txt"
            body_style = '''<body style="background-color: aliceblue;font-family:Arial;">'''
            self.wfile.write(body_style.encode("utf-8"))
            
            # set option for annotated/non-annotated results
            if "annotated_corpus" in self.path:
                annotated = True

            color_scheme = "<h4>Annotation Color Scheme: </h4><p style=color:green>Positive</p><p style=color:blue>Neutral</p><p style=color:red>Negative</p>"


            if annotated:
                
                self.wfile.write(color_scheme.encode("utf-8"))

            # get metadata
            metadata = self.path.split("/")[-1]
            time = metadata.split('_')[0]
            title = metadata.split("_")[1]

            time = "-".join((time[:4], time[4:6], time[6:]))
            title = " ".join([s.title() for s in title.split("-")])

            t_t = title + " (" + time + ")"

            self.wfile.write(b"<h4>Article: </h4>")

            self.wfile.write(b"<center>" + t_t.encode('utf-8') + b"</center>")

            # display the article
            with open(file_path, "r") as f:
                for p in f:
                    
                    p = p.strip("\n")

                    if annotated:

                        if p[0].isdigit():
                            polarity = p[-2:]

                            if polarity == " 1":
                                color = "green"
                            elif polarity == " 0":
                                color = "blue"
                            elif polarity == "-1":
                                color = "red"
                            
                            p_style = f"<p style='color:{color};'>"

                            self.wfile.write(p_style.encode("utf-8") + p[:-2].encode("utf-8") + b"</p>")
                        else:
                            self.wfile.write(b"<p>" + p.encode("utf-8") + b"</p>")
                    
                    else:
                        self.wfile.write(b"<p>" + p.encode("utf-8") + b"</p>")

            # add visualization for annotated articles            
            if annotated:
                get_polarity_graph(file_path,"pol.png")
                self.wfile.write(b"<h4>Polarity Trend in this Article:</h4>")

                self.wfile.write(b"<div class='content'><img src =" + b"../images/pol.png" +b"></div>")


            self.wfile.write(b'</body>')
   
        ## Search Part Ends 
          
        # Add background image to the main page
        elif "bkg.PNG" in self.path:
            self.send_header('Content-type','image/png') # what service we are sending over
            self.end_headers()
            with open("images/bkg.PNG", "rb") as f:
                self.wfile.write(f.read())
 

        return



### Run the Server

if __name__ == "__main__": # only runs the following code when this script is run
    http_port=9998
    server = HTTPServer(('localhost', http_port),  MyWebServer)
    server.serve_forever()