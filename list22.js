public function show($id)
{
    $post = Post::where('post_type', 'news')->findOrFail($id);
    
    if ($post->is_paid && !$post->isAccessible()) {
        return view('news.paid_required', compact('post'));
    }
    
    return view('news.show', compact('post'));
}
