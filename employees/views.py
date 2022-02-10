from django.shortcuts import render

_employees_list = [
    {"name": "Andres Green", "id": 4, "title": "COO", "manager_id": 2},
    {"name": "Barrett Glasauer", "id": 1, "title": "CTO", "manager_id": 2},
    {"name": "Chris Hancock", "id": 8, "title": "Engineering Lead", "manager_id": 1},
    {"name": "Julian Early", "id": 3, "title": "Engineer", "manager_id": 8},
    {"name": "Michael Chen", "id": 2, "title": "CEO", "manager_id": None},
    {"name": "Shrutika Dasgupta", "id": 22, "title": "Engineer", "manager_id": 8},
    {"name": "Ryan Miller", "id": 30, "title": "Operations Lead", "manager_id": 4},
]


def employee_to_text(employee: dict) -> str:
    """Returns the formatted text necessary to show the employee
    :param employee: employee to be formatted
    :return: Formatted text
    """
    return f'{employee.get("title")}: {employee.get("name")}'


def get_reporters(employee: dict) -> list:
    """Get the reporters of an employee, sorted by the last name of the reporter
    :param employee:
    :return: Reporters of an employee
    """
    return sorted(list(filter(lambda e: e.get('manager_id') == employee.get('id'), _employees_list)),
                  key=lambda e: e['name'].split()[1])


def process_employee(employee):
    """
    Get the list necessary to render in view using the builtin unordered_list, recursively
    https://docs.djangoproject.com/en/dev/ref/templates/builtins/#unordered-list
    Process from the CEO to lower ranks
    :param employee: employee to be process
    :return:
    """
    hold_list = [employee_to_text(employee)]
    reporters = get_reporters(employee)
    if reporters:
        hold_list.append([])
    for r in reporters:
        hold_list[-1].extend(process_employee(r))
    return hold_list


def employees_view(request):
    ceo = next(filter(lambda employee: not employee.get('manager_id'), _employees_list))
    employees_mapped = process_employee(ceo)
    context = {
        'employees': employees_mapped
    }
    return render(request, 'employees.html', context)
