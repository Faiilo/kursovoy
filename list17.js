public function hasActiveSubscription()
{
    return $this->id_subscription && 
           $this->subscription && 
           $this->subscription->status === 'Активна';
}
