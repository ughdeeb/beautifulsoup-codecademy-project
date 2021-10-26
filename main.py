from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Requests the raw HTML from the site
webpage = requests.get('https://content.codecademy.com/courses/beautifulsoup/cacao/index.html')


# Creates BeautifulSoup object that will traverse the HTML
soup = BeautifulSoup(webpage.content, "html.parser")

# -- START Making a historgram of the ratings data--
# Pull all ratings into a list
ratings = soup.find_all(attrs = {
  "class" : "Rating"
})

# Pull all ratings into a list
ratings_list = []

#append to ratings_list each rating from ratings and convert the values to float and start at element 1 of the list since it has the word "Rating"
for rating in ratings[1:]:
  ratings_list.append(float(rating.get_text()))

# print(ratings_list)
# print(ratings)

#use Matplotlib to create a histogram of ratings_list
plt.hist(ratings_list)
plt.show()

# END -- Making a historgram of the ratings data--

#Find top 10 highest rated cholatier companies
#    alt method:
# company_tags = soup.find_all(attrs = {
#   "class": "Company"
# })

company_tags = soup.select(".Company")
company_names = []
for company in company_tags[1:]:
  company_names.append(company.get_text())

# print(company_tags)
# print(company_names)

# #creates dictionary 
# company_rating = {"Company": company_names, "Rating": ratings_list}
# #creates dataframe 
# company_rating_df = pd.DataFrame.from_dict(company_rating)
# # print(company_rating_df)

# #creates dataframe of top 10
# mean_ratings = company_rating_df.groupby("Company").Rating.mean()
# top_ten = mean_ratings.nlargest(10)
# # print(top_ten)

#scrape cocoa perecent ratings
cocoa_percent_tags = soup.select(".CocoaPercent")
cocoa_percents = []

for cocoa_percentage in cocoa_percent_tags[1:]:
  cocoa_percents.append(float(cocoa_percentage.get_text().strip("%")))
# print(cocoa_percents)

#create add columns to dataframe
company_rating = {"Company": company_names, "Rating": ratings_list, "CocoaPercentage": cocoa_percents}
company_rating_df = pd.DataFrame.from_dict(company_rating)
# print(company_rating_df)

#make scatterplot of ratings vs cocoa percentage
plt.scatter(company_rating_df.CocoaPercentage, company_rating_df.Rating)

z = np.polyfit(company_rating_df.CocoaPercentage, company_rating_df.Rating, 1)
line_function = np.poly1d(z)
plt.plot(company_rating_df.CocoaPercentage, line_function(company_rating_df.CocoaPercentage), "r--")

plt.show()
plt.clf()
