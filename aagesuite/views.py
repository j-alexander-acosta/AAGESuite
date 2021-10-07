# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages


@login_required()
def home(request):
    return render(request, 'home.html')


def login_view(request):
    """
        Pantalla de Login

    :param request: Django request
    :return: Html Template
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                next = request.GET.get('next', None)
                if next:
                    return HttpResponseRedirect(
                        next
                    )
                else:
                    return redirect(
                        'home'
                    )
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    u'Cuenta inactiva, comuniquese con el administrador'
                )
        else:
            messages.add_message(
                request,
                messages.WARNING,
                u'Error en su contraseña o nombre de usuario, vuelva a intentarlo.'
            )
    else:
        messages.add_message(
            request,
            messages.INFO,
            'Bienvenido!'
        )

    return render(request, 'registration/login2.html')


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')
