import os
from math import log2

from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView

from InfoSearch.settings import STATICFILES_DIRS, WEB_PAGES_FILE, INDEX_FILE, TF_IDF_INDEX_FILE, INV_INDEX_FILE
from main_app.models import Document
from s_engine.crawler import Crawler
from s_engine.helpers import get_random_wiki_pages, cos_sim, bool_statement_to_postfix
from s_engine.lemmatizer import lemmatize


class IndexView(TemplateView):
    template_name = "search.html"


class BooleanView(TemplateView):
    template_name = "bool_search.html"


class OptionsView(TemplateView):
    template_name = "options.html"


class ArticlesView(ListView):
    template_name = "articles.html"
    model = Document


def generate_view(request):
    if request.method == 'GET':
        amount = int(request.GET['amount'])
        get_random_wiki_pages(amount)
    return redirect("options")


def download_view(request):
    if request.method == 'GET':
        docs = Document.objects.all()
        docs.delete()
        crawler = Crawler()
        index = 0
        f = open(os.path.join(STATICFILES_DIRS[0], WEB_PAGES_FILE))
        for url in f:
            name, path = crawler.crawl(url.replace('\n', ' '))
            doc = Document.objects.create(index=index, url=url, name=name, file=path)
            doc.save()
            index += 1
        f.close()
    return redirect("options")


def delete_view(request):
    if request.method == 'GET':
        docs = Document.objects.all()
        docs.delete()
    return redirect("options")


def gen_index(request):
    if request.method == 'GET':
        ixfile = open(os.path.join(STATICFILES_DIRS[0], INDEX_FILE), 'w')
        for d in Document.objects.all():
            ixfile.write('{} {} {}\n'.format(d.index, d.file.path, d.url))
        ixfile.close()
    return redirect("options")


def generate_inv_index(request):
    if request.method == 'GET':
        docs = Document.objects.all()
        rev_index = {}
        for d in docs:
            file = open(d.file.path, 'r', encoding='utf-8')
            words, lemmas = lemmatize(file.read())
            file.close()
            for l in lemmas:
                if l not in rev_index.keys():
                    rev_index[l] = set()
                rev_index[l].add(d.index)
        ixfile = open(os.path.join(STATICFILES_DIRS[0], INV_INDEX_FILE), 'w')
        for k in rev_index.keys():
            ixfile.write('{} {}\n'.format(k, ' '.join(str(s) for s in rev_index[k])))
        ixfile.close()
    return redirect("options")


def generate_tf_idf_index(request):
    if request.method == 'GET':
        # Рассчёт IDF
        docs = Document.objects.all()
        idf = {}
        ixfile = open(os.path.join(STATICFILES_DIRS[0], INV_INDEX_FILE), 'r')
        for l in ixfile.readlines():
            lemma = l.split(' ')[0]
            idf[lemma] = log2(len(docs) / len(l.split(' ')[1:]))
        ixfile.close()

        # Предзагрузка лемматизированных документов
        doc_lemmas = []
        for d in docs:
            file = open(d.file.path, 'r', encoding='utf-8')
            words, lemmas = lemmatize(file.read())
            doc_lemmas.append(lemmas)

        # Рассчёт TF
        tf = {}
        for k in idf.keys():
            entries = []
            for lemmas in doc_lemmas:
                i = 0
                for l in lemmas:
                    if k == l:
                        i += 1
                entries.append(i / len(lemmas))
            tf[k] = entries

        # Рассчёт TF-IDF векторов
        tf_idf = {}
        for k in idf.keys():
            tf_idf[k] = [x * idf[k] for x in tf[k]]

        # Сохранение индекса в файл
        ixfile = open(os.path.join(STATICFILES_DIRS[0], TF_IDF_INDEX_FILE), 'w')
        for k in tf_idf.keys():
            ixfile.write('{} {} {}\n'.format(k, idf[k], ' '.join(str(s) for s in tf_idf[k])))
        ixfile.close()
    return redirect("options")


def vector_search(request):
    docs = None
    if request.method == 'GET':
        query = request.GET['q']
        q_words, q_lemmas = lemmatize(query)

        # Загрузка TF-IDF индексов из файла
        tf_idf = {}
        idf = {}
        ixfile = open(os.path.join(STATICFILES_DIRS[0], TF_IDF_INDEX_FILE), 'r')
        for l in ixfile.readlines():
            lemma = l.split(' ')[0]
            idf[lemma] = float(l.split(' ')[1])
            tf_idf[lemma] = [float(x) for x in l.split(' ')[2:]]
        ixfile.close()

        # Вычисление вектора запроса
        ql_counts = {}
        for ql in q_lemmas:
            if ql in ql_counts.keys():
                ql_counts[ql] += 1
            else:
                ql_counts[ql] = 1

        max_count = 0
        for k in ql_counts.keys():
            if ql_counts[k] > max_count:
                max_count = ql_counts[k]

        q_vector = []
        for k in idf.keys():
            if k in ql_counts.keys():
                q_vector.append((ql_counts[k] / max_count) * idf[k])
            else:
                q_vector.append(0)

        # Рассчёт длин векторов
        vectors = []
        for i in range(len(Document.objects.all())):
            v = []
            for k in tf_idf.keys():
                v.append(tf_idf[k][i])
            vectors.append(v)

        results = []
        for i, v in enumerate(vectors):
            results.append((i, cos_sim(v, q_vector)))

        results.sort(reverse=True, key=lambda tup: tup[1])
        doc_indexes = []
        for i, x in results:
            if x > 0:
                doc_indexes.append((i, x))

        docs = []
        for i, x in doc_indexes:
            docs.append({'doc': Document.objects.get(index=i), 'val': x})

    return render(request, "results.html", context={'docs': docs})


def boolean_search(request):
    result_set = None
    if request.method == 'GET':
        q = request.GET['q']

        # Загрузка инвертированных индексов
        index = {}
        ixfile = open(os.path.join(STATICFILES_DIRS[0], INV_INDEX_FILE), 'r')
        for l in ixfile.readlines():
            lemma = l.split(' ')[0]
            index[lemma] = set(int(x) for x in l.split(' ')[1:])
        ixfile.close()

        # Преобразование терминов в множества документов
        operations = bool_statement_to_postfix(q)
        sets = []
        all_set = set(range(len(Document.objects.all())))
        for x in operations:
            if x != 'OR' and x != 'AND' and x != 'NOT':
                words, l = lemmatize(x)
                if l[0] in index.keys():
                    x = index[x]
                else:
                    x = set()
            sets.append(x)

        stack = []

        for x in sets:
            if not isinstance(x, set):
                if x == 'OR':
                    x1 = stack.pop()
                    x2 = stack.pop()
                    stack.append(x1.union(x2))
                elif x == 'AND':
                    x1 = stack.pop()
                    x2 = stack.pop()
                    stack.append(x1.intersection(x2))
                elif x == 'NOT':
                    x1 = stack.pop()
                    stack.append(all_set.difference(x1))
            else:
                stack.append(x)

        result_set = stack.pop()

    return render(request, "bool_results.html", context={'docs': Document.objects.filter(index__in=result_set)})
