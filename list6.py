def to_genitive_simple(full_name):
    """Преобразует ФИО в родительный падеж"""
    def transform_last_name(name):
        if name.endswith('ко'):  # Филенко → Филенко (не склоняется)
            return name
        if name.endswith('ий'):  # Дмитрий → Дмитрия
            return name[:-2] + 'ия'
        return name + 'а'
    
    def transform_first_name(name):
        exceptions = {'дмитрий': 'дмитрия', 'илья': 'ильи'}
        if name.lower() in exceptions:
            return exceptions[name.lower()].capitalize()
        if name.endswith('ий'):
            return name[:-2] + 'ия'
        return name + 'а'
    
    parts = full_name.split()
    result = [transform_last_name(parts[0])]
    if len(parts) >= 2:
        result.append(transform_first_name(parts[1]))
    if len(parts) >= 3:
        result.append(parts[2] + 'а')
    return " ".join(result)

def normalize_prac_type_for_title(prac_type):
    """Производственная → ПРОИЗВОДСТВЕННОЙ"""
    if prac_type.lower() == "производственная":
        return "ПРОИЗВОДСТВЕННОЙ"
    return "УЧЕБНОЙ"