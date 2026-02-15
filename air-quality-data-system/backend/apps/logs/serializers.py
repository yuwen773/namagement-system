from rest_framework import serializers

from .models import ImportTask, ImportTaskLog


class ImportTaskSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    class Meta:
        model = ImportTask
        fields = [
            "task_id",
            "file_name",
            "file_type",
            "status",
            "total_count",
            "success_count",
            "failed_count",
            "start_time",
            "end_time",
            "initiator",
            "progress",
        ]
        read_only_fields = fields

    def get_progress(self, obj: ImportTask) -> float:
        if obj.total_count <= 0:
            return 0.0
        done = obj.success_count + obj.failed_count
        return min(1.0, float(done) / float(obj.total_count))


class ImportTaskLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportTaskLog
        fields = [
            "row_number",
            "error_reason",
            "raw_data_snippet",
            "created_at",
        ]
        read_only_fields = fields

