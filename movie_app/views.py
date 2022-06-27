from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, DirectorDetailSerializer, MovieSerializer, MovieDetailSerializer, ReviewSerializer,\
    ReviewDetailSerializer, MovieValidateSerializer, DirectorValidateSerializer, ReviewValidateSerializer

# Create your views here.
@api_view(['GET'])
def static_data_view(request):
    dict_ = {
        'key': 'I am so proud of myself!!'
    }
    return Response(data=dict_)
@api_view(['GET', 'POST'])
def director_list_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorSerializer(directors, many=True).data
        return Response(data=data)
    else:
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        name = serializer.validated_data('name')
        director = Director.objects.create(
            name=name,
        )
        director.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Director created',
                              'director': DirectorDetailSerializer(director).data})

@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_view(request, id):
    try:
        directors = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(status=status.HHTP_4o4_NOT_FOUND,
                        data={'error': 'Director not found'})
    if request.method == 'GET':
        data = DirectorDetailSerializer(directors, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        directors.delete()
        return Response(data={"message": "Director removed"})
    else:
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        directors.name = serializer.validated_data('name')
        directors.save()
        return Response(data=DirectorDetailSerializer(directors).data)

@api_view(['GET', 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        word = 'B'
        data = MovieSerializer(movies, many=True,
                           context={'word':word}).data
        return Response(data=data)
    else:
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        title = serializer.validated_data('title')
        description = serializer.validated_data('description')
        category_id = serializer.validated_data('category_id')
        tags = serializer.validated_data('tags')
        director = serializer.validated_data('directors')
        movie = Movie.objects.create(
            title=title,
            description=description,
            category_id=category_id,
            director=director,
        )
        movie.tags.set(tags)
        movie.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Movie created',
                              'movie': MovieDetailSerializer(movie).data})


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_view(request, id):
    try:
        movies = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HHTP_4o4_NOT_FOUND,
                        data={'error': 'Product not found'})
    if request.method == 'GET':
        data = MovieDetailSerializer(movies, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        movies.delete()
        return Response(data={"message": "Movie removed"})
    else:
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        movies.title = serializer.validated_data('title')
        movies.description = serializer.validated_data('description')
        movies.category_id = serializer.validated_data('category_id')
        movies.director = serializer.validated_data('director')
        movies.tags.set(serializer.validated_data['tags'])
        movies.save()
        return Response(data=MovieDetailSerializer(movies).data)




@api_view(['GET', 'POST'])
def review_list_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data)
    else:
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        text = serializer.validated_data('text')
        stars = serializer.validated_data('stars')
        movie = serializer.validated_data('movie')
        review = Review.objects.create(
            text=text,
            stars=stars,
            movie=movie,
        )
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Review created',
                              'review': ReviewDetailSerializer(review).data})


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_view(request, id):
    try:
        reviews = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HHTP_4o4_NOT_FOUND,
                        data={'error': 'Review not found'})
    if request.method == 'GET':
        data = ReviewDetailSerializer(reviews, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        reviews.delete()
        return Response(data={"message": "Review removed"})
    else:
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        reviews.text = serializer.validated_data('text')
        reviews.stars = serializer.validated_data('stars')
        reviews.movie = serializer.validated_data('movie')
        reviews.save()
        return Response(data=ReviewDetailSerializer(reviews).data)

