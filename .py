import logging

from todoist_api_python.api import TodoistAPI
# from yaml import load, Loader

from test3 import get_tasks_from_the_table, get_current_data_rows

# config_file_path = "config.yaml"
# with open(config_file_path, "r", encoding="utf-8") as f:
#     config = load(f, Loader)

api = TodoistAPI('58a4f15efbfee49f7d3ac6aafe920749130fd6d1')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)


def main():
    projects = get_projects_todoist()
    del projects['Луч']
    del projects['Висишки']
    del projects['Другое']
    del projects['Inbox']
    del projects['Личное']

    logging.info(f"Кол-во проектов: {len(projects)}")
    for key, value in projects.items():
        try:
            tasks = get_tasks(value)
            logging.info(f"В проекте {key} {len(tasks)} задач")
            sections = get_sections(value)
            collaborators = get_collaborators(value)
            logging.info(f"Получаю все листы по заголовку таблицы {key}")
            data_table = get_tasks_from_the_table(key)
            logging.info(f"Кол-во полученных листов: {key}")

            if not data_table:
                continue
            elif isinstance(data_table[0], list):
                add_tasks(data_table, key, tasks, value, sections, collaborators)
            else:
                for i in data_table:
                    current_data = get_current_data_rows(i)
                    if not current_data:
                        continue
                    else:
                        add_tasks(current_data, str(i.title), tasks, value, sections, collaborators)
        except Exception as e:
            logging.exception(e)
            continue


def get_projects_todoist() -> dict:
    projects = api.get_projects()
    id_projects = {project.name: project.id for project in projects}
    return id_projects


def get_tasks(project_id):
    try:
        tasks = api.get_tasks(project_id=project_id)
        list_tasks = [task.content for task in tasks]
        return list_tasks
    except Exception as error:
        return error


def get_sections(project_id):
    try:
        sections = api.get_sections(project_id=project_id)
        id_sections = {section.name: section.id for section in sections}
        return id_sections
    except Exception as error:
        return error


def get_collaborators(project_id):
    try:
        collaborators = api.get_collaborators(project_id)
        collaborators_ids = {collaborator.name: collaborator.id for collaborator in collaborators}
        return collaborators_ids
    except Exception as error:
        return error


def add_tasks(data_table, project, list_tasks, project_id, section_id, collaborator_id):
    logging.info("Текущие задачи:\n" + "\n".join(list_tasks))
    for el in data_table:
        try:
            title_task = f'{project} // {el[0]} // Статья {el[1]}'

            if title_task not in list_tasks:
                logging.info(f"Задача {title_task} не в списке")
            else:
                logging.info(f"Задача {title_task} уже есть в списке")


            if title_task not in list_tasks:
                logging.info("Была обнаружена новая задача. Добавляю...")
                if el[-1].startswith('https://docs.google.com'):
                    description = f'[Ссылка на ТЗ]({el[-1]})'
                else:
                    description = None

                task = api.add_task(content=title_task, description=description, project_id=project_id,
                                    section_id=section_id[el[7]],
                                    labels=[el[5]], assignee_id=collaborator_id[el[7]],
                                    due_string=f'{el[8]} 14:00')
                logging.info("Задача успешно добавлена")
        except:
            continue


if __name__ == '__main__':
    main()