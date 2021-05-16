# Kanye Quotes
This is a solution to some recruitment task in some company. 
It's a webserver with a simple API and a client which allows you to
analyse arbitrary number of Kanye West quotes with regards to their sentiment. 
I had some time left so I decided to [host it on my Raspberry :)](https://kanye.antoniszczepanik.com/)

## How to run the project?
To run the project you will need `Python 3.7+`.

Information on how to download and install Python could be found [here.](https://wiki.python.org/moin/BeginnersGuide/Download)
If you want to jump straight to downloads here they are:
* [For MacOS](https://www.python.org/downloads/mac-osx/)
* [For Windows](https://www.python.org/downloads/mac-osx/)
* On Debian you could just `sudo apt install python3.9 python3.9-dev`

Then you can clone and run the project right away:
```
git clone https://github.com/antoniszczepanik/kanye-quotes.git
cd kanye-quotes
pip install -r requirements.txt
python3 server/server.py
```

That's all! The site is available at `http://localhost:8000`.

If you wouldn't like to pollute your environment with `requrements.txt` packages you
can use any Python virual environment manager. For example using `venv`:

On Unix/MacOS:
```
git clone https://github.com/antoniszczepanik/kanye-quotes.git
cd kanye-quotes
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 server/server.py
```

On Windows
```
git clone https://github.com/antoniszczepanik/kanye-quotes.git
cd kanye-quotes
python3 -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python3 server/server.py
```


## How to deploy the project?
To deploy the project is is enough to:

	1. Run server in the background (i.e. `python3.9 server/server.py &` on Unix systems).
	2. Point any webserver (`Nginx`, `Apache`,...) at `http://localhost:8000`.

## About the solution

Some specific information about the solution and decisions made.

I decided to implement the solution with server/client architecture because:
* It's client agnostic - even though I provide web interface we could easily integrate it with any client, be that mobile or desktop.
* We could scale server vertically. We use two separate API calls (documented below) to get necessary data. Hence no data is stored server side and we could freely duplicate server instance.

Web interface was used to present results because
* It's fully cross platform. Web browsers work on every system and device.
* There's no need to install anything on the client side. Just request the page.
* It's user friendly. Many users are not comfortable with for example CLI interfaces. That's not the case with web, most users are familiar with it.

I decided to implement server in Python because of limited time amount.
The solution uses only Python builtins extensively, the crucial one being HTTPServer.
I would not recommend to run this server production. Using a proper 
framework and WSGI server would be more advised, however no Frameworks were allowed for this specific task.

Webserver makes requests to external APIs in async manner which makes them
pretty fast, even though only single process is used :)


**API Documentation**
----

`GET /api/v1/quotes`  <b>Get specific number of unique Kanye quotes.</b>
  
*  **URL Params**
 
   `number=[integer] (required)`

* **Success Response:**
 
    **Content:** `{ "quotes" : ["quote1", "quote2", "quote3" }`
 
* **Sample Call:**

  `GET http://localhost:8000/api/v1/quotes=number=5`
  
  </br>

`POST /api/v1/sentiment`  <b>Get sentiment summary based on list of quotes sent.</b>

* **Data Params**

  Accepts JSON data with a list of quotes.
  `{ "quotes" : ["A branch was used", "when", "working on this solution"] }`


* **Success Response:**
 
    **Content:** `{ "positive_counts" : 2, "negative_count": 1, "neutral_counts": 2, "most_extreme": "quote2"}`
