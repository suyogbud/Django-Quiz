from typing import Any
from django.db.models import F
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from random import choice
from django.contrib.auth.decorators import login_required
import random

from .forms import SignUpForm
from .models import Choice, Question, UserScore

class IndexView(generic.ListView):
    # Return the latest 5 questions
    template_name = "quiz/index.html"
    context_object_name = "latest_question_list"

    # Function to get the latest 5 questions 
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    # Return the question and its choices
    model = Question
    # Return the question and its choices
    template_name = "quiz/detail.html"
    # Get the question and its choices
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    # Return the question and its choices
    model = Question
    # Return the question and its choices
    template_name = "quiz/results.html"

    # Get the question and its choices
    def get_context_date(self, **kwargs):
        # Get the question and its choices
        context = super().get_context_data(**kwargs)
        # Get the selected choice AND the correct choice
        context['correct_choice'] = self.get_object().choice_set.filter(correct=True).first()
        # Return the context
        return context

# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return render(request, "quiz/index.html", context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "quiz/detail.html", {"question": question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "quiz/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request,
            "quiz/detail.html",
            {
                "question":question,
                "error_message": "You didn't select a choice",
            }
        )
    else:
        # selected_choice.votes = F("votes") + 1
        # selected_choice.save()

        # return HttpResponseRedirect(reverse("quiz:results", args=(question.id,)))

        # selected_choice.votes += 1
        # selected_choice.save()

        # Check if the selected choice is correct
        # is_correct = selected_choice.correct

        selected_choice.votes += 1
        selected_choice.save()

        #make sure the selected choice is correct
        is_correct = selected_choice.correct


        # Save the attempted question and correctness check result in the session
        if 'attempted_questions' not in request.session:
            request.session['attempted_questions'] = []

        # Save the correct answers in the session

        if 'correct_answers' not in request.session:
            request.session['correct_answers'] = 0

        # Save the attempted question and correctness check result in the session
        
        request.session['attempted_questions'].append(question_id)
        if is_correct:
            request.session['correct_answers'] += 1
        request.session.modified = True

        # Pass the correctness check result to the template
        return render(request, 'quiz/results.html', {
            'question': question,
            'selected_choice': selected_choice,
            'is_correct': is_correct,
        })

def signup(request):
    #add the signup form
    if request.method == "POST":
        form = SignUpForm(request.POST)
        #check if the form is valid
        if form.is_valid():
            form.save()
            #redirect to the login page
            return redirect("login")
    else:
        #display the form
        form = SignUpForm()
    #return the form
    return render(request, "registration/signup.html", {"form": form})

def flush(request):
    # Clear the session
    request.session.flush()
    # Redirect to the start_quiz view
    return redirect('quiz:start_quiz')

@login_required
def start_quiz(request):
    # Debug: clear session for debugging purposes

    if 'attempted_questions' not in request.session:
        request.session['attempted_questions'] = []
    if 'correct_answers' not in request.session:
        request.session['correct_answers'] = 0

    #get all unattempted questions
    attempted_questions = request.session['attempted_questions']
    all_questions = list(Question.objects.values_list('id', flat=True))

    print(f"Attempted Questions: {attempted_questions}")
    print(f"All Questions: {all_questions}")

    # Check if all questions have been attempted    

    if len(attempted_questions) >= len(all_questions):
        correct_answers = request.session['correct_answers']
        total_questions = len(all_questions)
        percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

                # Save the score in the database
        UserScore.objects.create(user=request.user, score=percentage)

        # Calculate average, highest, and lowest scores
        scores = UserScore.objects.filter(user=request.user).values_list('score', flat=True)
        # calculate the highest, lowest, and average scores
        highest_score = max(scores) if scores else 0
        lowest_score = min(scores) if scores else 0
        average_score = sum(scores) / len(scores) if scores else 0

        #return the completion page with the scores
        return render(request, 'quiz/completion.html',{
            'correct_answers': correct_answers,
            'total_questions': total_questions,
            'percentage': percentage,
            'highest_score': highest_score,
            'lowest_score': lowest_score,
            'average_score': average_score,
        })

    # Get the next question
    unattempted_questions = list(set(all_questions) - set(attempted_questions))
    next_question_id = choice(unattempted_questions)
    
    # Redirect to the next question frontend page
    return redirect('quiz:detail', pk=next_question_id)

@login_required
def random(request):
    questions = Question.objects.all()
    if questions:
        random_question = choice(questions)
        return HttpResponseRedirect(reverse("quiz:detail", args=(random_question.id,) ))    
    else:
        return render(request, "quiz.no_question.html", {'error': "No questions available."})
    
