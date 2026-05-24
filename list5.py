@login_required
def generate_all_documents(request):
    """
    Генерация всех документов (титульный лист, задание, дневник) и упаковка в ZIP
    """
    from datetime import datetime
    import tempfile
    import os
    import zipfile
    from io import BytesIO
    
    # Получаем данные пользователя
    user_report = get_object_or_404(DatasetOtchet, user=request.user)
    
    # Проверяем, что у пользователя заполнены обязательные поля
    if not user_report.familia or not user_report.name:
        messages.error(request, 'Пожалуйста, заполните фамилию и имя в профиле перед генерацией документов.')
        return redirect('/profile/')
    
    # Проверяем наличие всех шаблонов
    templates = {
        'title': DocumentTemplate.objects.filter(doc_type='title').first(),
        'assignment': DocumentTemplate.objects.filter(doc_type='assignment').first(),
        'diary': DocumentTemplate.objects.filter(doc_type='diary').first(),
    }
    
    missing_templates = [name for name, tmpl in templates.items() if not tmpl]
    if missing_templates:
        messages.error(request, f'Отсутствуют шаблоны: {", ".join(missing_templates)}. Обратитесь к администратору.')
        return redirect('/profile/')
    
    # Функция для разбора даты
    def parse_date(date_string):
        if not date_string:
            return {'day': '', 'month': '', 'year': ''}
        try:
            if '.' in date_string:
                parts = date_string.split('.')
                if len(parts) == 3:
                    return {
                        'day': parts[0],
                        'month': parts[1],
                        'year': parts[2]
                    }
            elif '-' in date_string:
                parts = date_string.split('-')
                if len(parts) == 3:
                    return {
                        'day': parts[2],
                        'month': parts[1],
                        'year': parts[0]
                    }
        except:
            pass
        return {'day': '', 'month': '', 'year': ''}
    
    # Разбираем даты
    date_begin_parts = parse_date(user_report.date_begin)
    date_finish_parts = parse_date(user_report.date_finish)
    
    # Названия месяцев на русском
    months = {
        '01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля',
        '05': 'мая', '06': 'июня', '07': 'июля', '08': 'августа',
        '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'
    }
    
    month_begin_text = months.get(date_begin_parts['month'], date_begin_parts['month'])
    month_finish_text = months.get(date_finish_parts['month'], date_finish_parts['month'])

    # Получаем полное название модуля и его код
    module_full = user_report.module or ''
    module_code_match = re.search(r'ПМ\.\d+', module_full)
    module_code = module_code_match.group(0) if module_code_match else module_full
    
    # Получаем тип практики
    prac_type_name = user_report.prac_type.type_name if user_report.prac_type else 'Производственная'
    
    # Преобразуем тип практики для разных мест
    prac_type_for_title = normalize_prac_type_for_title(prac_type_name)
    prac_type_genitive = normalize_prac_type_for_sentence(prac_type_name, case='genitive')
    prac_type_dative = normalize_prac_type_for_sentence(prac_type_name, case='dative')
    prac_type_accusative = normalize_prac_type_for_accusative(prac_type_name)
    
    # Полное ФИО
    full_name = f"{user_report.familia} {user_report.name} {user_report.otchestvo}".strip()
    
    # ФИО в разных падежах
    full_name_genitive = to_genitive_simple(full_name)
    full_name_dative = to_dative_simple(full_name)
    
    # Сокращенные ФИО для руководителей
    head1_short = shorten_fio(user_report.head1)
    head2_short = shorten_fio(user_report.head2)
    ruc_pract_short = shorten_fio(user_report.ruc_pract)
    
    # Форматированные даты
    date_begin_formatted = format_date_for_doc(user_report.date_begin)
    date_finish_formatted = format_date_for_doc(user_report.date_finish)
    
    # Получаем компоненты дат
    begin_day = get_day_from_date(user_report.date_begin)
    begin_month = get_month_name_from_date(user_report.date_begin)
    begin_year = get_year_from_date(user_report.date_begin)
    
    finish_day = get_day_from_date(user_report.date_finish)
    finish_month = get_month_name_from_date(user_report.date_finish)
    finish_year = get_year_from_date(user_report.date_finish)
    
    # ФУНКЦИЯ ДЛЯ ОЧИСТКИ ДАННЫХ
    def clean_text(text):
        """Очищает текст от символов, которые могут повредить DOCX"""
        if not text:
            return ""
        # Преобразуем в строку
        text = str(text)
        # Удаляем недопустимые символы для XML
        import re
        # Удаляем control characters кроме \n, \r, \t
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        # Ограничиваем длину (Word может не выдержать слишком длинные строки)
        if len(text) > 5000:
            text = text[:5000] + "..."
        return text
    
    # Подготовка данных для шаблона с очисткой
    context = {
        'fio': clean_text(full_name),
        'familia': clean_text(user_report.familia or ''),
        'name': clean_text(user_report.name or ''),
        'otchestvo': clean_text(user_report.otchestvo or ''),
        'fio_genitive': clean_text(full_name_genitive),
        'fio_dative': clean_text(full_name_dative),
        'tip': clean_text(prac_type_name),
        'tip_title': clean_text(prac_type_for_title),
        'tip_genitive': clean_text(prac_type_genitive),
        'tip_dative': clean_text(prac_type_dative),
        'tip_accusative': clean_text(prac_type_accusative),
        'mdk': clean_text(user_report.mdk or ''),
        'head1': clean_text(user_report.head1 or '_________________________'),
        'head2': clean_text(user_report.head2 or '_________________________'),
        'ruc_pract': clean_text(user_report.ruc_pract or '_________________________'),
        'head1_short': clean_text(head1_short or '_________________________'),
        'head2_short': clean_text(head2_short or '_________________________'),
        'ruc_pract_short': clean_text(ruc_pract_short or '_________________________'),
        'module': clean_text(module_full),
        'module_code': clean_text(module_code),
        'specialization': clean_text(user_report.specialization or '09.02.07 "Информационные системы и программирование"'),
        'kurs': clean_text(str(user_report.kurs or '2')),
        'group': clean_text(user_report.group or ''),
        'date_begin': clean_text(user_report.date_begin or ''),
        'date_finish': clean_text(user_report.date_finish or ''),
        'day_begin': clean_text(date_begin_parts['day']),
        'mesto': clean_text(user_report.mesto or ''),
        'address': clean_text(user_report.address or ''),
        'month_begin': clean_text(month_begin_text),
        'year_begin': clean_text(date_begin_parts['year']),
        'day_finish': clean_text(date_finish_parts['day']),
        'month_finish': clean_text(month_finish_text),
        'year_finish': clean_text(date_finish_parts['year']),
        'date_begin_formatted': clean_text(date_begin_formatted),
        'date_finish_formatted': clean_text(date_finish_formatted),
        'begin_day': clean_text(begin_day),
        'begin_month': clean_text(begin_month),
        'begin_year': clean_text(begin_year),
        'finish_day': clean_text(finish_day),
        'finish_month': clean_text(finish_month),
        'finish_year': clean_text(finish_year),
        'year': clean_text(str(user_report.year or datetime.now().year)),
        'username': clean_text(request.user.username),
        'name_org': clean_text('ГБПОУ МО «Люберецкий техникум имени Героя Советского Союза, летчика-космонавта Ю.А.Гагарина»'),
        'address_org': clean_text('Московская область, г. Люберцы'),
        'phone_org': clean_text('+7 (495) XXX-XX-XX'),
        'email_org': clean_text('info@lubertsy-teh.ru'),
        'sphere': clean_text('Профессиональное образование'),
        'year_foundation': clean_text('19XX'),
        'form_ownership': clean_text('Государственное бюджетное учреждение'),
        'hours': clean_text(str(user_report.hours or '36')),
        'history_org': clean_text('_________________________'),
        'godovoy_otchet': clean_text('_________________________'),
        'uslugi_org': clean_text('Образовательные услуги по подготовке специалистов СПО'),
        'achievments_org': clean_text('_________________________'),
        'name_docher': clean_text('_________________________'),
        'address_docher': clean_text('_________________________'),
        'phone_docher': clean_text('_________________________'),
        'email_docher': clean_text('_________________________'),
        'name_podrazdel': clean_text('Отдел информационных технологий'),
        'head_podrazdel': clean_text('_________________________'),
        'fio_head_practice': clean_text(user_report.ruc_pract or '_________________________'),
        'kurator_phone': clean_text('_________________________'),
        'kurator_email': clean_text('_________________________'),
        'struk_and_func': clean_text('_________________________'),
        'goal_pract': clean_text(f'{prac_type_genitive} практической подготовки'),
        'prof_kompetentsii': clean_text('''
- ПК 11.1 Осуществлять сбор, обработку и анализ информации для проектирования баз данных
- ПК 11.2 Проектировать базу данных на основе анализа предметной области
- ПК 11.3 Разрабатывать объекты базы данных в соответствии с результатами анализа предметной области
- ПК 11.4 Реализовывать базу данных в конкретной системе управления базами данных
- ПК 11.5 Администрировать базы данных
- ПК 11.6 Защищать информацию в базе данных с использованием технологии защиты информации
        '''),
        'obsh_kompetentsii': clean_text('''
- ОК 01. Выбирать способы решения задач профессиональной деятельности применительно к различным контекстам
- ОК 02. Использовать современные средства поиска, анализа и интерпретации информации 
- ОК 03. Планировать и реализовывать собственное профессиональное и личностное развитие
- ОК 04. Эффективно взаимодействовать и работать в коллективе и команде
- ОК 05. Осуществлять устную и письменную коммуникацию на государственном языке
- ОК 06. Проявлять гражданско-патриотическую позицию, демонстрировать осознанное поведение
- ОК 07. Содействовать сохранению окружающей среды, ресурсосбережению
- ОК 08. Использовать средства физической культуры для сохранения и укрепления здоровья
- ОК 09. Пользоваться профессиональной документацией на государственном и иностранном языках
        '''),
    }
    
    doc_names_map = {
        'title': 'Титульный_лист',
        'assignment': 'Задание',
        'diary': 'Дневник'
    }
    
    try:
        # Создаем ZIP архив в памяти
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Генерируем каждый документ
            for doc_type, template_obj in templates.items():
                if not template_obj:
                    continue
                
                template_path = template_obj.template_file.path
                
                # Создаем временный файл для документа
                with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
                    tmp_path = tmp_file.name
                
                try:
                    # Рендерим документ
                    doc = DocxTemplate(template_path)
                    doc.render(context)
                    doc.save(tmp_path)
                    
                    # Проверяем, что файл не пустой
                    if os.path.getsize(tmp_path) < 100:
                        raise Exception(f"Файл {doc_type} слишком маленький, возможно ошибка рендеринга")
                    
                    # Читаем файл
                    with open(tmp_path, 'rb') as f:
                        docx_data = f.read()
                    
                    # Добавляем в ZIP
                    inner_name = f"{doc_names_map.get(doc_type, doc_type)}_{user_report.familia}_{user_report.name}.docx"
                    inner_name = "".join(c for c in inner_name if c.isalnum() or c in '._- ')
                    zip_file.writestr(inner_name, docx_data)
                    
                except Exception as e:
                    print(f"Ошибка при генерации {doc_type}: {e}")
                    # Продолжаем с другими документами
                    
                finally:
                    # Удаляем временный файл
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
        
        # Проверяем, что ZIP не пустой
        if zip_buffer.getbuffer().nbytes < 100:
            messages.error(request, 'Ошибка: не удалось сгенерировать документы. Проверьте шаблоны.')
            return redirect('/profile/')
        
        # Формируем имя ZIP файла
        zip_filename = f"Документы_практики_{user_report.familia}_{user_report.name}.zip"
        zip_filename = "".join(c for c in zip_filename if c.isalnum() or c in '._- ')
        
        # Отправляем ZIP файл
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
        response['Content-Length'] = len(zip_buffer.getvalue())
        
        return response