# apps/lectures/repository.py

from apps.lectures.models import Lecture


class LectureRepository:

    @staticmethod
    def create_lecture(
        namespace: str,
        subject: str,
        topic: str,
        academic_level: str,
        title: str = None,
    ) -> Lecture:

        return Lecture.objects.create(
            namespace=namespace,
            subject=subject,
            topic=topic,
            academic_level=academic_level,
            title=title,
        )

    @staticmethod
    def get_lecture(lecture_id):
        return Lecture.objects.get(id=lecture_id)
