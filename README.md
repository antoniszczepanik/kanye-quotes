# Kanye Quotes
This is a solution to some recruitment task in some company :) 

## How to run the project?
	- clone
	- install python
	- setup for localdev

The solution is tested on TODO

## How to deploy the project?
	- point nginx/apache at port and serve index.html as static TODO
	- take a look at example in github actions TODO

## About the solution
Some specific information about the decisions made.
I decided to write the logic as a server because:
	- It's client agnostic - even though I provide web client we could easily integrate it with any client, be that mobile or desktop.
	- It's written in a stateless manner - we could scale it vertically and the only bottleneck we could hit is performance of used API's.

Web interface was used to present results because
	- It's fully cross platform. Web browsers work on every system and device.
	- There's no need to install anything on the client side. Just request the page.
	- It's user friendly. Many users are not comfortable with i.e. CLI interfaces. That's not the case with web, most users are familiar with it.
