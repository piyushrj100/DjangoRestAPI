from django.urls import path, include
# from imdbapi.watchlist_app.api.views import WatchList 

# from watchlist_app.api.views import movie_list ,movie_details
from watchlist_app.api.views import (WatchDetailAV ,
 WatchListAV, 
 UserReview,
#  StreamPlatformAV,
#  StreamPlatformDetailAV,
 ReviewList,ReviewDetail,
 ReviewCreate,
 WatchListLAV,
 StreamPlatformVS)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename = 'streamplatform')


urlpatterns = [
    path('list/',WatchListAV.as_view(),name = 'movie-list'),
    path('<int:pk>/',WatchDetailAV.as_view(), name='movie-detail'),
    path('',include(router.urls)),

    # path('stream/',StreamPlatformAV.as_view(),name = 'stream-list'), # WE will combine both using router 
    # path('stream/<int:pk>/',StreamPlatformDetailAV.as_view(),name = 'stream-detail'),

    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/',ReviewDetail.as_view(),name='review-detail'),
    path('<int:pk>/review-create/',ReviewCreate.as_view(), name='review-create'),
    
    # path('review/',ReviewList.as_view(), name = 'review-list'),
    # path('review/<int:pk>/',ReviewDetail.as_view(), name = 'review-detail'),

    path('reviews/',UserReview.as_view(), name = 'user-review-detail'),
    path('list2/',WatchListLAV.as_view(), name = 'watch-list'),

]