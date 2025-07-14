from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
from constants import race_ids, drivers, teams

def get_driver_career(name):
    res = requests.get(f"https://www.formula1.com/en/drivers/{name}")
    content = BeautifulSoup(res.content, "html.parser")
    name = content.find_all(attrs={"class":"typography-module_custom-cursive-medium-regular__NBmfU typography-module_lg_custom-cursive-large-regular__zsXue"})[0].text
    name += f' {content.find_all(attrs={"class":"typography-module_display-3-xl-black__CWhFe typography-module_lg_display-4-xl-black__zBSx5 Text-module_upper__pWFEw"})[0].text}'
    keys = content.find_all(attrs={"class":"DataGrid-module_title__hXN-n typography-module_body-xs-semibold__Fyfwn"})[16::]
    keys = [key.text for key in keys]
    values = content.find_all(attrs={"class":"DataGrid-module_description__e-Mnw typography-module_display-l-bold__m1yaJ typography-module_lg_display-xl-bold__4nIv1"})[16::]
    values = [value.text for value in values]
    infos = {}
    for index in range(len(keys)):
        infos[keys[index]] = {name:values[index]}
    return infos

def get_driver_season(name):
    res = requests.get(f"https://www.formula1.com/en/drivers/{name}")
    content = BeautifulSoup(res.content, "html.parser")
    name = content.find_all(attrs={"class":"typography-module_custom-cursive-medium-regular__NBmfU typography-module_lg_custom-cursive-large-regular__zsXue"})[0].text
    name += f' {content.find_all(attrs={"class":"typography-module_display-3-xl-black__CWhFe typography-module_lg_display-4-xl-black__zBSx5 Text-module_upper__pWFEw"})[0].text}'
    keys = content.find_all(attrs={"class":"DataGrid-module_title__hXN-n typography-module_body-xs-semibold__Fyfwn"})[:16:]
    keys = [key.text for key in keys]
    values = content.find_all(attrs={"class":"DataGrid-module_description__e-Mnw typography-module_display-l-bold__m1yaJ typography-module_lg_display-xl-bold__4nIv1"})[:16:]
    values = [value.text for value in values]
    infos = {}
    for index in range(len(keys)):
        infos[keys[index]] = {name:values[index]}
    return infos

def get_team_history(name):
    res = requests.get(f"https://www.formula1.com/en/teams/{name}")
    content = BeautifulSoup(res.content, "html.parser")
    keys = content.find_all(attrs={"class":"DataGrid-module_title__hXN-n typography-module_body-xs-semibold__Fyfwn"})[16:23:]
    keys = [key.text for key in keys]
    values = content.find_all(attrs={"class":"DataGrid-module_description__e-Mnw typography-module_display-l-bold__m1yaJ typography-module_lg_display-xl-bold__4nIv1"})
    values = values[16:23:]
    values = [value.text for value in values]
    infos = {}
    for index in range(len(keys)):
        infos[keys[index]] = {name:values[index]}
    return infos

def get_team_season(name):
    res = requests.get(f"https://www.formula1.com/en/teams/{name}")
    content = BeautifulSoup(res.content, "html.parser")
    keys = content.find_all(attrs={"class":"DataGrid-module_title__hXN-n typography-module_body-xs-semibold__Fyfwn"})
    aux_k = keys[:16:]
    aux_k.extend(keys[23::])
    keys = aux_k.copy()
    keys = [key.text for key in keys]
    keys.append("Drivers")
    values = content.find_all(attrs={"class":"DataGrid-module_description__e-Mnw typography-module_display-l-bold__m1yaJ typography-module_lg_display-xl-bold__4nIv1"})
    aux_v = values[:16:]
    aux_v.extend(values[23::])
    values = aux_v.copy()
    values = [value.text for value in values]
    driver_one = content.find_all(attrs={"class":"typography-module_display-l-regular__MOZq8 group-hover/driver-card:underline"})[0].text
    driver_one += f' {content.find_all(attrs={"class":"typography-module_display-l-bold__m1yaJ group-hover/driver-card:underline"})[0].text}'
    driver_two = content.find_all(attrs={"class":"typography-module_display-l-regular__MOZq8 group-hover/driver-card:underline"})[1].text
    driver_two += f' {content.find_all(attrs={"class":"typography-module_display-l-bold__m1yaJ group-hover/driver-card:underline"})[1].text}'
    names = content.find_all(attrs={"class":"f1-heading tracking-normal text-fs-18px leading-tight normal-case font-normal non-italic f1-heading__body font-formulaOne mt-xs"})
    names = f"{driver_one} / {driver_two}"
    values.append(names)
    infos = {}
    for index in range(len(keys)):
        infos[keys[index]] = {name:values[index]}
    return infos

def get_drivers_classification(year):
    res = requests.get(f"https://www.formula1.com/en/results/{year}/drivers")
    content = BeautifulSoup(res.content, "html.parser")
    positions = content.find_all(attrs={"class":"f1-text font-titillium tracking-normal font-normal non-italic normal-case leading-none f1-text__micro text-fs-15px"})
    classification = {}
    for index in range(0,len(positions),5):
        name = positions[index+1].find_all(attrs={"class":"max-lg:hidden"})[0].text
        name += f' {positions[index+1].find_all(attrs={"class":"max-md:hidden"})[0].text}'
        classification[name] = {"Position":int(positions[index].text),
                                "Country":positions[index+2].text,
                                "Car":positions[index+3].text,
                                "Points":positions[index+4].text}
    return classification

def get_teams_classification(year):
    res = requests.get(f"https://www.formula1.com/en/results/{year}/team")
    content = BeautifulSoup(res.content, "html.parser")
    positions = content.find_all(attrs={"class":"f1-text font-titillium tracking-normal font-normal non-italic normal-case leading-none f1-text__micro text-fs-15px"})
    classification = {}
    for index in range(0,len(positions),3):
        classification[positions[index+1].text] = {"Position":int(positions[index].text), "Points":positions[index+2].text}
    return classification

def get_race_winners(year):
    res = requests.get(f"https://www.formula1.com/en/results/{year}/races")
    content = BeautifulSoup(res.content, "html.parser")
    races = content.find_all(attrs={"class":"f1-text font-titillium tracking-normal font-normal non-italic normal-case leading-none f1-text__micro text-fs-15px"})
    winners = {}
    for index in range(0,len(races),6):
        name = races[index+2].find_all(attrs={"class":"max-lg:hidden"})[0].text
        name += f' {races[index+2].find_all(attrs={"class":"max-md:hidden"})[0].text}'
        winners[races[index].text] = {"Winner":name,
                                      "Date":races[index+1].text,
                                      "Car":races[index+3].text,
                                      "Laps":races[index+4].text,
                                      "Time":races[index+5].text}
    return winners

def get_race_result(gp, year, sprint=False):
    gp = gp.lower()
    key = f"{gp} {year}"
    if not sprint:
        res = requests.get(f"https://www.formula1.com/en/results/{year}/races/{race_ids[key]}/{gp}/race-result")
    else:
        res = requests.get(f"https://www.formula1.com/en/results/{year}/races/{race_ids[key]}/{gp}/sprint-results")
    content = BeautifulSoup(res.content, "html.parser")
    table = content.find_all(attrs={"class":"f1-table f1-table-with-data w-full"})[0]
    data = table.find_all(attrs={"class":"typography-module_body-s-semibold__O2lOH"})
    info = {}
    for index in range(0,len(data),7):
        name = data[index+2].find_all(attrs={"class":"max-lg:hidden"})[0].text
        name += f' {data[index+2].find_all(attrs={"class":"max-md:hidden"})[0].text}'
        info[data[index+1].text] = {"Position":data[index].text,
                                    "Driver":name,
                                    "Car":data[index+3].text,
                                    "Laps":data[index+4].text,
                                    "Time":data[index+5].text,
                                    "Points":data[index+6].text
                                    }
    return info

def get_race_fastest_laps(gp, year):
    gp = gp.lower()
    key = f"{gp} {year}"
    res = requests.get(f"https://www.formula1.com/en/results/{year}/races/{race_ids[key]}/{gp}/fastest-laps")
    content = BeautifulSoup(res.content, "html.parser")
    table = content.find_all(attrs={"class":"f1-table f1-table-with-data w-full"})[0]
    data = table.find_all(attrs={"class":"typography-module_body-s-semibold__O2lOH"})
    info = {}
    if int(year) < 1998:
        for index in range(0,len(data),6):
            name = data[index+2].find_all(attrs={"class":"max-lg:hidden"})[0].text
            name += f' {data[index+2].find_all(attrs={"class":"max-md:hidden"})[0].text}'
            info[data[index+1].text] = {"Position":data[index].text,
                                        "Driver":name,
                                        "Car":data[index+3].text,
                                        "Lap":data[index+4].text,
                                        "Time":data[index+5].text}
    elif int(year) < 2014:
        for index in range(0,len(data),7):
            name = data[index+2].find_all(attrs={"class":"max-lg:hidden"})[0].text
            name += f' {data[index+2].find_all(attrs={"class":"max-md:hidden"})[0].text}'
            info[data[index+1].text] = {"Position":data[index].text,
                                        "Driver":name,
                                        "Car":data[index+3].text,
                                        "Lap":data[index+4].text,
                                        "Time":data[index+5].text,
                                        "Avg Speed":data[index+6].text}
    else:
        for index in range(0,len(data),8):
            name = data[index+2].find_all(attrs={"class":"max-lg:hidden"})[0].text
            name += f' {data[index+2].find_all(attrs={"class":"max-md:hidden"})[0].text}'
            info[data[index+1].text] = {"Position":data[index].text,
                                        "Driver":name,
                                        "Car":data[index+3].text,
                                        "Lap":data[index+4].text,
                                        "Time":data[index+6].text,
                                        "Avg Speed":data[index+7].text,
                                        "Time of Day":data[index+5].text}
    return info

def get_starting_grid(gp, year, special_case=False, sprint=False):
    gp = gp.lower()
    key = f"{gp} {year}"
    if not sprint:
        res = requests.get(f"https://www.formula1.com/en/results/{year}/races/{race_ids[key]}/{gp}/starting-grid")
    else:
        res = requests.get(f"https://www.formula1.com/en/results/{year}/races/{race_ids[key]}/{gp}/sprint-grid")
    content = BeautifulSoup(res.content, "html.parser")
    table = content.find_all(attrs={"class":"f1-table f1-table-with-data w-full"})[0]
    data = table.find_all(attrs={"class":"typography-module_body-s-semibold__O2lOH"})
    info = {}
    if sprint or not special_case:
        for index in range(0,len(data),5):
            name = data[index+2].find_all(attrs={"class":"max-lg:hidden"})[0].text
            name += f' {data[index+2].find_all(attrs={"class":"max-md:hidden"})[0].text}'
            info[data[index+1].text] = {"Position":data[index].text,
                                        "Driver":name,
                                        "Car":data[index+3].text,
                                        "Time":data[index+4].text}
    else:
        for index in range(0,len(data),4):
            name = data[index+2].find_all(attrs={"class":"max-lg:hidden"})[0].text
            name += f' {data[index+2].find_all(attrs={"class":"max-md:hidden"})[0].text}'
            info[data[index+1].text] = {"Position":data[index].text,
                                        "Driver":name,
                                        "Car":data[index+3].text}
    return info

def get_sprint_grid(gp, year):
    gp = gp.lower()
    key = f"{gp} {year}"
    res = requests.get(f"https://www.formula1.com/en/results/{year}/races/{race_ids[key]}/{gp}/sprint-grid")
    content = BeautifulSoup(res.content, "html.parser")
    table = content.find_all(attrs={"class":"f1-table f1-table-with-data w-full"})[0]
    data = table.find_all(attrs={"class":"typography-module_body-s-semibold__O2lOH"})
    info = {}
    for index in range(0,len(data),5):
        name = data[index+2].find_all(attrs={"class":"max-lg:hidden"})[0].text
        name += f' {data[index+2].find_all(attrs={"class":"max-md:hidden"})[0].text}'
        info[data[index+1].text] = {"Position":data[index].text,
                                    "Driver":name,
                                    "Car":data[index+3].text,
                                    "Time":data[index+4].text}
    return info

def get_overall_qualifying(gp, year, sprint=False):
    gp = gp.lower()
    key = f"{gp} {year}"
    if int(year) < 2006:
        res = requests.get(f"https://www.formula1.com/en/results/{year}/races/{race_ids[key]}/{gp}/qualifying/0")
    elif int(year) >= 2006 and not sprint:
        res = requests.get(f"https://www.formula1.com/en/results/{year}/races/{race_ids[key]}/{gp}/qualifying")
    elif int(year) > 2020 and sprint:
        res = requests.get(f"https://www.formula1.com/en/results/{year}/races/{race_ids[key]}/{gp}/sprint-qualifying")
    content = BeautifulSoup(res.content, "html.parser")
    table = content.find_all(attrs={"class":"f1-table f1-table-with-data w-full"})[0]
    data = table.find_all(attrs={"class":"typography-module_body-s-semibold__O2lOH"})
    info = {}
    if int(year) < 1994:
        for index in range(0,len(data),5):
            name = data[index+2].find_all(attrs={"class":"max-lg:hidden"})[0].text
            name += f' {data[index+2].find_all(attrs={"class":"max-md:hidden"})[0].text}'
            info[data[index+1].text] = {"Position":data[index].text,
                                        "Driver":name,
                                        "Car":data[index+3].text,
                                        "Time":data[index+4].text}
    elif int(year) < 2006:
        for index in range(0,len(data),6):
            name = data[index+2].find_all(attrs={"class":"max-lg:hidden"})[0].text
            name += f' {data[index+2].find_all(attrs={"class":"max-md:hidden"})[0].text}'
            info[data[index+1].text] = {"Position":data[index].text,
                                        "Driver":name,
                                        "Car":data[index+3].text,
                                        "Time":data[index+4].text,
                                        "Laps":data[index+5].text}
    else:
        for index in range(0,len(data),8):
            name = data[index+2].find_all(attrs={"class":"max-lg:hidden"})[0].text
            name += f' {data[index+2].find_all(attrs={"class":"max-md:hidden"})[0].text}'
            info[data[index+1].text] = {"Position":data[index].text,
                                        "Driver":name,
                                        "Car":data[index+3].text,
                                        "Q1":data[index+4].text,
                                        "Q2":data[index+5].text,
                                        "Q3":data[index+6].text,
                                        "Laps":data[index+7].text}
    return info

def get_practice(gp, year, n):
    gp = gp.lower()
    key = f"{gp} {year}"
    res = requests.get(f"https://www.formula1.com/en/results/{year}/races/{race_ids[key]}/{gp}/practice/{n}")
    content = BeautifulSoup(res.content, "html.parser")
    table = content.find_all(attrs={"class":"f1-table f1-table-with-data w-full"})[0]
    data = table.find_all(attrs={"class":"typography-module_body-s-semibold__O2lOH"})
    info = {}
    if int(year) < 1994:
        for index in range(0,len(data),5):
            name = data[index+2].find_all(attrs={"class":"max-lg:hidden"})[0].text
            name += f' {data[index+2].find_all(attrs={"class":"max-md:hidden"})[0].text}'
            info[data[index+1].text] = {"Position":data[index].text,
                                        "Driver":name,
                                        "Car":data[index+3].text,
                                        "Time / Gap":data[index+4].text}
    else:
        for index in range(0,len(data),6):
            name = data[index+2].find_all(attrs={"class":"max-lg:hidden"})[0].text
            name += f' {data[index+2].find_all(attrs={"class":"max-md:hidden"})[0].text}'
            info[data[index+1].text] = {"Position":data[index].text,
                                        "Driver":name,
                                        "Car":data[index+3].text,
                                        "Time / Gap":data[index+4].text,
                                        "Laps":data[index+5].text}
    return info

def formatted_output(f, *args):
    data = f(*args)
    for d in data:
        print(f"{d}: {data[d]}")

def data_to_csv(data, file_path):
    if len(data.keys()) > 0:
        df = pd.DataFrame(data).T
        df.to_csv(file_path)

def get_data(race, folder="gps"):
    gp, year = race.split()
    year = int(year)
    folder_gp = f"{gp}_{year}"
    if folder_gp not in folder:
        os.makedirs(f"./{folder}/{folder_gp}", exist_ok=True)
        data_to_csv(get_race_result(gp, year), f"./{folder}/{folder_gp}/race.csv")
        if year > 2020:
            data_to_csv(get_race_result(gp, year, sprint=True), f"./{folder}/{folder_gp}/sprint.csv")
            data_to_csv(get_starting_grid(gp, year, sprint=True), f"./{folder}/{folder_gp}/sprint_grid.csv")
            data_to_csv(get_overall_qualifying(gp, year, sprint=True), f"./{folder}/{folder_gp}/sprint_qualifying.csv")
        data_to_csv(get_race_fastest_laps(gp, year), f"./{folder}/{folder_gp}/fastest_laps.csv")
        try:
            data_to_csv(get_starting_grid(gp, year), f"./{folder}/{folder_gp}/starting_grid.csv")
        except IndexError:
            data_to_csv(get_starting_grid(gp, year, special_case=True), f"./{folder}/{folder_gp}/starting_grid.csv")
        data_to_csv(get_overall_qualifying(gp, year), f"./{folder}/{folder_gp}/overall_qualifying.csv")
        if year > 1987:
            for index in range(1,5):
                data_to_csv(get_practice(gp, year, index), f"./{folder}/{folder_gp}/practice_{index}.csv")

def get_teams_data(folder="teams_stats"):
    for team in teams:
        os.makedirs(f"./{folder}/{team.replace('-','_')}", exist_ok=True)
        data_to_csv(get_team_history(team), f"./{folder}/{team.replace('-','_')}/{team.replace('-','_')}_history.csv")
        data_to_csv(get_team_season(team), f"./{folder}/{team.replace('-','_')}/{team.replace('-','_')}_season.csv")

def get_drivers_data(folder="drivers_stats"):
    for driver in drivers:
        os.makedirs(f"./{folder}/{driver.replace('-','_')}", exist_ok=True)
        data_to_csv(get_driver_career(driver), f"./{folder}/{driver.replace('-','_')}/{driver.replace('-','_')}_career.csv")
        data_to_csv(get_driver_season(driver), f"./{folder}/{driver.replace('-','_')}/{driver.replace('-','_')}_season.csv")