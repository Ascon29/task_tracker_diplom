from collections import Counter

from task_tracker.models import Task


def get_important_tasks():
    # берем все существующие задачи.
    all_tasks = Task.objects.all()
    # берем всех существующих исполнителей, чтобы посчитать количество их задач.
    all_executors = [executor.full_name for task in all_tasks for executor in task.executor.filter(is_superuser=False)]
    executors_task_count = list(dict(Counter(all_executors).most_common()).items())

    # Создаем список наименее загруженных сотрудников. Берём последнего сотрудника из списка выше,
    # сравниваем количество его задач со всеми остальными и добавляем их в список, если они равны.
    least_busy_executors = [i for i in executors_task_count if i[-1] == executors_task_count[-1][-1]]

    # берем задачи не взятые в работу, имеющие родительскую задачу, взятую в работу.
    important_tasks = Task.objects.filter(status="Создана", parent_task__status="В работе")

    tmp_executors_list = [i[0] for i in least_busy_executors]
    result = []
    for tasks in important_tasks:  # цикл по важным задачам.
        parent_executors = tasks.parent_task.executor.all()  # сотрудники выполняющие родительскую задачу.
        for parent_executor in parent_executors:
            for i in executors_task_count:
                if (
                    f"{parent_executor}" == i[0]
                ):  # находим сотрудника-родителя среди всех сотрудников, чтобы узнать количество выполняемых им задач.
                    if (
                        i[-1] <= least_busy_executors[-1][-1] + 2
                    ):  # если ему назначено максимум на 2 задачи больше, чем наименее загруженному сотруднику,
                        tmp_executors_list.append(i[0])  # добавляем его в список возможных сотрудников
                        tmp_result = {
                            "important_task": tasks.name,
                            "deadline": str(tasks.deadline),
                            "possible_executors": list(set(tmp_executors_list)),
                        }
                        if (
                            tmp_result in result
                        ):  # пропускаем, если словарь с такой задачей уже есть в конечном списке.
                            continue
                        result.append(tmp_result)
    return result
