public function isAccessible()
{
    			if (!$this->is_paid) {
        			return true;
    			}
    
    			if (!auth()->check()) {
        			return false;
    			}
    
    			$user = auth()->user();
    
    			if (!$user->id_subscription) {
        			return false;
    			}
    
    			$subscription = \App\Models\Subscription::find($user->id_subscription);
    
    			return $subscription && $subscription->status === 'Активна';
}
