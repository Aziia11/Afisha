from rest_framework import serializers
from .models import Director, Movie, Review, Category, Tag

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
        name = Tag
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
        word = self.context['word']
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
