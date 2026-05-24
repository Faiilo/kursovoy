Schema::table('posts', function (Blueprint $table) {
    			$table->boolean('is_paid')->default(false);
});
