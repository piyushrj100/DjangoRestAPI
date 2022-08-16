
from .serializers import StreamPlatformSerializer
from ..models import Watchlist, StreamPlatform,Review
from watchlist_app.api.serializers import WatchlistSerializer, ReviewSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins 

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





class StreamPlatformAV(APIView) :
    def get(self,request) :
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform,many=True,context={'request' : request})
        return Response(serializer.data)
    
    def post(self,request) :
        serializer = StreamPlatformSerializer(data=request.data) 
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class StreamPlatformDetailAV(APIView) :
    def get(self,request,pk) :
        try :
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist :
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND) 
        serializer = StreamPlatformSerializer(platform,context={'request': request})
        return Response(serializer.data)
    
    def put(self,request,pk) :
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform,data=request.data)  #movie data aslo needs to be included as it will be updated.
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        else:
             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk) :
        try :
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist :
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND) 
        platform.delete()
        return Response(status.HTTP_204_NO_CONTENT)



class WatchListAV(APIView)  :
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



