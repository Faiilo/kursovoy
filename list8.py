def loginf(request): 
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Вы вошли как {username}')
                return redirect('/profile/')
            else:
                messages.error(request, 'Неправильное имя пользователя или пароль')
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль')
    
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})