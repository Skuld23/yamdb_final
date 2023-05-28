from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.filters import TitleFilterSet
from reviews.models import Category, Genre, Review, Title, User

from api_yamdb.settings import ADMIN_EMAIL

from .mixins import CreateDeleteListViewSet
from .permissions import Admin, AdminOrReadOnly, IsAuthorOrModer
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewsSerializer,
                          SerializerForAdminUser, SerializerForSignUp,
                          SerializerForToken, SerializerForUsers,
                          TitleCreateSerializer, TitleSerializer)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SerializerForSignUp(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, create = User.objects.get_or_create(
            **serializer.validated_data
        )
    except IntegrityError:
        raise ValidationError("Неверное имя пользователя или email")
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="Регистрация",
        message=f"Код подтверждения: {confirmation_code}",
        from_email=ADMIN_EMAIL,
        recipient_list=[user.email]
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_jwt_token(request):
    serializer = SerializerForToken(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get("username")
    )
    if default_token_generator.check_token(
            user, serializer.validated_data.get("confirmation_code")
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SerializerForUsers
    permission_classes = [Admin]
    filter_backends = (filters.SearchFilter,)
    lookup_field = "username"
    search_fields = ('username',)
    http_method_names = ['post', 'get', 'patch', 'delete']

    def get_serializer_class(self):
        if (not self.request.user.there_is_admin
                or self.request.user.is_superuser):
            return SerializerForUsers
        return SerializerForAdminUser

    @action(detail=False, methods=['GET', 'PATCH', ],
            permission_classes=[IsAuthenticated],
            )
    def me(self, request):
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'PATCH':
            serializer = SerializerForUsers(user, data=request.data,
                                            partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateDeleteListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDeleteListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering_fields = ['id']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (IsAuthenticatedOrReadOnly, AdminOrReadOnly,)
    filterset_class = TitleFilterSet
    ordering_fields = ['name']

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE'):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrModer,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrModer)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id, title__pk=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        new_review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=new_review)
