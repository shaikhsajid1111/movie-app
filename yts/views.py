from django.shortcuts import render,HttpResponse
from django.views import View
from django.template import RequestContext
import requests
import json

# Create your views here.
class homeView(View):
    '''for home,browse page'''
    template_name = 'index.html'

    def get(self,request):
        '''GET methods,
        > takes response from the API,
        >returns movies '''
        #taking response from the API
        response = requests.get('https://yts.mx/api/v2/list_movies.json')
        #converting the response to JSON format
        Json_format = response.json()
        return render(request,self.template_name,{
        "movies": Json_format['data']['movies'],
        'current_page_number' : Json_format['data']['page_number'],
        "next_page_number": int(Json_format['data']['page_number']+1),
        "later_page_number" : int(Json_format['data']['page_number']+2)
        })
    def post(self,request):
        response = requests.get('https://yts.mx/api/v2/list_movies.json')
        Json_format = response.json()
        return render(request,self.template_name,{
        "movies": Json_format['data']['movies'],
        'current_page_number' : Json_format['data']['page_number'],
        "next_page_number": int(Json_format['data']['page_number']+1),
        "later_page_number" : int(Json_format['data']['page_number']+2)
        })    

class detailView(View):
    template_name = "detail.html"
    ids = None
    def get_object(self,queryset = None):
        return queryset.get(ids = self.ids)
    def get(self,request,ids):
        URL = 'https://yts.mx/api/v2/movie_details.json?movie_id={ids}&with_images=true&with_cast=true'.format(ids = ids)
        response = requests.get(URL)
        json_format = response.json()
        return render(request,self.template_name,{'data' : json_format['data']['movie']})
    def post(self,request,ids):
        URL = 'https://yts.mx/api/v2/movie_details.json?movie_id={ids}&with_images=true&with_cast=true'.format(ids = ids)
        response = requests.get(URL)
        json_format = response.json()
        return render(request,self.template_name,{'data' : json_format['data']['movie']})    

class searchView(View):
    template_name = 'result.html'
    def get(self,request):
        try:
            search_query = request.GET['movie']
            response = requests.get('https://yts.mx/api/v2/list_movies.json?query_term={search}'.format(search = search_query))
            json_format = response.json()
          
            return render(request,self.template_name,{
                "movies" : json_format['data']['movies'] ,
                'movie_count':json_format['data']['movie_count'], 
                'query' : search_query})
        except:
            return HttpResponse("Nothing Found")        
    def post(self,request):
        try:
            search_query = request.POST['movie']
            response = requests.get('https://yts.mx/api/v2/list_movies.json?query_term={search}'.format(search = search_query))
            json_format = response.json()
            #print(json_format['data']['movies'])
            return render(request,self.template_name,{
                "movies" : json_format['data']['movies'] ,
                'movie_count':json_format['data']['movie_count'], 
                'query' : search_query}) 
        except:
            return HttpResponse("Nothing Found")                   

class nextPage(View):
    template_name = 'index.html'
    page_number = None
    def get_object(self,queryset = None):
        return queryset.get(page_number = self.page_number)

    def get(self,request,page_number):
        try:
            respond = requests.get('https://yts.mx/api/v2/list_movies.json?page={page}'.format(page = page_number))
            json_format_page = respond.json()
            current_page_number = json_format_page['data']['page_number']
            
            return render(request,self.template_name,{
        'movies': json_format_page['data']['movies'],
        'current_page_number': (int(current_page_number)),
        "next_page_number": int(json_format_page['data']['page_number']+1),
        "later_page_number" : int(json_format_page['data']['page_number']+2)
        })
        except:
            return HttpResponse("No page Found!")
    def post(self,request,page_number):
        try:
            respond = requests.get('https://yts.mx/api/v2/list_movies.json?page={page}'.format(page = page_number))
            json_format_page = respond.json()
            current_page_number = json_format_page['data']['page_number']
            return render(request,self.template_name,{
        'movies': json_format_page['data']['movies'],
        'current_page_number': (int(current_page_number)),
        "next_page_number": int(json_format_page['data']['page_number']+1),
        "later_page_number" : int(json_format_page['data']['page_number']+2)
        })    
        except:
            HttpResponse("Page Not Found!")