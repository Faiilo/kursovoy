def register(request):
    if request.method == "GET":
        return render(request, "register.html", {"form": UserCreationForm()})
    else: 
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                request.POST['username'],
                password=request.POST['password1']
            )
            user.save()
            DatasetOtchet.objects.create(user=user)
            login(request, user)
            return redirect('/profile/')
        else:
            messages.error(request, 'Пароли не совпадают')
            return render(request, "register.html", {"form": UserCreationForm()})