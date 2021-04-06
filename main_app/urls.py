from django.urls import path

from main_app.views import OptionsView, generate_view, download_view, delete_view, generate_inv_index, \
    generate_tf_idf_index, vector_search, boolean_search, ArticlesView

urlpatterns = [
    path('', OptionsView.as_view(), name="options"),
    path('articles/', ArticlesView.as_view(), name="articles"),
    path('generate/', generate_view, name="generate"),
    path('download/', download_view, name="download"),
    path('delete/', delete_view, name="delete"),
    path('inv_index/', generate_inv_index, name="inv_index"),
    path('tf_idf/', generate_tf_idf_index, name="tf_idf"),
    path('v_search/', vector_search, name="v_search"),
    path('b_search/', boolean_search, name="b_search")
]
