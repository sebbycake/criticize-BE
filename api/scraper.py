import re
import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        #We specify the websites in the order
        self.source = NewsSource
        self.Sites_to_Scrape = ["https://www.channelnewsasia.com"] #"https://www.bbc.com/news"]
        self.site_name = self.get_cat_name()
        self.all_soups = {self.site_name[i]: BeautifulSoup(requests.get(self.Sites_to_Scrape[i]).text, 'lxml') for i in range(len(self.site_name))}
        ##Following the website's order, we create their classes with their soups
        ## We must have already created its class and specified its arguments
        self.all_categories = self.create_cat_classes()

    def get_cat_name(self):
        return ["".join(re.split("www.|.com|.sg|https://|/", item)) for item in self.Sites_to_Scrape]


    def create_cat_classes(self):
        for i in range(len(self.Sites_to_Scrape)):
            site_name = self.site_name[i]
            current_soup = self.all_soups[site_name]
            exec("global %s; %s = %s(%s, %s)" % (site_name, site_name, site_name, "self.Sites_to_Scrape[i]", "current_soup"))


    ## return as a dictionary the titles of 
    def get_source_and_title(self):
        to_return = []
        for i in range(len(self.site_name)):
            to_return.extend(eval(self.site_name[i]).article_titles())
        return to_return


class NewsSource:
    #may accept varargs at the back
    def __init__(self, site_being_scraped, soup, tag, class_field, domain_list, get_article_tag,
                 get_article_class, arti_tag, arti_class, need_link, need_trunc_link, *trunc_link):
        #specify the number of articles we want per domain
        self.need_link = need_link
        self.need_trunc_link = need_trunc_link
        self.trunc_link = list(trunc_link)
        self.article_per_domain = 10
        self.scraping_site = site_being_scraped
        self.tag = tag
        self.soup = soup
        self.class_field = class_field
        self.domains = domain_list
        self.all_link_domains = self.get_link_domains()


        #returns a dictionary of Category of news and the Category class
        self.all_domain_classes = self.make_classes(get_article_tag, get_article_class, arti_tag, arti_class)


        #self.kk = self.me()
        
    def make_classes(self, get_article_tag, get_article_class, arti_tag, arti_class):
        lst = dict()
        for key, value in self.all_link_domains.items():
            if self.need_trunc_link:
                new_Cat = Category(self.scraping_site, value, self.article_per_domain, get_article_tag,
                               get_article_class, arti_tag, arti_class, self.trunc_link[0])
            else:
                new_Cat = Category(self.scraping_site, value, self.article_per_domain, get_article_tag,
                               get_article_class, arti_tag, arti_class)
            
            lst[key] = new_Cat
        return lst


    #def me(self):
     #   print(self.all_domain_classes)
    

    def article_titles(self):
        to_return = []
        for header in self.all_domain_classes.keys():
            title = self.all_domain_classes[header].get_titles()
            news = self.all_domain_classes[header].all_articles_full_text()
            for i in range(len(title)):
                inter = dict()
                inter['title'] = title[i]
                inter["content"] = news[i]
                inter["publisher"] = "".join(re.split("www.|.com|.sg|https://|/", self.scraping_site))
                inter["category"] = header
                to_return.append(inter)
        return to_return 
    

    def get_link_domains(self):
        #assuming the scraped part also has the href hyperlink
        all_links = self.soup.find_all(self.tag, class_ = self.class_field, href = True)
        all_wanted_obj = list(filter(lambda x: x.text in self.domains, all_links))
        if (self.need_link):
            all_links = dict(map(lambda x: (x.text, self.trunc_link[0] + x.attrs["href"]), all_wanted_obj))
        else:
            all_links = dict(map(lambda x: (x.text, x.attrs["href"]), all_wanted_obj))
        return all_links
    


class channelnewsasia(NewsSource):
    def __init__(self, site_being_scraped, soup):
        ### We self specify this part
        super(channelnewsasia, self).__init__(site_being_scraped, soup, "a", "nav-sections__list-item-link", ["Singapore", "Asia", "World", "Business", "Sport"],
                         "a","teaser__title","div", "c-rte--article", False, False)


'''

class bbcnews(NewsSource):
    def __init__(self, site_being_scraped, soup):
        super(bbcnews, self).__init__(site_being_scraped, soup, "a", "nw-o-link",
                                      ["Business", "Coronavirus", "Science", "World", "UK", "Tech", "Asia"],
                                      "a", "gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor",
                                      "div", "ssrcss-rgov1k-MainColumn e1sbfw0p0", True, True, "https://www.bbc.com")
                                  #Anything below here are additional tags required on top of the usuals ones
                                  #"h3", "gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text")
'''



class Category:
    
    #may accept varargs at the back
    def __init__(self, main_landing_link, category_link, no_articles, get_article_tag,
                 get_article_class, arti_tag, arti_class, *trunc_link):
        self.cat = category_link
        self.trunc_link = list(trunc_link)
        self.main_link = main_landing_link
        self.soup = BeautifulSoup(requests.get(category_link).text, 'lxml')
        self.no_of_articles = no_articles
        self.all_articles = self.soup.find_all(get_article_tag, class_ = get_article_class, href= True)
        self.article_titles = list(set(map(lambda x: " ".join(x.text.split()), self.all_articles)))
        self.article_links = self.get_article_links()


        self.lmao = get_article_tag
        self.looo = get_article_class


        self.arti_tag = arti_tag
        self.arti_class = arti_class

        #returns a dictionary of Category of news and the Category class
        #self.all_article = self.all_articles_full_text()

    def get_article_links(self):
        if len(self.trunc_link) == 0:
            return list(set(map(lambda stuff: self.main_link + stuff.attrs["href"], self.all_articles)))
        return list(set(map(lambda stuff: self.trunc_link[0] + stuff.attrs["href"]
                        if not re.match(r'^%s' % self.trunc_link[0], stuff.attrs["href"]) else stuff.attrs["href"]
                        , self.all_articles)))

        
    def all_articles_full_text(self):
        my_texts = []
        links = self.article_links[:self.no_of_articles]
        for link in links:
            my_soup = BeautifulSoup(requests.get(link).text, 'lxml')
            content = self.run_trials(my_soup)
            my_texts.append(content)
        return my_texts

    def run_trials(self, soup):
        trials = 4
        for i in range(trials):
            main_article = soup.find(self.arti_tag, class_ = self.arti_class)
            if (main_article != None):
                content = " ".join(list(map(lambda j: " ".join(j.text.split("\xa0")), main_article.find_all("p"))))
                return content
        return "No text available"
            
    def get_titles(self):
        return self.article_titles[:self.no_of_articles]
