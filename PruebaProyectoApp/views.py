from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Challenge, UserChallenge, UserScore
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
import re



# Create your views here.

@login_required
def reto(request, reto_id):

    challenge = get_object_or_404(Challenge, pk=reto_id)
    current_user = request.user
    cases = []
    
    def assertEquals(received, expected):
        
        message = f'Expected {expected} but received {received}' if received != expected else 'Correct!'
        
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

        
        # Ejecutar el script con los tests
        try:
            exec(normalized_script, globals(), locals())
        except SyntaxError as e:
            print(e)

        totalTests = len(cases)

        # Contar los casos correctos
        correct = len([case for case in cases if case[0] == 'Correct!'])
        failedTests = totalTests - correct

        if correct == totalTests:

            
            # Añadimos un registro a la tabla que relaciona usuarios con retos que han superado.
            user_challenge = UserChallenge(user=current_user, challenge=challenge, solution=solucion)
            try:
                # Obtener el objeto UserChallenge asociado al usuario actual si existe
                user_challenge = UserChallenge.objects.get(user=current_user, challenge=challenge, solution=solucion)

            except UserChallenge.DoesNotExist:
                user_challenge = UserChallenge.objects.create(user=current_user, challenge=challenge, solution=solucion)
                user_challenge.save()

            # Añadir score al player.
            scores = [1,2,3,4,5]
            score_to_add = scores[challenge.difficulty-1]
            try:
                # Obtener el objeto UserScore asociado al usuario actual si existe
                user_score = UserScore.objects.get(user=current_user)

            except UserScore.DoesNotExist:
                # Si no existe un registro, puedes crear uno nuevo con el puntaje inicial
                user_score = UserScore.objects.create(user=current_user, score=score_to_add)

            else:
                # Sumar el puntaje adicional al puntaje existente
                user_score.score += score_to_add
                user_score.save()

            user_challenge.save()
            return render(request, 'reto.html', {'challenge': challenge, 'cases': cases, 'failed': True, 'totalTests': totalTests, 'correct': correct, 'failedTests': failedTests})
        else:
            return render(request, 'reto.html', {'challenge': challenge, 'cases': cases, 'failed': True})
            
    return render(request, 'reto.html', {'challenge': challenge})

def retos(request):
    challenges = [challenge for challenge in Challenge.objects.all() if challenge.is_active]
    return render(request, 'retos.html', {'challenges': challenges})


def log_out(request):
    logout(request)
    return redirect(retos)


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
    
        if user is not None:
            login(request, user)

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