from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Challenge, UserChallenge, UserScore, User, Comment, Response
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
import re
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.db.models import Count




# Create your views here.

def home(request):
    return render(request, 'home.html')


def users(request):
    users = [user for user in User.objects.all()]
    # users_scores = [(user, UserScore.objects.get(user=user).score) for user in users]

    users_scores = []
    for user in users:
        try:
            score = UserScore.objects.get(user=user).score
        except UserScore.DoesNotExist:
            # El objeto UserScore no existe, realizar acciones adicionales o manejar el caso de manera adecuada
            # ...
            score = 0  # Otra asignación o valor predeterminado en caso necesario
        users_scores.append((user, score))
    users_scores = sorted(users_scores, key=lambda x: x[1], reverse=True)
            
    return render(request, 'users.html', {'users_scores': users_scores})


def user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        user_score = UserScore.objects.get(user=user)
    except:
        user_score = None

    score = user_score.score if user_score else 0
    num_retos = UserChallenge.objects.filter(user=user).distinct('challenge').count()
    user_challenges = UserChallenge.objects.filter(user=user).distinct('challenge')
    challenges = [userchallenge.challenge for userchallenge in user_challenges]
    challenges_dict = {}
    
    for challenge in challenges:
        user_challenges_all = UserChallenge.objects.filter(user=user, challenge=challenge)
        challenges_dict[challenge] = [user_challenge.solution for user_challenge in user_challenges_all]
    
    print(challenges_dict)
    authored_challenges = Challenge.objects.filter(creator=user)
    return render(request, 'user_profile.html', {'user': user, 'visitor': request.user, 'score': score, 'num_retos': num_retos, 'authored_challenges': authored_challenges, 'challenges_dict': challenges_dict})


@login_required
def your_profile(request):
    return render(request, 'user_profile.html', {'user': request.user})


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', { 'form': form})
    
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('retos')
        else:
            return render(request, 'register.html', {'form': form})


def not_found(request, url):
    return render(request, 'not_found.html')

@login_required
def reto(request, reto_id):

    challenge = get_object_or_404(Challenge, pk=reto_id)
    current_user = request.user
    cases = []
    
    def assertEquals(received, expected):
        
        message = 'Incorrect...' if received != expected else 'Correct!'
        
        cases.append((message, received, expected))

        return received == expected
    
    def normalize_code(code):

        # Elimina los saltos de línea y los espacios en blanco innecesarios al principio y final del código
        code = code.strip()

        # Elimina los tabs y los sustituye por 4 espacios
        code = code.replace('\t', '    ')

        # Normaliza los saltos de línea
        code = re.sub('\r\n|\r|\n', '\n', code)

        return code


    if request.method == 'POST':

        # Obtener los datos del formulario enviado por el usuario
        solucion = request.POST.get('codigo')
        tests = challenge.test_cases
        
        script = solucion + '\n' + tests
        normalized_script = normalize_code(script)

        print(script)
        print(normalized_script)

        excepcion = None
        
        # Ejecutar el script con los tests
        try:
            exec(normalized_script, globals(), locals())
        except Exception as e:
            excepcion = repr(e)

        totalTests = len(cases)

        # Contar los casos correctos
        correct = len([case for case in cases if case[0] == 'Correct!'])
        failedTests = totalTests - correct

        if correct == totalTests:

            score_to_add = 0
            
            try:
                # Obtener el objeto UserChallenge asociado al usuario actual si existe
                user_challenge = UserChallenge.objects.get(user=current_user, challenge=challenge, solution=solucion)

            except UserChallenge.DoesNotExist:
                already_beaten = UserChallenge.objects.filter(user=current_user, challenge=challenge).exists()
                user_challenge = UserChallenge.objects.create(user=current_user, challenge=challenge, solution=solucion)
                # Añadir score al player.
                

                if not already_beaten:
                    scores = [1,2,3,4,5]
                    score_to_add = scores[challenge.difficulty-1]

                user_challenge.save()
            
        
            try:
                # Obtener el objeto UserScore asociado al usuario actual si existe
                user_score = UserScore.objects.get(user=current_user)

            except UserScore.DoesNotExist:
                # Si no existe un registro, puedes crear uno nuevo con el puntaje inicial
                user_score = UserScore.objects.create(user=current_user, score=score_to_add)

            # Sumar el puntaje adicional al puntaje existente
            user_score.score += score_to_add
            user_score.save()

            user_challenge.save()
            return render(request, 'reto.html', {'challenge': challenge, 'cases': cases, 'totalTests': totalTests, 'correct': correct, 'failedTests': failedTests, 'excepcion': excepcion})
        else:
            print(excepcion)
            return render(request, 'reto.html', {'challenge': challenge, 'cases': cases, 'totalTests': totalTests, 'correct': correct, 'failedTests': failedTests, 'excepcion': excepcion})
            
    return render(request, 'reto.html', {'challenge': challenge})


@login_required
def challenge_comments(request, reto_id):

    challenge = get_object_or_404(Challenge, pk=reto_id)

    if request.method == 'POST':
        comment_body = request.POST.get('comment_body')

        if comment_body != '':
            current_user = request.user
            print(comment_body)

            # Crear el comentario
            nuevo_registro = Comment(challenge=challenge, user=current_user, body=comment_body)
            nuevo_registro.save()
            

            # Redirigir nuevamente al reto para evitar el reenvío del formulario
        return redirect('challenge_comments', reto_id=reto_id)

    return render(request, 'challenge_comments.html', {'challenge': challenge})


@login_required
def reto_info(request, reto_id):
    challenge = get_object_or_404(Challenge, pk=reto_id)

    if request.method == 'POST':
        if 'approve' in request.POST:
            challenge.is_active = True
            challenge.save()
            return redirect('challenges_reviews')
        elif 'reject' in request.POST:
            challenge.delete()
            return redirect('challenges_reviews')

    return render(request, 'reto_info.html', {'challenge': challenge})


def retos(request):
    search_term = request.GET.get('search')

    # Filtrar los retos según el término de búsqueda
    if search_term:
        challenges = Challenge.objects.filter(title__icontains=search_term)
    else:
        challenges = Challenge.objects.all()
    
    active_challenges = [challenge for challenge in challenges if challenge.is_active]

    return render(request, 'retos.html', {'challenges': active_challenges})

@login_required
def challenges_reviews(request):
    challenges = [challenge for challenge in Challenge.objects.all() if not challenge.is_active]
    return render(request, 'challenge_reviews.html', {'challenges': challenges})


def log_out(request):
    logout(request)
    return redirect('home')


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('retos')

    return render(request, 'login.html')


@login_required
def crea_challenge(request):
    if request.method == 'POST':
        # Obtener los datos del formulario enviado por el usuario
        titulo = request.POST.get('nombre')
        instrucciones = request.POST.get('instrucciones')
        descripcion = request.POST.get('descripcion')
        dificultad = request.POST.get('dificultad')
        tests = request.POST.get('tests')
        template = request.POST.get('template')
        category = request.POST.get('disciplina')
        created_at = datetime.now()

        current_user = request.user
        
        # Crear un nuevo registro en la base de datos
        nuevo_registro = Challenge(
            title=titulo,
            description=descripcion,
            code_template=template,
            test_cases=tests,
            created_at=created_at,
            creator=current_user,
            difficulty=dificultad,
            instructions=instrucciones,
            category=category
            )
        nuevo_registro.save()
        
        # Redirigir al usuario a otra página
        # return redirect('otra_vista')
        
    # Renderizar el template correspondiente
    return render(request, 'crea_challenge.html')