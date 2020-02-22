#!/usr/bin/env python
# coding: utf-8

# ## Assignment No:2
# ### Group Name: bobypie
# #### Group members: Nikita Pai and Abhilash Hemaraj
# 
# 

# ## Abstract
# 
# In this assignment, we work as a part of the company called Nerd Analytics that is incharge of handling databases. Throughout the asssignment we will go from data gathering, cleaning, to modelling conceptual ER diagrams and physical models. This can be achieved by process of Normalization wherein we decompose the original database into functional subsets that represent entity - relations.
# 

# ## Data and Data Cleaning and Data Auditing

# In[1]:


import pandas as pd
import numpy as np


# In[4]:


df = pd.read_csv("C:/Users/abhil/Downloads/amazon.csv")


# In[5]:


df.head()


# In[63]:


df1 = df.sample(n = 100)
df1


# In[64]:


df1.isnull().any()


# In[65]:


df1.isnull().sum()


# In[66]:


df1.dropna(axis = 0).info()


# In[67]:


df1 = df1.dropna(axis = 0)


# In[68]:


df1.info()


# In[69]:


s1 = df1.asins.str.split(',', expand=True).stack().str.strip().reset_index(level=1, drop=True)


# In[70]:


pd.unique(s1)


# In[72]:


s1 = pd.DataFrame(s1)


# In[73]:


df1


# In[74]:


df1


# In[75]:


df1.iloc[0]


# In[76]:


df1.loc


# In[78]:


final_csv1 = df1.to_csv(r'C:/Users/abhil/OneDrive/Desktop/dmdd/ass2B.csv')
final_csv1


# # Connecting jupyter notebook to mysql database

# In[16]:


import mysql.connector
from mysql.connector import Error


# In[7]:


import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password"
)

print(mydb)


# In[8]:


mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)


# In[10]:


import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="amazon"  
)

print(mydb)


# In[11]:


mycursor = mydb.cursor()


# In[12]:


mycursor


# In[18]:


#looking at the entire dataset at once

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM amazon.ass2b_revised")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)


# # Data Normalization
# ## 1NF

# It's a prominent database design technique wherein we divide tables into smaller tables and connect them via entity relationships.
# The main goal while performing data normalization is to reduce data redundancy and increase data integrity.

# The three essential steps to consider while deciding whether our data satisfies 1NF criteria are:
# 1) To check whether all records are unique:
# Herein all the rows reflect a particular order made by the customer that was fulfilled by the manufacturer. And hence each entry reflects a unique entry.
# 2) The values in each column of a table are atomic (No multi-value attributes allowed).
# Most of the attributes present where atomic i.e. single valued parameters. 'asins' turned out to be a multi valued attribute.
# which was formatted using str.split command in python
# 3) There are no repeating groups: two columns do not store similar information in the same table.
# There is no data redundancy and all columns represent unique information.(It may look like that brand and manufacturer table present same information but its just because that the mode of the subsetted data conatins similar values but are two different attributes.
# Hence the data satisfies 1NF criteria

# In[6]:


NF1 = pd.read_csv("C:/Users/abhil/OneDrive/Desktop/dmdd/ass2B_revised.csv")


# In[7]:


NF1.head()


# ## 2NF

# Problems faced in the first normal form include Insertion anomaly, deletion and modification anomaly.
# Insertion anomaly: We won't be able to add new information about the user/customer unless the customer places an order. it occurs because there is more than one entity in the table.
# Deletion anomaly: if the customer cancels the order he once place we would lose entire information of the transaction since the table in 1NF is completely dependent on the data after the order has been placed. Cancelled/deleted orders will result in us losing the data related t the user as well.
# Modification Anomaly: problem arises when we need to update the data but unable to because of presence of multiple entities.
# 
# The three essential steps to consider while deciding whether our data satisfies 2NF criteria are:
# 1) All requirements for 1st NF must be met.
# We have already achieved 1NF criteria
# 
# 2) No partial dependencies.
# Having a closer look at the data, attributes such as Product Id, asins(Amazon Standard Identification number), category, key and name doesnot have a direct relation to the Order No. We would be extracting these columns into a new entity called Product.
# 
# 3) No calculated data.
# The columns present in the dataset doesnot include any calculated data.

# In[31]:


Order = NF1.drop(['asins', 'categories', 'keys'], axis = 1)


# In[40]:


Product = NF1[['Product Id', 'asins', 'categories', 'keys']]


# In[41]:


Product.drop_duplicates(keep='first')


# In[42]:


Product = Product.drop_duplicates(keep='first').reset_index(drop=True)


# In[43]:


Order.head()
Product.head()


# ## 3NF

# The theoretical definition of third normal form says:
# 1) The relation is in second normal form.
# 2) There are no transitive dependencies.
# Removing the transitive dependicies between the entity user and entity order.

# In[33]:


Order = Order.drop(['reviews.sourceURLs', 'reviews.date', 'reviews.title','reviews.text', 'rating'], axis = 1)
User = NF1[['reviews.sourceURLs','reviews.username', 'reviews.date', 'reviews.title','reviews.text', 'rating']]


# In[47]:


Order = Order.drop(['name','brand', 'manufacturer'], axis = 1)
Order.head()


# In[35]:


User.head()


# In[44]:


Product.head()


# ## Conceptual ER Diagram

# In[39]:


from IPython.display import Image
Image("C:/Users/abhil/OneDrive/Pictures/assignment_2_conceptual_er.png")


# ### PHYSICAL MODEL

# In[1]:


from IPython.display import Image
Image("C:/Users/paini/OneDrive/Desktop/dmdd/assignnment 2/physical model.png")

Questions you must answer about your physical model:
1. Are all the tables in 1NF?

The dataset is a list of consumer reviews for Amazon products like the Kindle, Fire TV Stick, and more provided by Datafiniti's Product Database. The dataset includes basic product information, rating, review text, and more for each product. It has entities that represent consumers, producer as implied by product ID and company that takes Order.
It satisfies the condition that comprises of 1NF as all the values are atomic and non-repetitive at every intersection of row and column. The dataset also has a primary key and candidate key(which in future shall become foreign key) that can used to comceptual model.

2. Are all the tables in 2NF?

Yes. The second step involved branching out the attributes that were dependent on the candidate key(Product ID). Hence, the Product ID becomes foreign key in Table 1. The others columns that are dependent on Product ID are branched out as well(ASIN, Category, keys) hence leaving no sign for partial dependency. There is calculated data in the dataset either.

3. Are all the tables in 3NF?

Yes. The reviews are based on product assesment by the customer. The customer(B) evaluates the product(A) and gives reviews(C). Since, A -> B and B-> C which inturn gives A -> C, the dataset showed an indication of transitive dependency. The following was eliminated using 3NF table format, wherein a new table of Customer Reviews is created with entities like SourceURL(PID), Title, Text, Date AND rating. By eliminating fields that do not directly depend on the primary key, we have satisfied the condition for the same. 
# ## UML Diagram

# In[45]:


from IPython.display import Image
Image("C:/Users/abhil/OneDrive/Pictures/uml.png")


# ## Questions you must answer about your conceptual model:
# 
1) What are the ranges, data types and format of all of the attributes in your entities?

We classified attributes in our entities in the following category base on SQL data types:-

Numeric data types such as int, tinyint, bigint, float, real etc.
Date and Time data types such as Date, Time, Datetime etc.
Character and String data types such as char, varchar, text etc.
Unicode character string data types, for example nchar, nvarchar, ntext etc.

Based on that our attributes are given in the following type:
Attributes: Data type/ Format/ Range
Order No:   Int/ Numeric/0-30
Product Id: NVarChar/Unicode Character/0-30
Username:   String/Character/0-30
ASIN:       NVarChar/Unicode Character/0-30
Categories: String/Character/0-30
Keys:       NVarChar/Unicode String/0-30
Date:       DateTime/YYYY-MM-DD-TT/0-30
Rating:     Int/Number/0-1
SourceURL:  NVarChar/Unicode Character/0-100
text:       text/Character/0-200
Title:      String/String/0-50

2) When should you use an entity versus attribute? (Example: address of a person could be modeled as either)
Entities can be tangible and non tangible objects; if more than one attributes describes a particualar object then we can consider it as an entity and also define its relation. In the current database model we have clear entity - realtionship themes as in Order, Product and Consumer. We achieved this by correctly modelling the attributes explaining the entities and achieved the respective relationships.


3) When should you use an entity or relationship, and placement of attributes? (Example: a manager could be modeled as either)
Modelling real world datasets can lead to formation of something called as Weak Entities and Strong Entities. When there is no primary key attribute that can uniquely identify the entries in the entity table then that entity is referred to as Weak Entity. ANd vice versa for Strong entities. In our case all the keys turned out to be unique and hence leading to strong entities.

4) How did you choose your keys? Which are unique?
Our dataset exhibits various orders by different users andalso their feedback. Choosing an entity with a unique primary key was paramount to establish strong entities. As it turned out we came up with three entities with three different keys. The product id coulmn though had repeating entries but it was possible through simple data wrangling techniques to gain unique entries for product id.


5) Did you model hierarchies using the “ISA” design element? Why or why not?
We did not model hierarchies using the "ISA" design element; because there were no overlapping constraints; And it was pretty straight forward for us to model the ER diagram and understand the relationships from them. Hence we stuck to the basic constructs like entity, relationships, attributes.


6) Were there design alternatives? What are their tradeoffs: entity vs. attribute, entity vs. relationship, binary vs. ternary relationships?
Some of the tradeoffs we had to make include: entity vs attribute wehrein it was decided that the User reviews be a different entity rather than it being an attribute since what if the user decided to change/modify his review? in that case the reviews had to be an entity since it needed to hold multi valued attributes.

7) Where are you going to find real-world data to populate your model?
We got the real world data from kaggle or we would need to scrape the amazon website.
# ### CONCLUSION
# The main focus of this assessment was to understand process of normalization. Database normalization is the process of organizing the attributes and tables of a relational database to
# minimize data redundancy.
# Normalization involves refactoring a table into smaller (and less redundant) tables but without losing
# information; defining foreign keys in the old table referencing the primary keys of the new ones. The
# objective is to isolate data so that additions, deletions, and modifications of an attribute can be made in
# just one table and then propagated through the rest of the database using the defined foreign keys.

# ### Contribution
# 
# Nikita Pai: 30%
# Abhilash Hemaraj: 30%
# External: 15% 
# TA: 5%
# Professor: 10%
Portfolio(Github Link)
https://github.com/Nikita199511
https://github.com/AbhilashHemaraj/
# ### CITATION
https://www.kaggle.com/datafiniti/consumer-reviews-of-amazon-products
https://www.oreilly.com/library/view/relational-database-design/9780128499023/Copyright 2019 NIKITA PAI & ABHILASH HEMARAJ

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the 
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.