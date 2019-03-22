#!/usr/bin/env python
# coding: utf-8

# Section 19-215 onwards of Udemy Python course   https://www.udemy.com/the-python-mega-course/learn/v4/t/lecture/5569884?start=0

# In[1]:


import requests
from bs4 import BeautifulSoup


# In[2]:


request = requests.get('https://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/')
content = request.content

content


# In[5]:


soup = BeautifulSoup(content, 'html.parser')
soup


# In[110]:


# used below (19-218) in crawling to see how many pages are shown 
last_page_number = int(soup.find_all('a', {'class' : 'Page'})[-1].text)  # penultimate occurence
# look for element wherein 'last' page number is shown (turned out to be the *final* element with class 'Page')
print('Number of pages: ' + str(last_page_number))


# ... identify from HTML that DIVs of interest have class 'propertyRow' applied, so look for them ...

# In[9]:


all = soup.find_all('div', {'class':'propertyRow'})
all[0]


# In[10]:


# not actually a list per se, actually result set of BeautifulSoup, but has len function
len(all)  # get length of results


# ... after examining HTML to see occurences of price (all text within a h4 element with propPrice class e.g. <h4 class="propPrice">
# $725,000
# <span class="IconPropertyFavorite16"></span>
# </h4>), now get price element ...

# In[14]:


all[0].find_all('h4',{'class':'propPrice'})


# In[15]:


all[0].find_all('h4',{'class':'propPrice'})[0].text


# In[19]:


float(all[0].find_all('h4',{'class':'propPrice'})[0].text.replace('\n', '').replace(' ', '').replace('$','').replace(',',''))


#  ... or ...

# In[38]:


import re
regex_result = re.findall('\d+', all[0].find_all('h4',{'class':'propPrice'})[0].text)
value_string = ''.join(regex_result)
value_string


# 19-215 The objective here being to get property address, price and number of bathrooms ...
# 
# (Markup had been found out using Chrome F12 and elements arrow inspection.)

# In[59]:


# print all prices
for item in all:
    print(item.find('h4',{'class':'propPrice'}).text.replace("\n",''))  # replace('/n','').replace(' ','')
    # get address text (having found the appropriate span in markup)
    print(item.find_all('span', {'class' : 'propAddressCollapse'})[0].text)  # 
    # get number of baths (having found the appropriate span - but sometimes beds are before baths, or vice versa...)
    # actually inside <b> tag inside spans with infoFullBath - only 1 so find not find_all
    
    try:
        # print(item.find('span',{'class': 'infoValueFullBath'}).text)  # .text would take care of surrounding <b> tag
        print(item.find('span',{'class': 'infoValueFullBath'}).find('b').text)  # as I thought, take care of <b> manually
    except AttributeError:         # AttributeError found by checking during dev
        pass  # just carry on if not found
                                                                         
    try:
        print(item.find('span',{'class': 'infoSqFt'}).find('b').text)  # Square Feet inside <b> as well
    except AttributeError:
        print(None)     # try printing None (will print as string) if data not found
                                                                         
    
    print('\n')


# 19-216 ... now intended to extract the lot size value (not all results have a lot size, or lot size is in a different order, within containing element - in span featureName, but only if text of featureGroup SPANs  (within columnGroup DIVs) is 'lot size'  e.g. <span class="featureGroup">Lot Size: </span><span class="featureName">Under 1/2 Acre, </span><span class="featureName">0.23 Acres</span>) ...

# In[80]:


# print all prices
for item in all:
    print(item.find('h4',{'class':'propPrice'}).text.replace("\n",''))  # replace('/n','').replace(' ','')
    # get address text (having found the appropriate span in markup)
    print(item.find_all('span', {'class' : 'propAddressCollapse'})[0].text)  # 
    # get number of baths (having found the appropriate span - but sometimes beds are before baths, or vice versa...)
    # actually inside <b> tag inside spans with infoFullBath - only 1 so find not find_all
    
    try:
        # print(item.find('span',{'class': 'infoValueFullBath'}).text)  # .text would take care of surrounding <b> tag
        print(item.find('span',{'class': 'infoValueFullBath'}).find('b').text)  # as I thought, take care of <b> manually
    except AttributeError:         # AttributeError found by checking during dev
        pass  # just carry on if not found
                                                                         
    try:
        print(item.find('span',{'class': 'infoSqFt'}).find('b').text)  # Square Feet inside <b> as well
    except AttributeError:
        print(None)     # try printing None (will print as string) if data not found
                                                                             
    for column_group in item.find_all('div',{'class' : 'columnGroup'}):
        # print(column_group)
        # go through each column_group division (could be something other than 'lot size')
        try:
            # NB zip for checking 2 lists at once            
            for feature_group, feature_name in zip(column_group.find_all('span', {'class' : 'featureGroup'}), 
                                                   column_group.find_all('span', {'class' : 'featureName'})):
                # print(feature_group.text)
                # print(feature_name.text) 
                if ('Lot Size' in feature_group.text):
                    print(feature_name.text)
        except TypeError:
            # pass
            print(None)

            # if column_group
    
    print('\n')


# 19-217 ... storing data in dictionaries prior to writing to a file

# In[91]:


# dictionary-ise all data
list_of_feature_dictionary_entries = []
for item in all:
    dictionary = {}
    dictionary['Address'] = item.find_all('span', {'class' : 'propAddressCollapse'})[0].text
    dictionary['Locality'] = item.find_all('span', {'class' : 'propAddressCollapse'})[1].text
    dictionary['Price'] = item.find('h4', {'class' : 'propPrice'}).text.replace('\n','').replace(' ','')
        
    print(item.find('h4',{'class':'propPrice'}).text.replace("\n",''))  # replace('/n','').replace(' ','')
    # get address text (having found the appropriate span in markup)
    print(item.find_all('span', {'class' : 'propAddressCollapse'})[0].text)  # 
    # get number of baths (having found the appropriate span - but sometimes beds are before baths, or vice versa...)
    # actually inside <b> tag inside spans with infoFullBath - only 1 so find not find_all
    
    try:
        # print(item.find('span',{'class': 'infoValueFullBath'}).text)  # .text would take care of surrounding <b> tag
        dictionary['Full Baths'] = item.find('span',{'class': 'infoValueFullBath'}).find('b').text  # as I thought, take care of <b> manually
    except AttributeError:         # AttributeError found by checking during dev
        dictionary['Full Baths'] = None
        # pass  # just carry on if not found
    
    # could do similar for beds, &c....
                                                                         
    try:
        dictionary['Area'] = item.find('span',{'class': 'infoSqFt'}).find('b').text  # Square Feet inside <b> as well
    except AttributeError:
        dictionary['Area'] = None     # try printing None (will print as string) if data not found
                                                                             
    for column_group in item.find_all('div',{'class' : 'columnGroup'}):
        # print(column_group)
        # go through each column_group division (could be something other than 'lot size')
        try:
            # NB zip for checking 2 lists at once            
            for feature_group, feature_name in zip(column_group.find_all('span', {'class' : 'featureGroup'}), 
                                                   column_group.find_all('span', {'class' : 'featureName'})):
                # print(feature_group.text)
                # print(feature_name.text) 
                if ('Lot Size' in feature_group.text):
                    dictionary['Lot Size'] = feature_name.text
        except TypeError:
            pass
            # print(None)

            # if column_group
    
    #print('\n')
    
    list_of_feature_dictionary_entries.append(dictionary)
print(list_of_feature_dictionary_entries)


# In[93]:


import pandas
dataframe = pandas.DataFrame(list_of_feature_dictionary_entries)
dataframe


# In[94]:


dataframe.to_csv('Output_Property_Data.csv')


# 19-218 Crawling through successive linked pages (e.g. page 1,2,3 ...)

# In[116]:


base_url = 'http://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s='

# look for element wherein 'last' page number is shown (turned out to be the *final* element with class 'Page')
# obtained in an earlier calculation (qv)
# last_page_number = int(soup.find_all('a', {'class' : 'Page'})[-1].text)  # penultimate occurence

# for page in range (0,30,10):
for page in range (0, last_page_number * 10,10):
    print(base_url + str(page) + '.html')    
    request = requests.get(base_url + str(page) + '.html')
    content = request.content
    soup = BeautifulSoup(content,'html.parser')
    print(soup)
    all = soup.find_all('div', {'class':'propertyRow'})
    # print(all)
    list_of_feature_dictionary_entries = []
    for item in all:
        dictionary = {}
        dictionary['Address'] = item.find_all('span', {'class' : 'propAddressCollapse'})[0].text
        try:
            dictionary['Locality'] = item.find_all('span', {'class' : 'propAddressCollapse'})[1].text
        except:
            dictionary['Locality'] = None
        
        try:
            dictionary['Price'] = item.find('h4', {'class' : 'propPrice'}).text.replace('\n','').replace(' ','')
        except:#   # ought really to specify an exception here
            dictionary['Price'] = None

        print(item.find('h4',{'class':'propPrice'}).text.replace("\n",''))  # replace('/n','').replace(' ','')
        # get address text (having found the appropriate span in markup)
        print(item.find_all('span', {'class' : 'propAddressCollapse'})[0].text)  # 
        # get number of baths (having found the appropriate span - but sometimes beds are before baths, or vice versa...)
        # actually inside <b> tag inside spans with infoFullBath - only 1 so find not find_all

        try:
            # print(item.find('span',{'class': 'infoValueFullBath'}).text)  # .text would take care of surrounding <b> tag
            dictionary['Full Baths'] = item.find('span',{'class': 'infoValueFullBath'}).find('b').text  # as I thought, take care of <b> manually
        except AttributeError:         # AttributeError found by checking during dev
            dictionary['Full Baths'] = None
            # pass  # just carry on if not found

        # could do similar for beds, &c....

        try:
            dictionary['Area'] = item.find('span',{'class': 'infoSqFt'}).find('b').text  # Square Feet inside <b> as well
        except AttributeError:
            dictionary['Area'] = None     # try printing None (will print as string) if data not found

        for column_group in item.find_all('div',{'class' : 'columnGroup'}):
            # print(column_group)
            # go through each column_group division (could be something other than 'lot size')
            try:
                # NB zip for checking 2 lists at once            
                for feature_group, feature_name in zip(column_group.find_all('span', {'class' : 'featureGroup'}), 
                                                       column_group.find_all('span', {'class' : 'featureName'})):
                    # print(feature_group.text)
                    # print(feature_name.text) 
                    if ('Lot Size' in feature_group.text):
                        dictionary['Lot Size'] = feature_name.text
            except TypeError:
                pass
                # print(None)

                # if column_group

        #print('\n')

        list_of_feature_dictionary_entries.append(dictionary)
dataframe = pandas.DataFrame(list_of_feature_dictionary_entries)
dataframe.to_csv('Output_Crawl_Property_Data.csv')


# In[ ]:




