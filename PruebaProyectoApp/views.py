from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Challenge, UserChallenge
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

        
        # Ejecutar el script con los tests
        exec(normalized_script, globals(), locals())
        totalTests = len(cases)

        # Contar los casos correctos
        correct = len([result for result in cases if result[0] == 'Correct!'])

        if correct == totalTests:
            # Añadimos un registro a la tabla que relaciona usuarios con retos que han superado.
            nuevo_registro = UserChallenge(user=current_user, challenge=challenge)
            nuevo_registro.save()
            return render(request, 'retoLogrado.html', {'challenge': challenge, 'cases': cases})
        else:
            return render(request, 'retoLogrado.html', {'challenge': challenge, 'cases': cases})
            
    return render(request, 'reto.html', {'challenge': challenge})

def retos(request):
    challenges = Challenge.objects.all()
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
        descripcion = request.POST.get('descripcion')
        tests = request.POST.get('tests')
        template = request.POST.get('template')
        created_at = datetime.now()
        total_tests = request.POST.get('total-tests')

        current_user = request.user

    #         title = models.CharField(max_length=255)
    # description = models.TextField()
    # code_template = models.TextField()
    # test_cases = models.TextField()
    # total_tests = models.IntegerField(default=0)
    # created_at = models.DateTimeField(auto_now_add=True)
    # creator = models.ForeignKey(User, on_delete=models.CASCADE)
        
        # Crear un nuevo registro en la base de datos
        nuevo_registro = Challenge(
            title=titulo, description=descripcion, code_template=template, test_cases=tests, created_at=created_at, creator=current_user,
            total_tests=total_tests
            )
        nuevo_registro.save()
        
        # Redirigir al usuario a otra página
        # return redirect('otra_vista')
        
    # Renderizar el template correspondiente
    return render(request, 'crea_challenge.html')