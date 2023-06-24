from rest_framework import status

from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db.models import Sum
from django.http import HttpResponse
from djoser.views import UserViewSet
from rest_framework.exceptions import ValidationError

from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    FavoriteRecipe,
    ShoppingList,
    RecipeIngredient
)
from users.models import User, Subscribe
from api.serializers import (
    IngredientSerializer,
    ShortRecipeSerializer,
    TagSerializer,
    SubscriptionsSerializer,
    CustomUserSerializer,
    GetRecipeSerializer,
    CreateRecipeSerializer
)
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.pagination import Pagination
from api.filters import RecipeFilter, IngredientFilter


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetRecipeSerializer
        return CreateRecipeSerializer

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=pk)
            obj, created = FavoriteRecipe.objects.get_or_create(
                user=request.user,
                recipe=recipe
            )
            if created:
                serializer = ShortRecipeSerializer(recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'Ошибка': 'Рецепт уже есть в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)

        obj = FavoriteRecipe.objects.filter(user=request.user,
                                            recipe__id=pk).delete()

        if obj[0] > 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Ошибка': 'Рецепт отсутствует в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=pk)
            obj, created = ShoppingList.objects.get_or_create(
                user=request.user,
                recipe=recipe
            )
            if created:
                serializer = ShortRecipeSerializer(recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'Ошибка': 'Рецепт уже есть в списке покупок'},
                                status=status.HTTP_400_BAD_REQUEST)

        obj = ShoppingList.objects.filter(user=request.user,
                                          recipe__id=pk).delete()

        if obj[0] > 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Ошибка': 'Рецепт отсутствует в списке покупок'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_list = user.shopping_list.all()

        if not shopping_list:
            return Response("Список покупок пуст.",
                            status=status.HTTP_400_BAD_REQUEST)

        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_list__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        content = 'Список покупок:\n\n'
        for ingredient in ingredients:
            name = ingredient.get('ingredient__name')
            measurement_unit = ingredient.get(
                'ingredient__measurement_unit'
            )
            amount = ingredient.get('amount')
            content += f'{name} ({measurement_unit}) - {amount}\n'

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
        return response


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = Pagination

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = SubscriptionsSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Subscribe.objects.filter(user=user, author=author).exists():
                raise ValidationError(
                    detail='Вы и так не подписаны на этого пользователя',
                    code=status.HTTP_400_BAD_REQUEST
                )
            subscription = get_object_or_404(Subscribe,
                                             user=user,
                                             author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribing__user=user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(
            paginated_queryset,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
