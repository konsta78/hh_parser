import csv


def save_jobs_to_csv(jobs):
    """
    Сохраняет полученый список с описанием вакансий в csv-файл
    :param jobs: список с описанием вакансий
    :return: csv-файл
    """
    rows = list(jobs[0].keys()) # наимменование колонок
    with open('jobs.csv', mode='w', encoding='utf-8') as file:
        csv.writer(file).writerow(rows)
        for job in jobs:
            csv.writer(file).writerow(list(job.values()))
        file.close()