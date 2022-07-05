from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director, Movie, Review, Category, Tag
from .serializers import DirectorSerializer, DirectorDetailSerializer, MovieSerializer, MovieDetailSerializer, \
    ReviewSerializer, \
    ReviewDetailSerializer, MovieValidateSerializer, DirectorValidateSerializer, ReviewValidateSerializer, \
    UserLoginSerializer, UserCreateSerializer, \
    CategorySerializer, TagsSerializer

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from django.http import Http404

# Create your views here.
class TagModelViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = PageNumberPagination


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'id']
    pagination_class = PageNumberPagination


class CategoryItemUpdateDeleteAPIview(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RegisterAPIView(GenericAPIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED,
                        data={'user_id': user.id})


class LoginAPIView(GenericAPIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user is not None:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data={'error': 'Your data was not found'})


# @api_view(['POST'])
# def login_view(request):
#    serializer = UserLoginSerializer(data=request.data)
#    serializer.is_valid(raise_exception=True)
#   user = authenticate(**serializer.validated_data)
# user = authenticate(username=serializer.validated_data['username'],
# password=serializer.validated_data['password'])
#    if user is not None:
#       try:
#           token = Token.objects.get(user=user)
#      except Token.DoesNotExist:
#          token = Token.objects.create(user=user)
#      return Response(data={'key': token.key})
#  return Response(status=status.HTTP_403_FORBIDDEN,
#                data={'error': 'Your data was not found'})
@api_view(['GET'])
def static_data_view(request):
    dict_ = {
        'key': 'I am so proud of myself!!'
    }
    return Response(data=dict_)

class DirectorListAPIView(GenericAPIView):
    def get(self, request):
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DirectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class DirectorListAPIView(mixins.ListModelMixin,
#                           mixins.CreateModelMixin,
#                           generics.GenericAPIView):
#     def get(self, request):
#         if request.method == 'GET':
#             directors = Director.objects.all()
#             data = DirectorSerializer(directors, many=True).data
#             return Response(data=data)
#         else:
#             serializer = DirectorValidateSerializer(data=request.data)
#             if not serializer.is_valid():
#                 return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                                 data={'errors': serializer.errors})
#                 name = serializer.validated_data('name')
#                 director = Director.objects.create(
#                     name=name,
#                 )
#                 director.save()
#                 return Response(status=status.HTTP_201_CREATED,
#                                 data={'message': 'Director created',
#                                       'director': DirectorDetailSerializer(director).data})
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class DirectorDetailAPIView(GenericAPIView):
#     def director_detail_view(request, id):
#         try:
#             directors = Director.objects.get(id=id)
#         except Director.DoesNotExist:
#             return Response(status=status.HHTP_4o4_NOT_FOUND,
#                             data={'error': 'Director not found'})
#         if request.method == 'GET':
#             data = DirectorDetailSerializer(directors, many=False).data
#             return Response(datadat=a)
#         elif request.method == 'DELETE':
#             directors.delete()
#             return Response(data={"message": "Director removed"})
#         else:
#             serializer = DirectorValidateSerializer(data=request.data)
#             if not serializer.is_valid():
#                 return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                                 data={'errors': serializer.errors})
#             directors.name = serializer.validated_data('name')
#             directors.save()
#             return Response(data=DirectorDetailSerializer(directors).data)
#




class DirectorDetailAPIView(GenericAPIView):
    def get_object(self, id):
        try:
            return Director.objects.get(id=id)
        except Director.DoesNotExist:
            return Http404

    def get(self, request, id):
        directors = self.get_object(id)
        serializer = DirectorDetailSerializer(directors, many=False).data
        return Response(serializer.data)

    def put(self, request, id):
        directors = self.get_object(id)
        serializer = DirectorValidateSerializer(directors, data=request.data)
        if serializer.is_valid():
            directors.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        directors = self.get_object(id)
        directors.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






# @api_view(['GET', 'POST'])
# # @permission_classes([IsAuthenticated])
# def movie_list_view(request):
#     print(request.user)
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         word = 'B'
#         data = MovieSerializer(movies, many=True,
#                                context={'word': word}).data
#         return Response(data=data)
#     else:
#         serializer = MovieValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                             data={'errors': serializer.errors})
#         title = serializer.validated_data('title')
#         description = serializer.validated_data('description')
#         category_id = serializer.validated_data('category_id')
#         tags = serializer.validated_data('tags')
#         director = serializer.validated_data('directors')
#         movie = Movie.objects.create(
#             title=title,
#             description=description,
#             category_id=category_id,
#             director=director,
#         )
#         movie.tags.set(tags)
#         movie.save()
#         return Response(status=status.HTTP_201_CREATED,
#                         data={'message': 'Movie created',
#                               'movie': MovieDetailSerializer(movie).data})

class MovieListAPIView(GenericAPIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail_view(request, id):
#     try:
#         movies = Movie.objects.get(id=id)
#     except Movie.DoesNotExist:
#         return Response(status=status.HHTP_4o4_NOT_FOUND,
#                         data={'error': 'Product not found'})
#     if request.method == 'GET':
#         data = MovieDetailSerializer(movies, many=False).data
#         return Response(data=data)
#     elif request.method == 'DELETE':
#         movies.delete()
#         return Response(data={"message": "Movie removed"})
#     else:
#         serializer = MovieValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                             data={'errors': serializer.errors})
#         movies.title = serializer.validated_data('title')
#         movies.description = serializer.validated_data('description')
#         movies.category_id = serializer.validated_data('category_id')
#         movies.director = serializer.validated_data('director')
#         movies.tags.set(serializer.validated_data['tags'])
#         movies.save()
#         return Response(data=MovieDetailSerializer(movies).data)

class MovieDetailAPIView(GenericAPIView):
    def get_object(self, id):
        try:
            return Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return Http404

    def get(self, request, id):
        movies = self.get_object(id)
        serializer = DirectorDetailSerializer(movies, many=False).data
        return Response(serializer.data)

    def put(self, request, id):
        movies = self.get_object(id)
        serializer = DirectorValidateSerializer(movies, data=request.data)
        if serializer.is_valid():
            movies.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        movies = self.get_object(id)
        movies.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view(['GET', 'POST'])
# def review_list_view(request):
#     if request.method == 'GET':
#         reviews = Review.objects.all()
#         data = ReviewSerializer(reviews, many=True).data
#         return Response(data=data)
#     else:
#         serializer = ReviewValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                             data={'errors': serializer.errors})
#         text = serializer.validated_data('text')
#         stars = serializer.validated_data('stars')
#         movie = serializer.validated_data('movie')
#         review = Review.objects.create(
#             text=text,
#             stars=stars,
#             movie=movie,
#         )
#         review.save()
#         return Response(status=status.HTTP_201_CREATED,
#                         data={'message': 'Review created',
#                               'review': ReviewDetailSerializer(review).data})
#
class ReviewListAPIView(GenericAPIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# @api_view(['GET', 'PUT', 'DELETE'])
# def review_detail_view(request, id):
#     try:
#         reviews = Review.objects.get(id=id)
#     except Review.DoesNotExist:
#         return Response(status=status.HHTP_4o4_NOT_FOUND,
#                         data={'error': 'Review not found'})
#     if request.method == 'GET':
#         data = ReviewDetailSerializer(reviews, many=False).data
#         return Response(data=data)
#     elif request.method == 'DELETE':
#         reviews.delete()
#         return Response(data={"message": "Review removed"})
#     else:
#         serializer = ReviewValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                             data={'errors': serializer.errors})
#         reviews.text = serializer.validated_data('text')
#         reviews.stars = serializer.validated_data('stars')
#         reviews.movie = serializer.validated_data('movie')
#         reviews.save()
#         return Response(data=ReviewDetailSerializer(reviews).data)
class ReviewDetailAPIView(GenericAPIView):
    def get_object(self, id):
        try:
            return Review.objects.get(id=id)
        except Review.DoesNotExist:
            return Http404

    def get(self, request, id):
        reviews = self.get_object(id)
        serializer = ReviewDetailSerializer(reviews, many=False).data
        return Response(serializer.data)

    def put(self, request, id):
        reviews = self.get_object(id)
        serializer = ReviewValidateSerializer(reviews, data=request.data)
        if serializer.is_valid():
            reviews.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        reviews = self.get_object(id)
        reviews.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
