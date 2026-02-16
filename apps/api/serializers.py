from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    generation_mode = serializers.ChoiceField(choices=["strict", "enriched"], default="strict")
    output_level = serializers.ChoiceField(choices=["level2", "level3"], default="level2")
    question = serializers.CharField(required=True, help_text="Question or topic for content generation")
