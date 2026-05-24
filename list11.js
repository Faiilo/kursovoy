public function newsUpdate(Request $request, $id)
{
    $post = Post::findOrFail($id);
    
    $request->validate([
        'title' => 'required|string|max:255',
        'text' => 'required|string',
        'is_paid' => 'nullable|boolean',
        'image' => 'nullable|image|mimes:jpeg,png,jpg,gif,webp|max:5120',
    ]);
    
    // Удаление старого изображения
    if ($request->has('delete_image') && $post->media_id) {
        $oldMedia = Media::find($post->media_id);
        if ($oldMedia) {
            $oldPath = storage_path('app/public/' . $oldMedia->filename);
            if (file_exists($oldPath)) {
                unlink($oldPath);
            }
            $oldMedia->delete();
        }
        $post->media_id = null;
    }
    
    // Загрузка нового изображения
    if ($request->hasFile('image')) {
        $file = $request->file('image');
        $filename = time() . '_' . $file->getClientOriginalName();
        $mimeType = $file->getMimeType();
        
        if ($post->media_id) {
            $oldMedia = Media::find($post->media_id);
            if ($oldMedia) {
                $oldPath = storage_path('app/public/' . $oldMedia->filename);
                if (file_exists($oldPath)) {
                    unlink($oldPath);
                }
                $oldMedia->delete();
            }
        }
        
        $file->move(storage_path('app/public/news'), $filename);
        
        if (file_exists(storage_path('app/public/news/' . $filename))) {
            $media = Media::create([
                'filename' => 'news/' . $filename,
                'file_type' => $mimeType,
                'description' => $request->title,
            ]);
            $post->media_id = $media->id;
        } else {
            return back()->with('error', 'Не удалось сохранить изображение');
        }
    }
    
    $post->title = $request->title;
    $post->text = $request->text;
    $post->is_paid = $request->has('is_paid');
    $post->save();
    
    return redirect()->route('admin.news')->with('success', 'Новость обновлена');
}
