public function newsDelete($id)
{
    			$post = Post::findOrFail($id);
    			$post->delete();
    
    	return redirect()->route('admin.news')->with('success', 'Новость удалена');
}
