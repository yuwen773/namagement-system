from django.db.models import Q
from rest_framework import status, viewsets

from apps.users.permissions import IsAdminOrReadOnly
from utils.pagination import StandardPageNumberPagination
from utils.response import success_response

from .models import Region
from .serializers import RegionReadSerializer, RegionWriteSerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search")
        if search:
            keyword = search.strip()
            queryset = queryset.filter(
                Q(country_name__icontains=keyword)
                | Q(country_code__icontains=keyword.upper())
            )
        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RegionReadSerializer
        return RegionWriteSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            total = self.paginator.page.paginator.count
            return success_response(
                data=serializer.data,
                message="Fetched successfully",
                total=total,
            )

        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message="Fetched successfully",
            total=len(serializer.data),
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message="Fetched successfully")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        read_serializer = RegionReadSerializer(
            serializer.instance,
            context=self.get_serializer_context(),
        )
        return success_response(
            data=read_serializer.data,
            message="Created successfully",
            status_code=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        read_serializer = RegionReadSerializer(
            serializer.instance,
            context=self.get_serializer_context(),
        )
        return success_response(data=read_serializer.data, message="Updated successfully")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(data=None, message="Deleted successfully")
