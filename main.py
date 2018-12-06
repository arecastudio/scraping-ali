from bs4 import BeautifulSoup
import requests,csv,json
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# browser = webdriver.PhantomJS('/opt/phantomjs/bin/phantomjs')
# browser = webdriver.Chrome("./chromedriver")

#browser = webdriver.Chrome("/usr/bin/chromedriver")
urs="https:"
woman_link="https://www.aliexpress.com/category/100003109/women-clothing-accessories.html?spm=2114.11010108.101.1.650c649bxRk6dj"
woman_sub_link="https://www.aliexpress.com/category/100003109/women-clothing-accessories/arecastudio.html?site=glo&g=y&needQuery=n&tag="

def getLinks():
    req=requests.get(woman_link).text
    soup=BeautifulSoup(req,'lxml')
    links=[]
    links.append(woman_link)
    mdiv=soup.find('div',class_='ui-pagination-navi util-left')
    anc=mdiv.find_all('a')
    for a in anc:
        #print(a)
        try:
            if int(a.text)>0:
    #            print(str("https:"+a.get('href')))
                link="https:"+a.get('href')
                links.append(link)
        except:
            pass

    for l in links:
        print(l)
        #scrapeMe(l)
#----------------------------------------------------------------------------------------------------------------------------------------------



ex_detail_link="https://www.aliexpress.com/item/Summer-Kpop-Seventeen-T-Shirt-with-Short-Sleeve-Fashion-Cotton-T-Shirt-Seventeen-tshirt-for-Young/32819238260.html?spm=2114.search0103.3.27.117a3a216UHcC2&ws_ab_test=searchweb0_0,searchweb201602_2_10065_10068_10890_5730315_319_10546_317_10548_10696_453_10084_454_10083_10618_5729215_10307_537_536_10059_10884_10887_100031_321_322_10103,searchweb201603_51,ppcSwitch_0&algo_expid=667d20b9-fc5f-4c68-927b-e56ea42e2e31-3&algo_pvid=667d20b9-fc5f-4c68-927b-e56ea42e2e31"
def womanDetail(link):
    req=requests.get(link).text
    #browser.get(link)
    soup=BeautifulSoup(req,'lxml')
    #soup=BeautifulSoup(browser.page_source,'html.parser')
    try:
        x=soup.find('h1',class_='product-name')
        if x is not None:
            _product_name=x.text
        else:
            _product_name=''
            
        x=soup.find('span',class_='p-symbol')
        if x is not None:
            _price_symbol=x.text
        else:
            _price_symbol=''
            
        x=soup.find('span',id='j-sku-price')
        if x is not None:
            _price=x.text
        else:
            _price=''
            
        x=soup.find('span',id='j-sku-discount-price')
        if x is not None:
            _disc_price=x.text
        else:
            _disc_price=''
            
        x=soup.find('a',class_='store-lnk')
        if x is not None:
            _shop_name=x.text
        else:
            _shop_name=''

        _shop_url=''
        x=soup.find('a',class_='store-lnk')
        if x is not None:
            xx=x.get('href')
            if xx is not None:
                _shop_url=xx

        x=soup.find('span',id='j-wishlist-num')        
        if x is not None:
            _wishlist_num=x.text
        else:
            _wishlist_num='0'

        _brand_name=''
        x=soup.find('li',id='product-prop-2')
        if x is not None:
            xx=x.find('span',class_='propery-des')
            if xx is not None:
                _brand_name=xx.text

        _image=''
        x=soup.find('a',class_='ui-image-viewer-thumb-frame')
        if x is not None:
            xx=x.find('img')#.get('src')
            if xx is not None:
                _image=xx.get('src')
                if _image is None:
                    _image=xx.get('image-src')

        _cat=''
        x=soup.find('div',class_='ui-breadcrumb')
        if x is not None:
            xx=x.find('div',class_='container')
            if xx is not None:
                xxx=xx.find('h2')
                if xxx is not None:
                    xxxx=xxx.find('a')
                    if xxxx is not None:
                        _cat=xxxx.text

        x=soup.find('span',id='j-order-num')
        if x is not None:
            _order_num=x.text
        else:
            _order_num=''
            
        x=soup.find('span',class_='rantings-num')
        if x is not None:
            _review_num=x.text
        else:
            _review_num='0'

        _review_score='0'
        x=soup.find('span',class_='percent-num')
        if x is not None:
            _review_score=x.text

        my_dictionary={
            'product_name':_product_name.strip().replace(";"," "),
            'price_symbol':_price_symbol,
            'price':_price,
            'disc_price':_disc_price,
            'shop_name':_shop_name.strip().replace(";"," "),
            'shop_url':urs+_shop_url,
            'wishlist_num':_wishlist_num,
            'brand_name':_brand_name.strip().replace(";"," "),
            'image':_image,
            'cat':_cat,
            'order_num':_order_num.replace("orders","").replace("order","").strip(),
            'review_num':_review_num.replace("(","").replace("votes)","").strip(),
            'review_score':_review_score
        }
        #print('name'+_product_name)
        #print('symbol'+_price_symbol)
        #print('price'+_price)
        #print('disc'+_disc_price)
        #print('seller'+_shop_name)
        #print('seller url'+urs+_shop_url)
        #print('wishlist'+_wishlist_num)
        #print('brand'+_brand_name)
        #print('image'+_image)
        #print('cat'+_cat)
        #print('order count'+_order_num.replace("orders","").strip())
        #print('review count'+ _review_num.replace("(","").replace("votes)","").strip() )
        
        return my_dictionary
    except Exception as e:
        print('-----------------------------------------------------------')
        if hasattr(e,'message'):
            print('Error:',str(e.message))
        else:
            print('Error:',str(e))        
        print('-----------------------------------------------------------')

        

def produceLinks():
    links=[]
    links.append(woman_link)
    for x in range(2,100+1):
        link=woman_sub_link.replace("arecastudio",str(x))
        links.append(link)
        #print(link)
        #scrapeMe(link)

    for link in links:
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(link)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')        
        #scrapeMe(link)
        produceSubLinks(link)

def produceSubLinks(link):
    result=[]
    req=requests.get(link).text
    soup=BeautifulSoup(req,'lxml')
    try:
        urls=soup.find_all('div',class_='item')
        for item in urls:
            _url=item.find('a',class_='product')
            if _url is not None:
                _ur=urs+_url.get('href')
                result.append(_ur)
            else:
                _ur=''
    except Exception as e:
        print('----------------------------------------------------')
        print('Error: ',str(e))
        print('----------------------------------------------------')        
        
    for page_url in result:
        try:
            #print(page_url)
            dct=womanDetail(page_url)
            print(dct["shop_name"])
            writer.writerow([
                page_url,
                dct["product_name"],
                dct["shop_name"],
                dct["wishlist_num"],
                dct["brand_name"],
                dct["image"],
                dct["price"],
                dct["cat"],
                dct["review_num"],
                dct["review_score"],
                dct["order_num"]
            ])
        except Exception as e:
            print('----------------------------------------------------')
            print('Error: ',str(e))
            print('----------------------------------------------------')



        
def scrapeMe(link):
    req=requests.get(link).text
    soup=BeautifulSoup(req,'lxml')
    
    items=soup.find_all('div',class_='item')
    for item in items:
        #TODO: Jangan ambil products link dari gambar, ambil dari title
        a=item.find('div',class_='img img-border').find('div',class_='pic').find('a',class_='picRind')
        img=a.find('img',class_='picCore').get('image-src')
        if img is None:
            img=a.find('img',class_='picCore').get('src')
        try:
            _url=urs+item.find('a',class_='product').get('href')
            #print('\n\n---------------------------------------------------------------------------------------------------')
            #print('https:'+a.get('href').strip())
            #print(img.get('alt'),'\n','https:'+img.get('image-src'))
            ##print(img)
            #_name=str(item.find('div',class_='info').find('h3').find('a').text)
            #_store=str(item.find('div',class_='info-more').find('div',class_='store-name-chat').find('div',class_='store-name util-clearfix').find('a').text)
            #_url="https:"+str(a.get('href')).strip()
            #print(_url)
            dct=womanDetail(_url)
            _image_url="https:"+str(img)
            #print(dct)
            #writer.writerow([ _name, _store, _url, _image_url ])
#            writer.writerow([
#                _url,
#                dct["product_name"],
#                dct["shop_name"],
#                dct["wishlist_num"],
#                dct["brand_name"],
#                dct["image"],
#                dct["price"],
#                dct["cat"],
#                dct["review_num"],
#                dct["review_num"],
#                dct["order_num"]
#            ])
        except Exception as e:
            print('###############################')
            print('Error desc: ',str(e))
            print('###############################')

#scrapeMe(woman_link)


outfile = open('woman-chloting-aliexpress.csv','w', newline='')
writer = csv.writer(outfile)
writer.writerow([
    "product_page_url",
    "product_tile",
    "shop_name",
    "add_to_wishlist_number",
    "brand_name",
    "image_url",
    "price",
    "category",
    "number_of_reviews",
    "review_score",
    "number_of_orders"
])
    
produceLinks()
#mydict=womanDetail(ex_detail_link)
#print(mydict['product_name'])

outfile.close()


#TODO project 1:
#Product Page URL
#Product Title
#Shop Name
#Add to Wishlist Number
#Brand Name
#Image
#Price
#Category 
#Number of Reviews
#Review Score
#Number of Orders
