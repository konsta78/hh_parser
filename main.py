from flask import Flask, render_template, request, redirect
from extract import get_all_jobs
import saveCSV

app = Flask('HHScrapper')
db = {}

@app.route('/')
def index():
    """
    Главная страница сайта
    :return: html-шаблон главной страницы
    """
    return render_template('index.html')


@app.route('/result')
def result():
    """
    Страница с результатами поиска
    :return: html-шаблон страницы с результатами при введенном ключе поиска,
    иначе - переход на главную страницу
    """
    inquiry = request.args.get('vacancy')
    if inquiry:
        inquiry = inquiry.lower()
        jobs = get_all_jobs(inquiry)
        count_jobs = len(jobs)
        db['inquiry'] = jobs
    else:
        return redirect('/')
    return render_template('results.html',
                           result=inquiry, jobs=jobs, count_jobs=count_jobs)


@app.route('/export')
def export_data_to_csv():
    """
    Сохранение результатов поиска в CSV-файл
    :return: при наличии данных - CSV-файл,
    иначе - переход на главную страницу
    """
    if db:
        try:
            saveCSV.save_jobs_to_csv(db['inquiry'])
            return redirect('/')
        except Exception:
            return ''
    return redirect('/')


app.run()