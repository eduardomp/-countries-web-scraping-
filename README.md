# Setup

```shell
# create a virtual environment (to isolate your libraries)
python3 -m venv venv

# activate virtual environment "venv"
source venv/bin/activate

# install libraries
pip install --upgrade pip
pip install -r requirements.txt

# you can exit venv using the command
deactivate

```

# To run the scrapper, create index and test the search algorithms 

After setup, you need to run the scripts in the following order to check the results

 ```
# will scrap data from wikipedia, reading links from a local txt file, create local html files and export data in csv and xlsx 
python scrapper.py

#create the inverse index file
python create_index.py

# show the outputs of the functions country_search(keyword) and fuzzy_search(keyword)  
python search.py toronto

#or

python search.py toronta

 ```
