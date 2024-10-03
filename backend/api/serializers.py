from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.constants import MAX_LENGTH_RECIPE_NAME
from recipes.models import (Favorite,
                            Ingredient,
                            Recipe,
                            RecipeIngredient,
                            ShoppingList,
                            Tag)
from users.models import Follow, User


class UserCreateSerializer(UserCreateSerializer):
    """Переиспользуем сериализатор Djoser для создания юзера."""
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'password')


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Собственный сериализатор создания юзера при регистрации."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                f'Юзернейм {value} уже занят.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(f'{value} уже зарегистрирован.')
        return value


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для получения, обновления информации о пользователе"""

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    avatar = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'is_subscribed',
                  'avatar')

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий юзер из сессии на блогера."""
        subscribe = Follow.objects.filter(
            user=self.context['request'].user.id,
            following=obj,
        ).exists()
        return subscribe


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для получения содержимого объекта тега."""

    class Meta:
        model = Tag
        fields = ('id',
                  'name',
                  'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для получения  содержимого объекта ингредиента."""

    class Meta:
        model = Ingredient
        fields = ('id',
                  'name',
                  'measurement_unit',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Запись наименования и количества ингредиентов в рецпет.
    Принимает пару id + amount, возвращает name + amount.
    """

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(),
                                            source='ingredient')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id',
                  'name',
                  'measurement_unit',
                  'amount')
        read_only_fields = ('name',
                            'measurement_unit')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для READ-операций (GET) с рецептами."""

    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True,
                                             source='recipe_ingredient_amount')
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user,
                                           recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingList.objects.filter(user=user,
                                               recipe=obj).exists()
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для записи и редактирования рецептов."""

    ingredients = RecipeIngredientSerializer(many=True,
                                             required=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all(),
                                              required=True)
    name = serializers.CharField(max_length=MAX_LENGTH_RECIPE_NAME,
                                 required=True)
    image = Base64ImageField(max_length=None,
                             use_url=True,
                             required=True)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(required=True)

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time')
        read_only_fields = ('id',
                            'author',
                            'tags',
                            'ingredients')

    def validate_ingredients(self, value):
        """Проверяем, что ингредиенты не пустые и уникальные."""
        ingredients = self.initial_data.get('ingredients')
        # Проверяем, что список ингредиентов не пустой
        if len(ingredients) == 0:
            raise serializers.ValidationError(
                {'ingredients': "Укажите хотя бы один ингредиент."}
            )

        # Список для отслеживания уникальных ингредиентов
        ingredients_list = []

        # Проверяем, что ингредиенты не повторяются
        for item in ingredients:
            if item['id'] in ingredients_list:
                raise serializers.ValidationError(
                    {'ingredients': "Ингредиенты не должны повторяться."}
                )
            ingredients_list.append(item['id'])

        return value

    def validate_tags(self, value):
        """Проверяем, что теги не пустые и уникальные."""
        if not value:
            raise serializers.ValidationError("Теги не могут быть пустыми.")

        if len(value) != len(set(value)):
            raise serializers.ValidationError("Теги не могут повторяться.")
        return value

    def validate_image(self, value):
        """Проверяем, что изображение не является пустой строкой."""
        if value == "" or value is None:
            raise serializers.ValidationError("Картинка обязательна.")
        return value

    def validate_cooking_time(self, value):
        """Проверяем, что время приготовления больше 1."""
        if value < 1:
            raise serializers.ValidationError(
                "Время приготовления должно быть больше 1 минуты.")

        return value

    def complete_recipe(self,
                        recipe,
                        tags_part,
                        ingredients_part):
        """
        Функция для:
        - отдельной дозаписи тегов в Recipe;
        - отдельной дозаписи ингредиентов и их кол-ва в RecipeIngredient.
        """
        # Перезаписываем существующие теги новыми
        recipe.tags.set(tags_part)
        # Извлечем значения из словаря:
        for item in ingredients_part:
            ingredient = item.get('ingredient')
            amount = item.get('amount')
            # Создадим объект связи между рецептом, ингредиентом, и кол-вом.
            ingredient_amount, status = RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount,
            )
        return recipe

    def create(self, validated_data):
        """
        Чтобы избежать конфликтов при создании рецепта,
        извлечем теги и ингредиенты, и обработаем их отдельно.
        """
        # Вынес из вью задание автора по-умолчанию.
        validated_data['author'] = self.context['request'].user
        # Обработаем провалидированные списки отдельно.
        tags_popped = validated_data.pop('tags')
        ingredients_popped = validated_data.pop('ingredients')
        # Создаем новый объект "Recipe" с оставшимися валидированными данными.
        recipe_incomplete = Recipe.objects.create(**validated_data)
        return self.complete_recipe(
            recipe_incomplete,  # передаем созданный рецепт (его часть).
            tags_popped,  # передаем извлеченные теги.
            ingredients_popped  # передаем извлеченные ингредиенты.
        )

    def update(self, instance, validated_data):
        """
        Обновляет существующий объект рецепта на основе валидированных данных.
        """
        # Проверяем наличие ингредиентов и тегов в validated_data
        ingredients = validated_data.get('ingredients')
        tags = validated_data.get('tags')

        if ingredients is None:
            raise serializers.ValidationError(
                {'ingredients':
                 'Поле ingredients обязательно для обновления рецепта.'}
            )
        if tags is None:
            raise serializers.ValidationError(
                {'tags': 'Поле tags обязательно для обновления рецепта.'}
            )

        # Вызываем валидаторы для проверки ингредиентов и тегов.
        self.validate_ingredients(ingredients)
        self.validate_tags(tags)

        # Обработаем провалидированные списки отдельно.
        tags_popped = validated_data.pop('tags')
        ingredients_popped = validated_data.pop('ingredients')
        # Очищаем теги и ингредиенты у текущего рецепта перед обновлением.
        instance.ingredients.clear()
        instance.tags.clear()
        # Обновляем оставшиеся поля рецепта новыми значениями.
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return self.complete_recipe(
            instance,
            tags_popped,
            ingredients_popped
        )

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class FavoriteShoppingListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для показа атрибутов рецепта после его добавления
    в Избранное или в Список Покупок.
    """
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор модели Читатель (follower) - Блогер (following)."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    avatar = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count',
                  'avatar')
        read_only_fields = ('email',
                            'username',
                            'first_name',
                            'last_name',
                            'is_subscribed',
                            'recipes',
                            'recipes_count',
                            'avatar')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Follow.objects.filter(user=request.user,
                                     following=obj).exists()

    def get_recipes(self, obj):
        limit = self.context['request'].query_params.get('recipes_limit')
        query = obj.recipes.all()

        limit_value = None
        if limit:
            # Пробуем преобразовать limit в целое число.
            try:
                limit_value = int(limit)
            except (ValueError, TypeError):
                # Зададим limit_value в 0 при ошибках преобразования.
                limit_value = 0

        if limit_value:
            query = query[:limit_value]

        recipes = FavoriteShoppingListSerializer(query, many=True)
        return recipes.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
