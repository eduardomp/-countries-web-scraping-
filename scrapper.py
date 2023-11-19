import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import pandas as pd 

REGEX_GDP = '\$[.0-9]*\s{,1}[a-zA-Z]*'
REGEX_NUMBER = '^[0-9,]*'
csv_rows = []

def get_sibling_td_from_th_text(table,cell_titles):
    td = None
    ths = table.find_all("th")
    for cell_title in cell_titles:
        for th in ths:
            text = th.get_text(strip=True)
            cell_title_lowercase = ''.join(cell_title.split()).lower()
            text_lowercase = ''.join(text.split()).lower()
            if text_lowercase.find(cell_title_lowercase) > -1:
                td = th.next_sibling
                break

        if td is not None:
            break

    return td

def get_near_tr_data_from_reference(table, ref_tag, ref_text,index_increment):
    target_tr = None
    trs = table.find_all("tr")

    for i, tr in enumerate(trs):
        tag = tr.find(ref_tag)
        if tag and tag.get_text(strip=True) == ref_text:
            target_tr = trs[i+index_increment]
            if target_tr:
                break

    return target_tr

def get_tr_data_from_reference_regex_filter(table, ref_tag, ref_text,index_increment, regex):
    target_tr = get_near_tr_data_from_reference(table, ref_tag, ref_text, index_increment)
    data = target_tr.find("td", class_="infobox-data") if target_tr else None
    return re.findall(regex, data.get_text(strip=True))[0] if data else ""

def get_area(table):
    return get_tr_data_from_reference_regex_filter(table, 'a', 'Area',1, REGEX_NUMBER)

def get_population(table):
    return get_tr_data_from_reference_regex_filter(table, 'a', 'Population',1, REGEX_NUMBER)

def get_gdp_korea(soup):
    wikitable = soup.find('table', class_ = "wikitable")
    rows = wikitable.find_all('tr')
    target_row = rows[11]
    tds = target_row.find_all('td')
    target_td = tds[2]
    return re.findall(REGEX_GDP, target_td.get_text(strip=True))[0] if target_td else ""

def get_gdp(table, country, soup):
    if country == "Korea":
        return get_gdp_korea(soup)
    return get_tr_data_from_reference_regex_filter(table, 'a', 'GDP',1, REGEX_GDP)

def get_highest_population_area_gdp(df):
    print(df.groupby(['Population', 'Area', 'GDP']).max())
    selected_country = df.groupby(['Population', 'Area', 'GDP']).max()['Country Name'].iloc[0]
    print(f"\nThe country with the highest population, area, and GDP is:\n\t - {selected_country} \n")

def save_html(country,soup):
    with open(f"./html/{country}.html", "w") as file:
        file.write(str(soup))

with open('link.txt') as f:
    for line in f:
        country = line.split(",")[0]
        url = line.split(",")[1]

        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        #Assignemt 3 - save these source files (*.html) in a dedicated folder on your laptop.
        save_html(country, soup)

        country_name = soup.find_all("div", class_="country-name")[0].string
        
        table = soup.find("table", {"class": ["infobox", "ib-country", "vcard"]})
        
        capital_td = get_sibling_td_from_th_text(table,["Capital"])
        capital = capital_td.a.get_text(strip=True)

        possible_laguage_labels = ["National language","Official languages","Official language","Native languages"]
        native_languages_td = get_sibling_td_from_th_text(table, possible_laguage_labels)
        native_languages = [l.string for l in native_languages_td.find_all('a')] if native_languages_td else None

        area = get_area(table)

        population = get_population(table)

        gdp = get_gdp(table, country, soup)

        print(f"Data extracted: {country_name} - {capital} - {native_languages[0]} - {area} km2 - Population {population} - GDP {gdp}")

        gdp = re.sub(r'[^0-9]', '', gdp)
        area = re.sub(r'[^0-9]', '', area)
        population = re.sub(r'[^0-9]', '', population)

        csv_rows.append([country_name, capital, native_languages[0], float(area), float(population), float(gdp)])

    print("----------------------------------------------------------------------------------")
    df = pd.DataFrame(csv_rows, columns=['Country Name', 'Capital', 'Language', 'Area', 'Population', 'GDP'])
    
    print("Generating csv... \n")
    df.to_csv("countries.csv")

    print("Generating xlsx... \n")
    df.to_excel('countries.xlsx', sheet_name='Countries', index=False)

    print("----------------------------------------------------------------------------------")
    get_highest_population_area_gdp(df)

    print("----------------------------------------------------------------------------------")
    print("\nPearson correlation (area, population):\n")
    df_area_pop = df.copy()
    df_area_pop.drop(["Country Name","Capital","Language","GDP"], inplace=True, axis=1)
    print(df_area_pop.corr(method='pearson'))

    print("----------------------------------------------------------------------------------")
    print("\nPearson correlation (area, gdp):\n")
    df_area_gpd = df.copy()
    df_area_gpd.drop(["Country Name","Capital","Language","Population"], inplace=True, axis=1)
    print(df_area_gpd.corr(method='pearson'))

    print("----------------------------------------------------------------------------------")
    print("\nPearson correlation (population, gdp):\n")
    df_pop_gdp = df.copy()
    df_pop_gdp.drop(["Country Name","Capital","Language","Area"], inplace=True, axis=1)
    print(df_pop_gdp.corr(method='pearson'))

    print("Done!")