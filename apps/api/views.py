import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from apps.api.serializers import FileUploadSerializer
from apps.tasks.celery_tasks import process_slides_task
from celery.result import AsyncResult

class SlideRAGAPIView(APIView):
    """
    API to upload slides and trigger async LangGraph pipeline via Celery.
    """

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            print(f"Received file: {uploaded_file.name}, size: {uploaded_file.size} bytes")
            generation_mode = serializer.validated_data['generation_mode']
            print(f"Generation mode: {generation_mode}")
            output_level = serializer.validated_data['output_level']
            print(f"Output level: {output_level}")
            question = serializer.validated_data['question']
            print(f"Question: {question}")

            # Save uploaded file locally
            filename = f"{uuid.uuid4()}_{uploaded_file.name}"
            upload_path = os.path.join(settings.MEDIA_ROOT, filename)
            print(f"Saving uploaded file to: {upload_path}")
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            with open(upload_path, 'wb+') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            try:
                # Trigger async Celery task that executes LangGraph
                task = process_slides_task.delay(
                    file_path=upload_path,
                    question=question,
                    generation_mode=generation_mode,
                    output_level=output_level
                )

                return Response(
                    {
                        "task_id": task.id,
                        "status": "submitted",
                        "message": "Slides are being processed asynchronously. Poll task-status endpoint for PDF download."
                    },
                    status=status.HTTP_202_ACCEPTED
                )

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskStatusAPIView(APIView):
    """
    API to check the status of a Celery task and retrieve the PDF when ready.
    """

    def get(self, request, task_id):
        task_result = AsyncResult(task_id)

        if task_result.state == "PENDING":
            return Response({"status": "pending"}, status=status.HTTP_200_OK)
        elif task_result.state == "STARTED":
            return Response({"status": "in_progress"}, status=status.HTTP_200_OK)
        elif task_result.state == "FAILURE":
            return Response({"status": "failed", "error": str(task_result.info)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif task_result.state == "SUCCESS":
            result = task_result.get()
            pdf_filename = os.path.basename(result.get("pdf_filename"))
            pdf_url = request.build_absolute_uri(f"/media/{pdf_filename}")
            return Response({
                "status": "success",
                "pdf_filename": pdf_filename,
                "pdf_url": pdf_url
            }, status=status.HTTP_200_OK)
        else:
            return Response({"status": task_result.state}, status=status.HTTP_200_OK)
