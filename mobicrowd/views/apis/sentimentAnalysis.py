import re 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transformers import pipeline
from ...models.submisson import Comment
from mobicrowd.serializers.submissionSerializers import CommentSerializer
from rest_framework import generics

# Initialize the sentiment analysis and chatbot pipelines outside the view for efficiency
sentiment_analyzer = pipeline("sentiment-analysis")
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-small", pad_token_id=50256)

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
            sentiment_category = sentiment if sentiment in ['positive', 'negative'] else 'neutral'

            # Create the comment instance with the sentiment
            comment = Comment(
                event=serializer.validated_data['event'],  # Ensure this references the Event instance
                patient=serializer.validated_data['patient'],  # Ensure this references the Patient instance
                content=comment_content,
                sentiment=sentiment_category,  # Ensure this field is included if needed
            )
            comment.save()

            # Return the serialized data of the created comment
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']  # Get the event ID from the URL parameters
        return Comment.objects.filter(event=event_id).order_by('-created_at')  # Filter by event and order by creation date

def preprocess_message(message):
    # Basic text cleaning
    message = re.sub(r'\s+', ' ', message).strip()  # Remove extra spaces
    message = message.lower()  # Convert to lowercase
    return message

def generate_follow_up_question(bot_response):
    # Example implementation: Generate a simple follow-up question
    if "symptom" in bot_response.lower():
        return "Can you describe the symptom in more detail?"
    else:
        return "Would you like to ask anything else?"

class ChatbotView(APIView):
    def post(self, request, *args, **kwargs):
        user_message = request.data.get("message", "").strip()
        
        if user_message:
            preprocessed_message = preprocess_message(user_message)

            try:
                response = chatbot(preprocessed_message, max_length=150, truncation=True, num_return_sequences=1)
                bot_response = response[0]["generated_text"].strip()

                # Call the follow-up question function
                follow_up_question = generate_follow_up_question(bot_response)

                return Response({
                    "response": bot_response,
                    "follow_up": follow_up_question
                })
            except Exception as e:
                return Response({"error": "Failed to generate a response"}, status=500)
        else:
            return Response({"error": "Message cannot be empty"}, status=400)
