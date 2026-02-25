from rest_framework import status, viewsets
from rest_framework.decorators import action

from apps.users.permissions import IsAdminOrReadOnly
from utils.pagination import StandardPageNumberPagination
from utils.response import success_response

from .models import Category
from .serializers import CategoryReadSerializer, CategoryWriteSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.select_related("parent")
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        level = params.get("level")
        if level:
            queryset = queryset.filter(level=level)

        parent_id = params.get("parent_id")
        if parent_id is not None:
            normalized_parent = parent_id.strip().lower()
            if normalized_parent in ("", "null", "none"):
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(parent_id=parent_id)

        name = params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name.strip())

        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CategoryReadSerializer
        return CategoryWriteSerializer

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

        read_serializer = CategoryReadSerializer(
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

        read_serializer = CategoryReadSerializer(
            serializer.instance,
            context=self.get_serializer_context(),
        )
        return success_response(data=read_serializer.data, message="Updated successfully")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(data=None, message="Deleted successfully")

    @action(detail=False, methods=["get"], url_path="tree")
    def tree(self, request, *args, **kwargs):
        categories = list(Category.objects.select_related("parent").order_by("id"))
        node_map = {}

        for category in categories:
            node_map[category.id] = {
                "id": category.id,
                "name": category.name,
                "code": category.code,
                "level": category.level,
                "parent_id": category.parent_id,
                "children": [],
            }

        roots = []
        for category in categories:
            node = node_map[category.id]
            if category.parent_id and category.parent_id in node_map:
                node_map[category.parent_id]["children"].append(node)
            else:
                roots.append(node)

        return success_response(
            data=roots,
            message="Fetched successfully",
            total=len(categories),
        )
