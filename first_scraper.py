from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uRequest

file_name = 'fsktm.csv'
f = open(file_name, 'w')
f.write('Title,Name,URL,Department,Phone Number,Email,Expertise\n')

inital_url = 'https://umexpert.um.edu.my/cv_search_page.php?selCat=01&txtname=&fak=C&dept=-&page_no={}'

for i in range(1, 10):
    # global str
    uClient = uRequest(inital_url.format(str(i)))
    temp_page = uClient.read()
    uClient.close()

    soup_page = soup(temp_page, "html.parser")
    containers = soup_page.findAll("table", {"style": "border:1px solid #CCC; border-bottom:"})
    for container in containers: 
        name = container.strong.a.text.strip()
        title = container.strong.find_next("br").next.strip()
        department = container.strong.find_next("br").next.next.next.strip().replace("\r\n                           ", "").replace(',', '.')
        
        try:
            phone_num = container.find("i", {"class": "fa fa-phone-square"}).next.replace("\xa0", "").replace(" ", "").replace("\t", "")
        except:
            print('Phone number error, {}'.format(name))

        try:
            email = container.find("i", {"class": "fa fa-envelope"}).next.replace("\xa0", "").replace(" ", "").replace("\t", "")
        except:
            print('Email error, {}'.format(name))

        expertises = []

        try:
            list_areas_of_expertise = container.find("div", {"class": "panel-body"}).children
            for a in list_areas_of_expertise:
                expertises.append(a)

            expertises = str(expertises[1]).replace(",", "-").replace(";", "-").replace("</li><li>", " || ")
            expertises = expertises.replace("<ul>", "").replace("</ul>", "")
            expertises = expertises.replace("<li>", "").replace("</li>", "")
            expertises = expertises.replace("\xa0", " ")
        except AttributeError:
            expertises = 'Error'
            print('AttributeError, {}'.format(name))
        #finally:
        #    f.close()

        #expertises = str(expertises[1]).replace(",", "-").replace(";", "-").replace("</li><li>", " || ")
        #expertises = expertises.replace("<ul>", "").replace("</ul>", "")
        #expertises = expertises.replace("<li>", "").replace("</li>", "")
        #expertises = expertises.replace("\xa0", " ")

        url = container.strong.a['href']

        f.write('{},{},{},{},{},{},{}\n'.format(title, name, url, department, phone_num, email, expertises))
        # f.write(title + ',' + name + ',' + department + ',' + phone_num + ',' + email + ',' + expertises + ',' + url)

f.close()