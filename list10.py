public function newsStore(Request $request)
{
    $request->validate([
        'title' => 'required|string|max:255',
        'text' => 'required|string',
        'is_paid' => 'nullable|boolean',
        'image' => 'nullable|image|mimes:jpeg,png,jpg,gif,webp|max:5120',
    ]);
    
    $mediaId = null;
    
    if ($request->hasFile('image')) {
        $file = $request->file('image');
        $filename = time() . '_' . $file->getClientOriginalName();
        $mimeType = $file->getMimeType();
        $file->move(storage_path('app/public/news'), $filename);
        
        if (file_exists(storage_path('app/public/news/' . $filename))) {
            $media = Media::create([
                'filename' => 'news/' . $filename,
                'file_type' => $mimeType,
                'description' => $request->title,
            ]);
            $mediaId = $media->id;
        } else {
            return back()->with('error', 'Не удалось сохранить изображение');
        }
    }
    
    $post = Post::create([
        'title' => $request->title,
        'text' => $request->text,
        'media_id' => $mediaId,
        'post_type' => 'news',
        'is_paid' => $request->has('is_paid'),
        'created_at' => now(),
    ]);
    
    return redirect()->route('admin.news')->with('success', 'Новость добавлена');
}
