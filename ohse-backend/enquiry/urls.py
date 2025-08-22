from django.urls import path
from .views import EnquiryView
from .views import *

urlpatterns = [
    path('', EnquiryView.as_view(), name='enquiry'),
    path('<uuid:enquiry_id>/comments/', EnquiryCommentView.as_view(), name='enquiry-comments'),
]
