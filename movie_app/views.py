from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, DirectorDetailSerializer, MovieSerializer, MovieDetailSerializer, ReviewSerializer, ReviewDetailSerializer

# Create your views here.
@api_view(['GET'])
def static_data_view(request):
    dict_ = {
        'key': 'I am so proud of myself!!'
    }
    return Response(data=dict_)
@api_view(['GET'])
def director_list_view(request):
    directors = Director.objects.all()
    data = DirectorSerializer(directors, many=True).data
    return Response(data=data)

@api_view(['GET'])
def director_detail_view(request, id):
    directors = Director.objects.get(id=id)
    data = DirectorDetailSerializer(directors, many=False).data
    return Response(data=data)

@api_view(['GET'])
def movie_list_view(request):
    movies = Movie.objects.all()
    data = MovieSerializer(movies, many=True).data
    return Response(data=data)

@api_view(['GET'])
def movie_detail_view(request, id):
    movies = Movie.objects.get(id=id)
    data = MovieDetailSerializer(movies, many=False).data
    return Response(data=data)

@api_view(['GET'])
def review_list_view(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(reviews, many=True).data
    return Response(data=data)

@api_view(['GET'])
def review_detail_view(request, id):
    reviews = Review.objects.get(id=id)
    data = ReviewDetailSerializer(reviews, many=False).data
    return Response(data=data)