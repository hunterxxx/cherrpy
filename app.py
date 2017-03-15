#wikipedia api is easy but not for advanced usage, thus BeautifulSoup is used
from pptx import Presentation
import wikipedia
#wiki text scrap
from bs4 import BeautifulSoup
#html request
import requests
from cherrypy.lib import static
import cherrypy
import os
from jinja2 import Environment, FileSystemLoader

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

env = Environment(loader=FileSystemLoader('html'))

#wiikipedia api
city_name = "Leipzig"
city = wikipedia.page("Leipzig")

#beautifulsoup library
url= "https://en.wikipedia.org/wiki/" + city_name
content = requests.get(url).content
soup = BeautifulSoup(content, 'lxml')

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        data_to_show = ['Hello', 'world']
        tmpl = env.get_template('index.html')

        prs = Presentation()
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]

        title.text = "Hello, World!"
        subtitle.text = "python-pptx was here!"

        prs.save('test1.pptx')
        #RETURN_FILE = open("test1.txt",'r')
        #return serve_fileobj(RETURN_FILE,disposition='attachment',content_type='.txt',name=none)
        #return tmpl.render(data=data_to_show)

    @cherrypy.expose
    def download(self):
        path = os.path.join(absDir, "test1.pptx")
        return static.serve_file(path, "application/x-download",
                                 "attachment", os.path.basename(path))

config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    },
    '/assets': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'assets',
    }
}

cherrypy.quickstart(HelloWorld(), '/', config=config)
