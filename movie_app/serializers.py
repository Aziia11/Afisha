from rest_framework import serializers
from movie_app.models import Director, Movie, Review, Category, Tag
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id name'.split()


class DirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = '__all__'

class DirectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id name'.split()


class MovieSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagsSerializer(many=True)
    tag_list = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title category tags rating tag_list'.split()

    def get_tag_list(self, movie):
        return [i.name for i in movie.tags.all()]



class MovieDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Movie
        fields = 'id title description duration rating tag_list reviews'.split()


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id name'.split()


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=100)
    description = serializers.CharField(required=False, default='')
    duration = serializers.FloatField(min_value=0.5, max_value=1000000)
    category_id = serializers.IntegerField(allow_null=True, required=False,
                                           default=None)
    tags = serializers.ListField(child=serializers.IntegerField())

    def validate_category_id(self, category_id):
        #try:
         #   Category.objects.get(id=category_id)
       # except Category.DoesNotExist:
        #    raise ValidationError('Category not found')
        categories = Category.objects.filter(id=category_id)
        if categories.count()== 0:
            raise ValidationError(f'Category not found with {category_id}')
        return category_id


    def validate_tags(self, tags):
        #for tag in tags:
         #   try:
        #        Tag.objects.get(id=tag)
         #   except Tag.DoesNotExist:
         #       raise ValidationError('Tag is not found')
        tag_list = Tag.objects.filter(id__in=tags)
        if tag_list.count() != len(set(tags)):
            raise ValidationError('Tag not found')
        return tags

class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=100)

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    stars = serializers.IntegerField()
    movie = serializers.CharField()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        if User.objects.filter(username=username).count() > 0:
            raise ValidationError('User already exists')
        return username