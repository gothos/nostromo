from django.contrib.postgres.fields import JSONField
from django.db import models

class Survey(models.Model):
    title = models.CharField(max_length=128)

    def __unicode__(self):
        return '%s' % self.title


class UserSurvey(models.Model):
    survey = models.ForeignKey(Survey)
    user = models.ForeignKey("account.User")
    passed_at = models.DateTimeField(null=True, blank=True)
    new = models.BooleanField(default=True)

    def get_questions_count(self):
        return self.survey.question_set.all().count()
    def get_questions_list(self):
        qs = self.survey.question_set.all()
        return qs


class QuestionType(models.Model):
    idx = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=128)


class Question(models.Model):
    survey = models.ForeignKey(Survey)
    question_text = models.CharField(max_length=256)
    type = models.ForeignKey(QuestionType)
    possible_answers = JSONField(null=True, blank=True)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey("account.User")
    answer_text = models.CharField(max_length=256)
