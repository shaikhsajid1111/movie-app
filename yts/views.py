from django.shortcuts import render,HttpResponse,Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
import requests
import json

def fetch_data(url:str):
    '''takes parameter URL of string,
    ->takes response from the URL and 
    -> returns JSON format data 
    similar to:
    response = requests.get(url)
    return response.json()
    '''
    return (requests.get(url)).json()
    

class homeView(ListView):
    '''for home,browse page'''
    template_name = 'index.html'
    try:
        @csrf_exempt
        def get(self,request):
            '''GET methods,
            > takes response from the API,
            >returns movies '''
            #taking response from the API
            Json_format = fetch_data('https://yts.mx/api/v2/list_movies.json')
            '''retrning Http Response with template'''
            return render(request,self.template_name,{
        "movies": Json_format['data']['movies'],
        'current_page_number' : Json_format['data']['page_number'],
        "next_page_number": int(Json_format['data']['page_number']+1),
        "later_page_number" : int(Json_format['data']['page_number']+2)
        })
    except:
        Http404("Failed to Load Page!")

class detailView(DetailView):
    template_name = "detail.html"
    ids = None
    @csrf_exempt
    def get_object(self,queryset = None):
        return queryset.get(ids = self.ids)
    def get(self,request,ids):
        '''takes request and ID from the URL'''
        #generating URL from the passed ID
        try:
            URL = 'https://yts.mx/api/v2/movie_details.json?movie_id={ids}&with_images=true&with_cast=true'.format(ids = ids)
        #fetching data from the generated URL
            json_format = fetch_data(URL)
        #returning Http Response 
            return render(request,self.template_name,{
            'data' : json_format['data']['movie']}
            )
        except:
            return Http404("No Page Found")
  
class searchView(ListView):
    template_name = 'result.html'
    @csrf_exempt
    def get(self,request):
        try:
            #fetching search term from the request
            search_query = request.GET['movie']
            url = 'https://yts.mx/api/v2/list_movies.json?query_term={search}'.format(search = search_query)
            json_format = fetch_data(url)
          
            return render(request,self.template_name,{
                "movies" : json_format['data']['movies'] ,
                'movie_count':json_format['data']['movie_count'], 
                'query' : search_query})
        except:
            return HttpResponse("No Movie Found!")        
    
class nextPage(ListView):
    template_name = 'index.html'
    page_number = None
    def get_object(self,queryset = None):
        return queryset.get(page_number = self.page_number)
    @csrf_exempt
    def get(self,request,page_number):
        try:
            URL = 'https://yts.mx/api/v2/list_movies.json?page={page}'.format(page = page_number)
            json_format_page = fetch_data(URL)
            current_page_number = json_format_page['data']['page_number']
            
            return render(request,self.template_name,{
        'movies': json_format_page['data']['movies'],
        'current_page_number': (int(current_page_number)),
        "next_page_number": int(json_format_page['data']['page_number']+1),
        "later_page_number" : int(json_format_page['data']['page_number']+2)
        })
        except:
            return Http404("No Movie Found!")
    