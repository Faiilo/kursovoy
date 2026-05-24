def logoutf(request):
    logout(request)
    return redirect('/login/')