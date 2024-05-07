import dicos
from bs4 import BeautifulSoup
import requests
from athlete import Athlete
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

annee = "2024"
sexe = "M"
categorie = "CA"
epreuve = "110"
outdoor = True
page = "0"
vent = "VR"

dicos.LISTE_ATHLETES = []

url = f"https://bases.athle.fr/asp.net/liste.aspx?frmpostback=true&frmbase=bilans&frmmode=1&frmespace=0&frmannee={annee}&frmathlerama=&frmfcompetition=&frmfepreuve=&frmepreuve={epreuve}&frmplaces=&frmnationalite=&frmamini=&frmamaxi=&frmsexe={sexe}&frmcategorie={categorie}&frmvent={vent}"


# url = "https://bases.athle.fr/asp.net/liste.aspx?frmpostback=true&frmbase=bilans&frmmode=1&frmespace=0&frmannee=2024&frmathlerama=&frmfcompetition=&frmfepreuve=&frmepreuve=110&frmplaces=&frmnationalite=&frmamini=&frmamaxi=&frmsexe=M&frmcategorie=&frmvent=VR"

def get_soup(url, page):
    response = requests.get(url)
    print("Get_soup : " + str(response.status_code))

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Trouver la table qui contient les informations
        table = soup.find('table', {'id': 'ctnBilans'})
        return table


def get_pages(url):
    response = requests.get(url)
    print("Get_pages : " + str(response.status_code))

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Trouver la table qui contient les informations
        table = soup.find('table', {'id': 'ctnBilans'})
        select = soup.find('select', {'class': 'barSelect'})
        select2 = soup.find('td', {'class': 'barInputs'})

        if select2:
            barres = select2.find_all('select')
            print("Barres : " + str(len(barres)))
            if len(barres) == 2:
                print("Select " + str(len(select)))
                pages = select.find_all('option')
                print("Nombre de pages : " + str(len(pages)))
                return str(len(pages))
            else:
                return "1"

        # if select:
        # print("Select " + str(len(select)))
        # pages = select.find_all('option')
        # print("Nombre de pages : " + str(len(pages)))
        # return str(len(pages))


def extract_data_from_page(url):
    print("extract_data_from_page : " + url)
    response = requests.get(url)
    print(response.status_code)
    pages = get_pages(url)
    print("pages" + str(pages))
    p = 0
    page = "0"
    print("Epreuve" + epreuve)
    while p < (int(pages)):
        fixed_url = url + f"&frmposition={page}"
        print("Début boucle : " + fixed_url)
        if response.status_code == 200:
            table = get_soup(fixed_url, page)
            print("page : " + page)
            if table and (epreuve != "710" and epreuve != "810" and epreuve != "840" and epreuve != "296"):
                rows = table.find_all('tr')
                for row in rows[2:]:  # Ignore la première ligne qui contient les en-têtes
                    columns = row.find_all('td')
                    print("Columns" + str(len(columns)))
                    athlete = Athlete()
                    classement = columns[0].text.strip()
                    athlete.classement = classement
                    vide_1 = columns[1].text.strip()
                    chrono = columns[2].text.strip()
                    athlete.chrono = chrono
                    vide_2 = columns[3].text.strip()
                    vide_3 = columns[4].text.strip()
                    vide_4 = columns[5].text.strip()
                    nom_athlete = columns[6].text.strip()
                    athlete.nom = nom_athlete
                    vide_5 = columns[7].text.strip()
                    club = columns[8].text.strip()
                    athlete.club = club
                    vide_6 = columns[9].text.strip()
                    region = columns[10].text.strip()
                    athlete.region = region
                    vide_7 = columns[11].text.strip()
                    departement = columns[12].text.strip()
                    athlete.departement = departement
                    vide_8 = columns[13].text.strip()
                    categorie = columns[14].text.strip()
                    athlete.categorie = categorie
                    vide_9 = columns[15].text.strip()
                    annee_naissance = columns[16].text.strip()
                    athlete.annee_naissance = annee_naissance
                    vide_10 = columns[17].text.strip()
                    date_performance = columns[18].text.strip()
                    athlete.date_perf = date_performance
                    vide_11 = columns[19].text.strip()
                    lieu_performance = columns[20].text.strip()
                    athlete.lieu_perf = lieu_performance

                    # print(type(athlete))
                    dicos.LISTE_ATHLETES.append(athlete)
            else:
                print("Pas de données disponibles")
                break

                # print("Classement:", classement)
                # print("Chrono:", chrono)
                # print("Nom de l'athlète:", nom_athlete)
                # print("Club:", club)
                # print("Région:", region)
                # print("Département:", departement)
                # print("Catégorie:", categorie)
                # print("Année de naissance:", annee_naissance)
                # print("Date de la performance:", date_performance)
                # print("Lieu de la performance:",lieu_performance)
                # print("---------------------------------------------")

        else:
            print("La requête a échoué. Code de statut :", response.status_code)
            return None

        p += 1
        (print("P : " + str(p)))
        page = str(p)

        for athlete in dicos.LISTE_ATHLETES:
            print("Classement :" + athlete.classement + " - Nom : " + athlete.nom + " - Chrono : " + athlete.chrono)


# extract_data_from_page(url)

print("liste d'athletes : " + str(len(dicos.LISTE_ATHLETES)))
print(type(dicos.LISTE_ATHLETES))
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")
print("----------------------------------- TEST LISTE ATHLETES ------------------------------------")
for athlete in dicos.LISTE_ATHLETES:
    print(athlete.classement + " - " + athlete.nom + " : " + athlete.chrono)

ctk.set_appearance_mode("System")

ctk.set_default_color_theme("green")

window = tk.Tk()

window.title("Athlete App")
window.geometry("1024x768")


def combobox_callback(choice):
    print(choice)


yearLabel = ctk.CTkLabel(window, text="Année")
yearLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
year_string = tk.StringVar(value=dicos.liste_annee[4])
yearChoice = ttk.Combobox(window, values=dicos.liste_annee, textvariable=year_string)
yearChoice.bind('<<ComboboxSelected>>', lambda event: combobox_callback(year_string.get()))
yearChoice.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

sexlabel = ctk.CTkLabel(window, text="Sexe")
sexlabel.grid(row=0, column=2, padx=20, pady=20, sticky="ew")
sex_string = tk.StringVar(value=dicos.liste_sexe[0])
sexChoice = ttk.Combobox(window, values=dicos.liste_sexe, textvariable=sex_string)
sexChoice.bind('<<ComboboxSelected>>', lambda event: combobox_callback(sex_string.get()))
sexChoice.grid(row=0, column=3, padx=20, pady=20, sticky="ew")

categorieLabel = ctk.CTkLabel(window, text="Catégorie")
categorieLabel.grid(row=0, column=4, padx=20, pady=20, sticky="ew")
cate_string = tk.StringVar(value=dicos.liste_categorie[0])
categorieChoice = ttk.Combobox(window, values=dicos.liste_categorie, textvariable=cate_string)
categorieChoice.bind('<<ComboboxSelected>>', lambda event: combobox_callback(cate_string.get()))
categorieChoice.grid(row=0, column=5, padx=20, pady=20, sticky="ew")

typeCompetitionLabel = ctk.CTkLabel(window, text="Type")
typeCompetitionLabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
type_comp_string = tk.StringVar(value=dicos.liste_In_Out[0])
typeCompetitionChoice = ttk.Combobox(window, values=dicos.liste_In_Out, textvariable=type_comp_string)
typeCompetitionChoice.bind('<<ComboboxSelected>>', lambda event: combobox_callback(type_comp_string.get()))
typeCompetitionChoice.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

epreuveLabel = ctk.CTkLabel(window, text="Epreuve")
epreuveLabel.grid(row=1, column=2, padx=20, pady=20, sticky="ew")
epreuve_string = tk.StringVar(value=dicos.liste_epreuves_outdoor[0])
epreuveChoice = ttk.Combobox(window, values=dicos.liste_epreuves_outdoor, textvariable=epreuve_string)
epreuveChoice.bind('<<ComboboxSelected>>', lambda event: combobox_callback(epreuve_string.get()))
epreuveChoice.grid(row=1, column=3, padx=20, pady=20, sticky="ew")

# data
annee = year_string.get()
# sexe = sex_string.get()
# categorie = cate_string.get()
# epreuve = epreuve_string.get()
url_final = f"https://bases.athle.fr/asp.net/liste.aspx?frmpostback=true&frmbase=bilans&frmmode=1&frmespace=0&frmannee={annee}&frmathlerama=&frmfcompetition=&frmfepreuve=&frmepreuve={epreuve}&frmplaces=&frmnationalite=&frmamini=&frmamaxi=&frmsexe={sexe}&frmcategorie={categorie}&frmvent={vent}"


def clic_url(url, annee, epreuve, categorie, sexe):
    print("Année cliquée" + annee)
    print("Epreuve cliquée" + epreuve)
    print("Catégorie cliquée" + categorie)
    print("Sexe cliquée" + sexe)
    url = f"https://bases.athle.fr/asp.net/liste.aspx?frmpostback=true&frmbase=bilans&frmmode=1&frmespace=0&frmannee={annee}&frmathlerama=&frmfcompetition=&frmfepreuve=&frmepreuve={epreuve}&frmplaces=&frmnationalite=&frmamini=&frmamaxi=&frmsexe={sexe}&frmcategorie={categorie}&frmvent={vent}"
    url_final = url
    print("clic_url " + url_final)
    return url_final


def correspondance(choice, dicos):
    for key, value in dicos.items():
        if choice == key:
            print(value)
            return value


def display(liste):
    for athlete in liste:
        tk_textbox.insert(window, athlete.classement + " " + athlete.chrono + " " + athlete.nom)


url = f"https://bases.athle.fr/asp.net/liste.aspx?frmpostback=true&frmbase=bilans&frmmode=1&frmespace=0&frmannee={annee}&frmathlerama=&frmfcompetition=&frmfepreuve=&frmepreuve={epreuve}&frmplaces=&frmnationalite=&frmamini=&frmamaxi=&frmsexe={sexe}&frmcategorie={categorie}&frmvent={vent}"
url_final = clic_url(url_final, year_string.get(), correspondance(epreuve_string.get(), dicos.dico_epreuves_outdoor),
                     correspondance(cate_string.get(), dicos.dico_categories),
                     correspondance(sex_string.get(), dicos.dico_sexes))
print("Final A : " + url_final)
btn = ctk.CTkButton(window, text="Url a créer",
                    command=lambda: print(
                        f"Command button : {clic_url(url_final, year_string.get(), correspondance(epreuve_string.get(), dicos.dico_epreuves_outdoor), correspondance(cate_string.get(), dicos.dico_categories), correspondance(sex_string.get(), dicos.dico_sexes))}"),
                    border_width=2,
                    corner_radius=5)
# command = lambda: [extract_data_from_page(url), print(    f'{year_string.get()} / {sex_string.get()} / {cate_string.get()} / {type_comp_string.get()} / {epreuve_string.get()}'),print(f"Url btn : {url}")],

# btn.bind("<Button>", lambda event: clic_url(url, annee))
btn.grid(row=2, column=2, columnspan=2, padx=20, pady=20, sticky="ew")
print("Final B : " + url_final)
url_string = url_final
label_url = tk.Label(window, text='url', textvariable=url_string)
label_url.grid(row=3, column=2, columnspan=2, padx=20, pady=20, sticky="ew")
btn_envoi = ctk.CTkButton(window, text="Envoi", command=lambda: extract_data_from_page(
    clic_url(url_final, year_string.get(), correspondance(epreuve_string.get(), dicos.dico_epreuves_outdoor),
             correspondance(cate_string.get(), dicos.dico_categories),
             correspondance(sex_string.get(), dicos.dico_sexes))))
btn_envoi.grid(row=4, column=2, columnspan=2, padx=20, pady=20, sticky="ew")

btn_display = ctk.CTkButton(window, text="Display", command=display(dicos.LISTE_ATHLETES))
btn_display.grid(row=5, column=2, columnspan=2, padx=20, pady=20, sticky="ew")

# create scrollable textbox
tk_textbox = tk.Text(window, highlightthickness=0)
tk_textbox.grid(row=6, column=1, sticky="nsew")

# create CTk scrollbar
ctk_textbox_scrollbar = ctk.CTkScrollbar(window, command=tk_textbox.yview)
ctk_textbox_scrollbar.grid(row=6, column=2, columnspan=1, sticky="ns")

# connect textbox scroll event to CTk scrollbar
tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

window.mainloop()
