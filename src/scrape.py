from bs4 import BeautifulSoup
import requests
import re
from csv import writer
s = requests.Session()
with open('providers.csv', 'w', encoding = 'utf8', newline = '') as f:
    thewriter =writer(f)
    header = ['Full Name', 'Speciality', 'Add_speciality', 'practice', 'Full Address', 'City', 'State', 'Zip', 'phone', 'Url']
    thewriter.writerow(header)

    def index_in_list(a_list, index):
        return (index < len(a_list))

    for i in range(1,38):
        form_data= {
                "PhysicianSearch$FTR01$PagingID": i
            }
        
        baseurl="https://www.stfrancismedicalcenter.com"
        url = "https://www.stfrancismedicalcenter.com/find-a-provider/"

        print(form_data)
        page = s.post(url,  data=form_data)
        providerslink=[]

        soup = BeautifulSoup(page.content, "html.parser")
        providers_lists = soup.find_all('li', class_="half")
        for list in providers_lists:
            for link in list.find_all('a', class_="flex-top-between-block-500"):
                if link['href']:
                    pass
                else:
                    continue
                providerslink.append(baseurl + link['href'])

        for link in providerslink:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, "html.parser")
            
            full_Name = soup.find('h1', class_="hide-1024").text.strip() if soup.find('h1', class_="hide-1024") else " "
            Speciality = soup.find('div', class_="two-thirds").text.strip() if soup.find('div', class_="two-thirds") else " "
            
            regex = re.compile('.*AdditionalPhysicianSpecialties*')
            
            Add_speciality = soup.find('li', {"id" : regex}).find('span').text.strip() if soup.find('li', {"id" : regex})  else " "
            
            
            Full_Address = soup.address.text.strip() if soup.address else " "
            Add_list = soup.address.get_text(strip=True, separator='\n').splitlines()
            if index_in_list(Add_list, 1):
                Add_list1 = Add_list[1].split(",")
                city = Add_list1[0] if index_in_list(Add_list1, 0) else " "
                state_zip = Add_list1[1].strip().split(" ") if index_in_list(Add_list1, 1) else " "
                state = state_zip[0]
                zip = state_zip[1] if index_in_list(state_zip, 1) else " "
                phone = soup.address.a.text if soup.address.a else " "
            else:
                city = " "
                state = " "
                zip = " "
                phone = " "
            
            practice = soup.find('strong', class_="title-style-5").text.strip() if soup.find('strong', class_="title-style-5") else " "

            # print(f"Full Name : {full_Name}")
            # print(f"Speciality : {Speciality}")
            # print(f"Add_speciality : {Add_speciality}")
            # print(f"practice : {practice}")
            # print(f"Full Address : {Full_Address}")
            # print(f"City : {city}")
            # print(f"State : {state}")
            # print(f"Zip : {zip}")
            # print(f"phone : {phone}")
            # print(f"Url : {link}")
            info = [full_Name, Speciality, Add_speciality, practice, Full_Address,city, state, zip, phone, link]
            thewriter.writerow(info)



            



            
