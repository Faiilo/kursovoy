@login_required
def profile(request):
    user_report, created = DatasetOtchet.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if request.POST.get('familia'):
            user_report.familia = request.POST['familia']
        if request.POST.get('name'):
            user_report.name = request.POST['name']
        if request.POST.get('otchestvo'):
            user_report.otchestvo = request.POST['otchestvo']
        if request.POST.get('tip'):
            try:
                user_report.prac_type = PracType.objects.get(type_name=request.POST['tip'])
            except PracType.DoesNotExist:
                pass
        if request.POST.get('module'):
            user_report.module = request.POST['module']
        if request.POST.get('specialization'):
            user_report.specialization = request.POST['specialization']
        if request.POST.get('kurs'):
            user_report.kurs = request.POST['kurs']
        if request.POST.get('group'):
            user_report.group = request.POST['group']
        if request.POST.get('hours'):
            try:
                user_report.hours = int(request.POST['hours'])
            except ValueError:
                user_report.hours = None
        if request.POST.get('mesto'):
            user_report.mesto = request.POST['mesto']
        if request.POST.get('address'):
            user_report.address = request.POST['address']
        if request.POST.get('mdk'):
            user_report.mdk = request.POST['mdk']
        if request.POST.get('begin_date'):
            date_parts = request.POST['begin_date'].split('-')
            if len(date_parts) == 3:
                user_report.date_begin = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
        if request.POST.get('finish_date'):
            date_parts = request.POST['finish_date'].split('-')
            if len(date_parts) == 3:
                user_report.date_finish = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
        if request.POST.get('head1'):
            user_report.head1 = request.POST['head1']
        if request.POST.get('head2'):
            user_report.head2 = request.POST['head2']
        if request.POST.get('ruc_pract'):
            user_report.ruc_pract = request.POST['ruc_pract']
        if request.POST.get('year'):
            user_report.year = request.POST['year']
        
        user_report.save()
        messages.success(request, 'Данные успешно сохранены!')
        return redirect('/profile/')
    
    # Обработка GET запроса (показываем форму)
    begin_date_for_input = ''
    finish_date_for_input = ''
    
    if user_report.date_begin:
        try:
            date_parts = user_report.date_begin.split('.')
            if len(date_parts) == 3:
                begin_date_for_input = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
        except:
            pass
    
    if user_report.date_finish:
        try:
            date_parts = user_report.date_finish.split('.')
            if len(date_parts) == 3:
                finish_date_for_input = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
        except:
            pass
    
    prac_types = PracType.objects.all()
    
    # Проверяем наличие шаблонов
    templates_exist = {
        'title': DocumentTemplate.objects.filter(doc_type='title').exists(),
        'assignment': DocumentTemplate.objects.filter(doc_type='assignment').exists(),
        'diary': DocumentTemplate.objects.filter(doc_type='diary').exists(),
    }
    
    return render(request, "profile.html", {
        "user_report": user_report,
        "prac_types": prac_types,
        "begin_date_for_input": begin_date_for_input,
        "finish_date_for_input": finish_date_for_input,
        "templates_exist": templates_exist
    })
    user_report, created = DatasetOtchet.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if request.POST.get('familia'):
            user_report.familia = request.POST['familia']
        if request.POST.get('name'):
            user_report.name = request.POST['name']
        if request.POST.get('otchestvo'):
            user_report.otchestvo = request.POST['otchestvo']
        if request.POST.get('tip'):
            try:
                user_report.prac_type = PracType.objects.get(type_name=request.POST['tip'])
            except PracType.DoesNotExist:
                pass
        if request.POST.get('module'):
            user_report.module = request.POST['module']
        if request.POST.get('specialization'):
            user_report.specialization = request.POST['specialization']
        if request.POST.get('kurs'):
            user_report.kurs = request.POST['kurs']
        if request.POST.get('group'):
            user_report.group = request.POST['group']
        if request.POST.get('hours'):
            try:
                user_report.hours = int(request.POST['hours'])
            except ValueError:
                user_report.hours = None
        if request.POST.get('mesto'):
            user_report.mesto = request.POST['mesto']
        if request.POST.get('address'):
            user_report.address = request.POST['address']
        if request.POST.get('mdk'):  # НОВОЕ ПОЛЕ
            user_report.mdk = request.POST['mdk']
        if request.POST.get('begin_date'):
            date_parts = request.POST['begin_date'].split('-')
            if len(date_parts) == 3:
                user_report.date_begin = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
        if request.POST.get('finish_date'):
            date_parts = request.POST['finish_date'].split('-')
            if len(date_parts) == 3:
                user_report.date_finish = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
        if request.POST.get('head1'):
            user_report.head1 = request.POST['head1']
        if request.POST.get('head2'):
            user_report.head2 = request.POST['head2']
        if request.POST.get('ruc_pract'):
            user_report.ruc_pract = request.POST['ruc_pract']
        if request.POST.get('year'):
            user_report.year = request.POST['year']
        
        user_report.save()
        messages.success(request, 'Данные успешно сохранены!')
        return redirect('/profile/')