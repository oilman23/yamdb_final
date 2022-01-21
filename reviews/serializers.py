from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('id',)


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'category',
            'genre',
            'name',
            'year',
            'description',
            'rating',
        )
        read_only_fields = ('id', 'rating')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    title = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Title.objects.all()
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data

        id_title = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if Review.objects.filter(author=author, title__id=id_title).exists():
            raise serializers.ValidationError(
                'You can not leave review twice.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    review = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Review.objects.all()
    )

    class Meta:
        model = Comment
        fields = '__all__'
