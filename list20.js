public function store(LoginRequest $request)
{
    $request->authenticate();
    $request->session()->regenerate();

    return redirect()->intended('/');
}
