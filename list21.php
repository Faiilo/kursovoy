Gate::define('admin', function (User $user) {
    return $user->is_admin == 1;
});
