from rest_framework import status, viewsets

from apps.users.permissions import IsAdminOrReadOnly
from utils.pagination import StandardPageNumberPagination
from utils.response import success_response

from .models import HeritageItem
from .serializers import HeritageItemReadSerializer, HeritageItemWriteSerializer


class HeritageItemViewSet(viewsets.ModelViewSet):
    queryset = HeritageItem.objects.select_related("category", "region")
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        category = params.get("category")
        if category:
            queryset = queryset.filter(category_id=category)

        level = params.get("level")
        if level:
            queryset = queryset.filter(level=level)

        region = params.get("region")
        if region:
            queryset = queryset.filter(region_id=region)

        name = params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name.strip())

        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return HeritageItemReadSerializer
        return HeritageItemWriteSerializer

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

        read_serializer = HeritageItemReadSerializer(
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

        read_serializer = HeritageItemReadSerializer(
            serializer.instance,
            context=self.get_serializer_context(),
        )
        return success_response(data=read_serializer.data, message="Updated successfully")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(data=None, message="Deleted successfully")
