public function userToggleSubscription($id)
{
    $user = User::findOrFail($id);
    
    if ($user->id_subscription) {
        // Отключаем подписку
        $user->id_subscription = null;
        $user->save();
        $message = 'Подписка отключена';
    } else {
        // Включаем подписку
        $sub = Subscription::firstOrCreate(['id' => 1], ['status' => 'Активна']);
        $user->id_subscription = $sub->id;
        $user->save();
        $message = 'Подписка включена';
    }
    
    return redirect()->route('admin.users')->with('success', $message);
}
