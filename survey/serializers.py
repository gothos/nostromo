from rest_framework import serializers
from survey.models import UserSurvey,Question,Survey,Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('answer_text',)

class QuestionSerializer(serializers.ModelSerializer):
    question= serializers.ReadOnlyField(source='question_text')
    type = serializers.ReadOnlyField(source='type.text')
    #choices = serializers.ReadOnlyField(source='possible_answers')
    class Meta:
        model = Question
        fields = ('id','question','type',)

    def to_representation(self, instance):
        k = super().to_representation(instance)
        user_id = self._kwargs['context']['user_id']
        objs = Answer.objects.filter(user_id=user_id,question=instance)
        if instance.possible_answers:
            k['choices'] = instance.possible_answers
        if objs.exists():
            serializer = AnswerSerializer(objs.last())
            k['answer'] = serializer.data['answer_text']
        return k


class SurveysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey

class QuestionRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        if 'request' in self.root.context.keys():
            idx = self.root.context['request'].user.id
            context = {'user_id':idx}
        else:
            context = self.root.get_extra_kwargs()
        serializer = QuestionSerializer(value,context=context)
        return serializer.data


class UserSurveysSerializer(serializers.ModelSerializer):

    title = serializers.ReadOnlyField(source='survey.title')
    id = serializers.ReadOnlyField(source='survey.id')
    questions_count = serializers.ReadOnlyField(source='get_questions_count')
    questions = QuestionRelatedField(source='get_questions_list',read_only=True,many=True)

    class Meta:
        model = UserSurvey
        fields = ('id','title','passed_at','questions_count','questions',)


    def get_extra_kwargs(self):
        k = super().get_extra_kwargs()
        if self.instance:
            if isinstance(self.instance,list):
                k['user_id'] = self.instance[0].user.id
            else:
                k['user_id'] = self.instance.user.id
        return k


