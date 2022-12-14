
from django.shortcuts import get_object_or_404
from .serializers import StreamPlatformSerializer
from ..models import Watchlist, StreamPlatform,Review
from watchlist_app.api.serializers import WatchlistSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
# from rest_framework import mixins 
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from .permissions import  IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from .throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination
 

class UserReview(generics.ListAPIView) :
    serializer_class = ReviewSerializer
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    # def get_queryset(self) :
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    
    def get_queryset(self) :
        #map the parameters instead of mapping the value.
        username = self.request.query_params.get('username', None)

        return Review.objects.filter(review_user__username=username)








class ReviewList(generics.ListAPIView) :
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, ReviewListThrottle]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username','active']


    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewCreate(generics.CreateAPIView) :
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self) :

        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = Watchlist.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=review_user)

        if review_queryset.exists() :
            raise ValidationError("You have already reviewed this movie!") 

        if movie.number_rating == 0 :
            movie.avg_rating  = serializer.validated_data['rating']
        else :
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2

        movie.number_rating = movie.number_rating + 1
        movie.save()

        serializer.save(watchlist=movie, review_user=review_user)
        # return super().perform_create(serializer)
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView) :
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    

'''
class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView) :
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs) :
        return self.retrieve(request, *args, **kwargs)

class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView) :
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    def get(self, request, *args, **kwargs) :
        return self.list(request, *args, **kwargs)
    
    def post(self,request, *args, **kwargs) :
        return self.create(request, *args, **kwargs)

'''


'''
class StreamPlatformVS(viewsets.ViewSet) :
    def list(self,request) :
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self, request,pk=None) :
        queryset = StreamPlatform.objects.all()
        watchlist = get_object_or_404(queryset,pk=pk)
        serializer = StreamPlatformSerializer(watchlist)
        return Response(serializer.data)

    def post(self,request) : 
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        else : 
            return Response(serializer.errors)
'''
#Using Model View Set | works with router |  We have the control of everything GET, PUT, PATCH, DELETE, HEAD, OPTIONS  

class StreamPlatformVS(viewsets.ModelViewSet) :
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    
# class StreamPlatformAV(APIView) :
#     permission_classes = [IsAdminOrReadOnly]
#     def get(self,request) :
#         platform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platform,many=True,context={'request' : request})
#         return Response(serializer.data)
    
#     def post(self,request) :
#         serializer = StreamPlatformSerializer(data=request.data) 
#         if serializer.is_valid() :
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)




# class StreamPlatformDetailAV(APIView) :
#     permission_classes = [IsAdminOrReadOnly]
#     def get(self,request,pk) :
#         try :
#             platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist :
#             return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND) 
#         serializer = StreamPlatformSerializer(platform,context={'request': request})
#         return Response(serializer.data)
    
#     def put(self,request,pk) :
#         platform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(platform,data=request.data)  #movie data aslo needs to be included as it will be updated.
#         if serializer.is_valid() :
#             serializer.save()
#             return Response(serializer.data)
#         else:
#              return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self,request,pk) :
#         try :
#             platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist :
#             return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND) 
#         platform.delete()
#         return Response(status.HTTP_204_NO_CONTENT)



class WatchListLAV(generics.ListAPIView) :
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['platform__name','title'] # will match exact keyword
    # filter_backends = [filters.SearchFilter]
    # search_fields  = ['title', 'platform__name']
    # search_fields  = ['=title', '=platform__name'] # will search exact

    #Ordering
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = [ '-avg_rating']
    # pagination_class = WatchListPagination
    pagination_class =WatchListCPagination


    '''
The search behavior may be restricted by prepending various characters to the search_fields.

'^' Starts-with search.
'=' Exact matches.
'@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
'$' Regex search.
   
    '''
        
class WatchListAV(APIView)  :
    permission_classes = [IsAdminOrReadOnly]

    def get(self,request) :
        movies = Watchlist.objects.all()
        serializer = WatchlistSerializer(movies,many=True)
        return Response(serializer.data)

    def post(self,request) :
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors)



class WatchDetailAV(APIView) :
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk) :
        try :
            movie = Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist :
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND) 
        serializer = WatchlistSerializer(movie)
        return Response(serializer.data)
    
    def put(self,request,pk) :
        movie = Watchlist.objects.get(pk=pk)
        serializer = WatchlistSerializer(movie,data=request.data)  #movie data aslo needs to be included as it will be updated.
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        else:
             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk) :
        try :
            movie = Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist :
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND) 
        movie.delete()
        return Response(status.HTTP_204_NO_CONTENT)









# @api_view(['GET','POST'])
# def movie_list(request) :
#     if request.method == 'GET' :

#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)
#         return Response(serializer.data)
#     if request.method == 'POST' :
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid() :
#             serializer.save()
#             return Response(serializer.data)
#         else :
#             return Response(serializer.errors)


# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,pk) :
#     if request.method == 'GET' :
#         try :
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist :
#             return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND) 
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#     if request.method == 'PUT' :
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie,data=request.data)  #movie data aslo needs to be included as it will be updated.
#         if serializer.is_valid() :
#             serializer.save()
#             return Response(serializer.data)
#         else:
#              return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     if request.method == 'DELETE' :
#         try :
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist :
#             return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND) 
#         movie.delete()
#         return Response(status.HTTP_204_NO_CONTENT)



