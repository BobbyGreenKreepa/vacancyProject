import json

import numpy as np
import pandas as pd

from CentralBankService import CentralBankService


def get_data_frame(df: pd.DataFrame) -> pd.DataFrame:
    central_bank_service = CentralBankService()
    df["salary"] = df[['salary_from', 'salary_to']].mean(axis=1)
    df["salary"] = df.apply(
        lambda row: np.nan if pd.isnull(row["salary_currency"]) else
        row["salary"] * central_bank_service.get_rubles(str(row["salary_currency"]), str(row["published_at"])), axis=1
    )
    df = df.drop(df[df["salary"] >= 10000000.0].index)
    df["published_year"] = pd.to_datetime(df["published_at"], utc=True).dt.year
    return df


def print_demand_data(df: pd.DataFrame):
    print_salary_dynamics(df)
    print_vacancies_dynamics(df)
    print_profession_salary_dynamics(df)
    print_profession_vacancies_dynamics(df)

def print_salary_dynamics(df: pd.DataFrame):
    title = "Динамика уровня зарплат по годам"
    salary_to_year = df.groupby("published_year")["salary"].mean().astype(int).to_dict()
    print(f"{title}: {json.dumps(salary_to_year)}")

def print_vacancies_dynamics(df: pd.DataFrame):
    vacancies_dynamics = df['published_year'].value_counts().sort_index().astype(int).to_dict()
    print(f"Динамика количества вакансий по годам: {json.dumps(vacancies_dynamics)}")

def print_profession_salary_dynamics(df: pd.DataFrame, profession_name: str):
    data_prof = df[df['name'].str.contains(profession_name, case=False, na=False)]
    prof_salaries_dynamics = data_prof.groupby("published_year")["salary"].mean().astype(int).to_dict()
    print(f"Динамика зарплат по годам для выбранной профессии: {json.dumps(prof_salaries_dynamics)}")

def print_profession_vacancies_dynamics(df: pd.DataFrame, profession_name: str):
    data_prof = df[df['name'].str.contains(profession_name, case=False, na=False)]
    prof_vacancies_dynamics = data_prof["published_year"].value_counts().sort_index().astype(int).to_dict()
    print(f"Доля вакансий по годам для выбранной профессии {json.dumps(prof_vacancies_dynamics)}")


def calculate_filtered_cities(df: pd.DataFrame) -> pd.Series:
    total_vacancies = df.shape[0]
    min_vacancies_threshold = total_vacancies * 0.002
    filtered_cities = df['area_name'].value_counts()
    filtered_cities = filtered_cities[filtered_cities >= min_vacancies_threshold]
    return filtered_cities


def print_vacancy_share_by_area(vacancies_by_area: dict):
    print(f"Доля вакансий по городам: {print_top_cities(vacancies_by_area)}")


def print_vacancy_share_by_area_for_profession(prof_vacancies_by_area: dict):
    print(f"Доля вакансий по городам для выбранной профессии: {print_top_cities(prof_vacancies_by_area)}")


def calculate_salaries_by_area(df: pd.DataFrame, filtered_cities: pd.Series) -> dict:
    df = df.dropna(subset=["salary"])
    salaries_by_area = df.groupby('area_name')['salary'].mean().astype(int)
    salaries_by_area = salaries_by_area[salaries_by_area.index.isin(filtered_cities.index)].sort_values(ascending=False).to_dict()
    return salaries_by_area


def print_salaries_by_area(salaries_by_area: dict):
    print(f"Уровень зарплат по городам: {get_top_cities_by_salary(salaries_by_area)}")


def print_salaries_by_area_for_profession(prof_salaries_by_area: dict):
    print(f"Уровень зарплат по городам для выбранной профессии {get_top_cities_by_salary(prof_salaries_by_area)}")


def print_geography(df: pd.DataFrame, profession_name: str = None):
    filtered_cities = calculate_filtered_cities(df)
    vacancies_by_area = df['area_name'].value_counts(normalize=True)
    vacancies_by_area = vacancies_by_area[vacancies_by_area.index.isin(filtered_cities.index)].to_dict()
    print_vacancy_share_by_area(vacancies_by_area)

    if profession_name:
        data_prof = df[df['name'].str.contains(profession_name, case=False, na=False)]
        prof_vacancies_by_area = data_prof['area_name'].value_counts(normalize=True)
        prof_vacancies_by_area = prof_vacancies_by_area[prof_vacancies_by_area.index.isin(filtered_cities.index)].to_dict()
        print_vacancy_share_by_area_for_profession(prof_vacancies_by_area)

        salaries_by_area = calculate_salaries_by_area(df, filtered_cities)
        print_salaries_by_area(salaries_by_area)

        prof_salaries_by_area = calculate_salaries_by_area(data_prof, filtered_cities)
        print_salaries_by_area_for_profession(prof_salaries_by_area)



def print_skills(df: pd.DataFrame):
    df["key_skills"] = df["key_skills"].apply(lambda row: [] if pd.isnull(row) else row.split("\n"))
    skills_freq = df.explode("key_skills").groupby(["published_year", "key_skills"]).size().reset_index(
        name="frequency")

    top_skills = (
        skills_freq
        .groupby("published_year")
        .apply(lambda x: x.nlargest(20, "frequency"))
        .reset_index(drop=True)
    )
    skills_frequency_by_year: dict = top_skills.groupby("published_year").apply(
        lambda x: [x["key_skills"].to_list(), x["frequency"].to_list()]).to_dict()

    for skill_by_year in skills_frequency_by_year.keys():
        array = skills_frequency_by_year[skill_by_year]
        dict = {x: y for x, y in zip(array[0], array[1])}
        print(f"{skill_by_year}: {json.dumps(dict, ensure_ascii=False).encode('utf-8').decode()}")


def print_top_cities(cities: dict) -> dict:
    top_cities = dict(list(cities.items())[:15])
    other_cities_sum = 1 - sum(top_cities[city] for city in top_cities)
    top_cities["Другие"] = other_cities_sum
    return top_cities


def get_top_cities_by_salary(cities: dict) -> dict:
    top_cities = dict(list(cities.items())[:15])
    other_cities_sum = sum(cities[item] for item in cities if item not in top_cities) / (len(cities) - 15)
    top_cities["Другие"] = int(other_cities_sum)
    return top_cities


# Подготовка данных из файла для аналитики. Запись обработанного файла в новый, чтобы больше не обращаться к API ЦБ
# file_name = "vacancies.csv"
# data = pd.read_csv(file_name)
# data = prepare_df(data)
# data.to_csv("vacancies_with_salary.csv", index=False, encoding='utf-8')


file_name = "vacancies_with_salary.csv"
# Вводить regex все возможные названия через |
profession_name = r"android|андроид|andorid|andoroid|andriod|andrind|xamarin"
data = pd.read_csv(file_name)

# get_demand_page_content(data.copy())
# print_geography(data.copy())
print_skills(data.copy())
print_skills(data[data['name'].str.contains(profession_name, case=False, na=False)].copy()) # Навыки для выбранной профессии
