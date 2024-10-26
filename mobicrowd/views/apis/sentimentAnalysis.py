# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transformers import pipeline
from ...models.submisson import Comment
from mobicrowd.serializers.submissionSerializers import CommentSerializer
from rest_framework import generics
# Initialize the sentiment analysis pipeline outside the view for efficiency
sentiment_analyzer = pipeline("sentiment-analysis")

class CommentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # Extract content from the validated data
            comment_content = serializer.validated_data['content']

            # Analyze the sentiment of the comment
            sentiment_result = sentiment_analyzer(comment_content)[0]
            sentiment = sentiment_result['label'].lower()  # Get the sentiment label (e.g., 'POSITIVE', 'NEGATIVE')

            # Determine sentiment category
            if sentiment == 'positive':
                sentiment_category = 'positive'
            elif sentiment == 'negative':
                sentiment_category = 'negative'
            else:
                sentiment_category = 'neutral'

            # Create the comment instance with the sentiment
            comment = Comment(
                event=serializer.validated_data['event'],  # Ensure this references the Event instance
                patient=serializer.validated_data['patient'],  # Ensure this references the Patient instance
                content=comment_content,
                sentiment=sentiment_category,
                  # Ensure this field is included if needed
            )
            comment.save()

            # Return the serialized data of the created comment
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EventCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']  # Obtenez l'ID de l'événement à partir des paramètres d'URL
        return Comment.objects.filter(event=event_id).order_by('-created_at')  # Filtrer par événement et trier par date de création