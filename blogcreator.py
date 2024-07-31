import asyncio
import fastapi_poe as fp
import os
from pathlib import Path
from datetime import datetime
import re

api_key = ''

async def get_response(api_key, message):
    responses = []  # List to store the responses
    async for partial in fp.get_bot_response(messages=message, bot_name="Mixtral-8x7b-Chat", api_key=api_key):
        responses.append(partial)  # Collect each partial response
    # After collecting all responses, combine and print them
    full_response = "".join([resp.text for resp in responses])
    print(full_response)
    return full_response

async def get_keywds(api_key, message2):
    responses = []  # List to store the responses
    async for partial in fp.get_bot_response(messages=message2, bot_name="Mixtral-8x7b-Chat", api_key=api_key):
        responses.append(partial)  # Collect each partial response
    # After collecting all responses, combine and print them
    keywds_response = "".join([resp.text for resp in responses])
    print(keywds_response)
    return keywds_response

async def create_file(full_response, keywds_response, filename):
    title_match = re.search(r'<h1>(.*?)<\/h1>', full_response, re.IGNORECASE)
    dtitle = title_match.group(1) if title_match else None

    # Remove the title from the response to get the rest of the content
    dcontent = re.sub(r'<h1>.*?<\/h1>', '', full_response, flags=re.IGNORECASE).strip()
    dkeywds = keywds_response
    print("Title:", dtitle)
    print("Content:", dcontent)
    print("Keywords:", dkeywds)
    date = '1/23/2024'

    htmlcode = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>"""+dtitle+"""</title>
        <meta name="description" content="An article about """+dtitle+"""">
        <meta name="author" content="example">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Wruczek/Bootstrap-Cookie-Alert@gh-pages/cookiealert.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.3.0/css/all.min.css">
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        <style>
            /* Basic styling for readability */
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1, h2, h3 {
                color: #333;
            }
            p {
                margin-bottom: 1.5em;
            }
            img {
                padding-top: 20px;
                padding-bottom: 20px;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 50%;
            }
        </style>
        <link rel="stylesheet" href="/styles.css">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand" href="/">example</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <a class="nav-item nav-link" href="/">Home</a>
                    <a class="nav-item nav-link active" href="/calculator">Calculator</a>
                    <a class="nav-item nav-link" href="/contactus">Contact Us</a>
                    <a class="nav-item nav-link" href="/privacypolicy">Privacy Policy</a>
                </div>
            </div>
        </nav>
        <div class="container">
            <article>
                <h2>"""+dtitle+"""</h2>
                <img src="/images/teslachargerlocations.jpg" class="d-block w-100" id="blogs" alt="Tesla Charger Locations">
                </img>
                """+dcontent+"""
            </article>
            <div class="alert text-center cookiealert" role="alert">
                &#x1F36A; We use cookies to improve your experience and personalize content and advertisements. By continuing to use our website, you consent to our use of cookies. <a href="https://cookiesandyou.com/" target="_blank">Learn more</a>
            
                <button type="button" class="btn btn-info btn-sm acceptcookies">
                    Ok
                </button>
            </div>
            <footer>
                <p>&copy; 2024 example</p>
            </footer>
        </div>
        <script type="application/ld+json">
            {
            "@context": "http://schema.org",
            "@type": "BlogPosting",
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": "http://example.com"
            },
            "headline": \""""+dtitle+"""",
            "keywords": \""""+dkeywds+"""",
            "datePublished": \""""+date+"""",
            "dateModified": \""""+date+"""",
            "author": {
                "@type": "Person",
                "name": "example",
                "url": "http://example.com"
            },
            "publisher": {
                "@type": "Organization",
                "name": "example",
                "url": "http://example.com"
            }
            }  
        </script>
        <script src="https://cdn.jsdelivr.net/gh/Wruczek/Bootstrap-Cookie-Alert@gh-pages/cookiealert.js"></script>
    </body>
    </html>"""

    file_path =  os.path.join(filename+'.html')    
    #file_path =  os.path.join('webpages', 'testfile.html')

    # Write the file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(htmlcode)
        print('File has been written successfully')
    except Exception as e:
        print(f'An error occurred writing the file: {e}')


#ogprompts = ["Electric vehicles vs gas vehicles", "Electric vehicles vs hybrid", "Electric vehicles vs fuel vehicles", "Electric vehicles vs conventional vehicles", "Electric vehicles vs gasoline vehicles", "Electric vehicles vs hydrogen vehicles", "Electric vehicles vs combustion engine", "Electric vehicles vs gas cost", "Electric vehicles vs combustion vehicles", "Electric vehicles vs fossil fuel vehicles", "Electric vehicles vs public transportation", "Electric vehicles vs petrol vehicles", "Electric vehicles vs fuel vehicles ppt", "Electric vehicles or gas vehicles", "Electric vehicles or electrical vehicles", "Electric vehicles or fuel vehicle", "Electric vehicles or hydrogen fuel cell", "Electric vehicles and cold weather", "Electric vehicles and climate change", "Electric vehicles and the power grid", "Electric vehicles and fires", "Electric vehicles and environmental sustainability", "Electric vehicles and radiation", "Electric vehicles and the grid", "Electric vehicles and environment", "Electric vehicles and cold climates", "Electric vehicles and parking garages", "Electric vehicles and winter", "Electric vehicles and lithium mining", "Electric vehicles and the economy", "Electric vehicles and hov lanes", "Electric vehicles and prices", "Electric vehicles in cold weather", "Electric vehicles 2023", "Electric vehicles 2024", "Electric vehicles cold", "Electric vehicles for sale", "Electric vehicles news", "Electric vehicles headaches in cold weather", "Electric vehicles tax credit", "Electric vehicles chicago", "Electric vehicles reddit", "Electric vehicles for sale near me", "Electric vehicles eligible for tax credit", "Electric vehicles suv", "Electric vehicles that qualify for tax credit", "Electric vehicles for kids", "Electric vehicles to lease", "Electric vehicles to buy", "Electric vehicles to invest in", "Electric vehicles to avoid", "Electric vehicles to dominate the market", "Electric vehicles to rent", "Electric vehicles in india", "Electric vehicles for sale", "Electric vehicles for sale near me", "Electric vehicles in australia", "Electric vehicles in canada", "Electric vehicles in the philippines", "Electric car to buy", "Electric vehicles with awd", "Electric vehicles for 2024", "Electric vehicles virginia", "Electric vehicles maryland", "Electric vehicles near", "Icon electric vehicles near me", "Used electric vehicles near me", "Electric vehicle showroom near me", "Electric vehicles around the world", "Electric vehicles around 30k", "Electric vehicles around 40k", "Electric cars in near future", "How electric vehicles can reduce air pollution", "Electric vehicles that can power a house", "Electric vehicles without license", "Electric vehicles without registration", "Electric vehicle without home charger", "Electric vehicle without battery", "Electric vehicle without garage", "Electric vehicle without transmission", "Electric vehicles not selling", "Electric car without home charging", "Electric car without driving licence", "Electric vehicles or gas vehicles", "Electric vehicles or electrical vehicles", "Electric vehicles or fuel vehicle", "Electric vehicles or hydrogen fuel cell", "Electric vehicles and cold weather", "Electric vehicles and climate change", "Electric vehicles and the power grid", "Electric vehicles and fires", "Electric vehicles and environmental sustainability", "Electric vehicles and radiation", "Electric vehicles and the grid", "Electric vehicles and environment", "Electric vehicles and cold climates", "Electric vehicles and parking garages", "Electric vehicles and winter", "Electric vehicles and lithium mining", "Electric vehicles and the economy", "Electric vehicles and hov lanes", "Electric vehicles and prices", "Electric vehicles in cold weather", "Electric vehicles 2024"] 
prompts = ["Electric Vehicles: Advantages and Disadvantages","Environmental Impact of Electric Vehicles","Cost Comparison: Electric Vehicles vs. Gas-Powered Vehicles","Charging Infrastructure for Electric Vehicles","Government Incentives and Policies for Electric Vehicles","Electric Vehicle Technology and Innovations","Future Trends in Electric Vehicle Development","Electric Vehicles and Sustainable Transportation","Electric Vehicles and Energy Efficiency","Electric Vehicles and Smart Cities","Electric Vehicles and Urban Mobility","Electric Vehicles and Long-Distance Travel","Electric Vehicles and Extreme Weather Conditions","Electric Vehicles and Safety","Electric Vehicles and Maintenance","Electric Vehicles and Consumer Behavior","Electric Vehicles and the Automotive Industry","Electric Vehicles and Global Markets","Electric Vehicles and the Economy","Electric Vehicles and Social Impact"]

async def main():
    #Continuing systematic naming of blog html files; last was blog27.html
    filenum = 27
    for topic in prompts:
        filenum = filenum+1
        filename = 'blog'+str(filenum)
        query = "Write a three thousand word article about "+topic+" formatted with HTML tags. Only send the formatted article, do not include any other text. Don't include any html besides from h1 to the end of the writing with <p>"
        print(type(query))
        message = fp.ProtocolMessage(role="user", content=query)
        content = await get_response(api_key, [message])
        print('getresponse called once')
        query2 = "give me a list of 10 longtail seo keywords that are not numbered for my article about "+topic+". only send the keywords without any numbers and seperated by commas. follow this example: keyword1, keyword2, keyword3"
        message2 = fp.ProtocolMessage(role="user", content=query2)
        keywords = await get_keywds(api_key, [message2])
        await create_file(content, keywords, filename)
        print('functionran for '+filename)

asyncio.run(main())