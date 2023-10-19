from src.API import HeadHunterAPI, SuperJobAPI
from src.vacancy import Vacancy
from src.filsaver import JSONSaver
import os

QUIT_WORDS = ('exit', 'end', 'quit', 'q')
BACK_WORDS = ('back', 'previous', 'b')


def greetings_menu():
    print(
        f'Hi! You can search vacancies by keyword on Head Hunter or SuperJob, '
        f'or you can work with previously found vacancies'
        f'To select action please type its number in console\n'
        f'To stop program you can type {QUIT_WORDS} in ANY menu\n'
        f'You can get to previous page if you type {BACK_WORDS} in menus with "back" option'
    )


def main_menu():
    while True:
        print(
            f'1: Search on HeadHunter\n'
            f'2: Search on SuperJob\n'
            f'3: Search on both\n'
            f'4: Work with previously found vacancies\n'
            f'q: Exit program\n'
            f'Please select what you want to do'
        )
        user_input = check_for_quit(input('Your choice: '))
        if user_input not in ('1', '2', '3', '4'):
            print('Please select viable option')
            continue
        else:
            return user_input


def check_for_quit(user_input):
    if user_input.lower() in QUIT_WORDS:
        quit('Thanks for using')
    else:
        return user_input


def search_screen(previous_choice):
    if previous_choice == '1':
        print('To start search for vacancies on HeadHunter, please enter search keyword')
        user_input = check_for_quit(input('Search keyword:'))
        print(f'Parsing HeadHunter for vacancies with keyword')
        search_results = HeadHunterAPI(user_input).get_vacancies()
        if search_results is None:
            return None
        return [Vacancy.init_from_json(vacancy) for vacancy in search_results]
    if previous_choice == '2':
        print('To start search for vacancies on SuperJob, please enter search keyword')
        user_input = check_for_quit(input('Search keyword:'))
        search_results = SuperJobAPI(user_input).get_vacancies()
        if search_results is None:
            return None
        return [Vacancy.init_from_json(vacancy) for vacancy in search_results]
    if previous_choice == '3':
        print('To start search for vacancies on HeadHunter and SuperJob, please enter search keyword')
        user_input = check_for_quit(input('Search keyword:'))
        search_results_hh = HeadHunterAPI(user_input).get_vacancies()
        search_results_sj = SuperJobAPI(user_input).get_vacancies()
        if search_results_hh is None and search_results_sj is None:
            return None
        elif search_results_hh is None:
            print('Something went wrong with Head Hunter, but we got vacancies from SuperJob')
            return [Vacancy.init_from_json(vacancy) for vacancy in search_results_sj]
        elif search_results_sj is None:
            print('Something went wrong with SuperJob, but we got vacancies from HeadHunter')
            return [Vacancy.init_from_json(vacancy) for vacancy in search_results_hh]
        else:
            return [Vacancy.init_from_json(vacancy) for vacancy in search_results_sj] + \
                [Vacancy.init_from_json(vacancy) for vacancy in search_results_hh]


def search_result_menu(search_results: list):
    print(f'We have {len(search_results)} vacancies, what you want to do next?')
    while True:
        print(f'1: Save in file. You can select file to save vacancies with this option. After you can View results\n'
              f'2: View results. File vacancies.json will be overwritten\n'
              f'b: Main menu\n'
              f'q: Exit program\n'
              f'Please select what you want to do\n'
              )
        user_input = check_for_quit(input('Your choice: '))
        if user_input.lower() in BACK_WORDS:
            return 'back'
        elif user_input not in ('1', '2'):
            print('Please select viable option\n')
            continue
        else:
            return user_input


def custom_save_file():
    while True:
        print(
            f'To save vacancies, please input file name that consists only from letters without file type\n'
            f'b: Previous menu\n'
            f'q: Exit program\n'
              )
        file_name = check_for_quit(input('File name: '))
        if file_name.lower() in BACK_WORDS:
            return 'back'
        elif not file_name.isalpha():
            print('File name must consist only from letters\n')
            continue
        elif os.path.exists(os.path.join('../', 'Vacancies', (file_name + '.json'))):
            print(
                f'File {file_name}.json already exists. Do you want to overwrite this file?\n'
                f'y: Yes\n'
                f'n: No \n'
                f'q: Exit\n'
                f'Please select what you want to do\n'
              )
            user_input = check_for_quit(input('Your choice: '))
            if user_input.lower() in ('y', 'yes'):
                return file_name
            elif user_input.lower() in ('n', 'no'):
                continue
            else:
                print('Please select viable option\n')
                continue
        else:
            return file_name


def save_file(search_results: list, file_name=None) -> JSONSaver:
    if file_name is None:
        default_saver = JSONSaver()
        default_saver.save_vacancy_list(search_results)
        return default_saver
    else:
        custom_saver = JSONSaver(file_name)
        custom_saver.save_vacancy_list(search_results)
        return custom_saver


def view_results_menu():
    print('Do you need results filtering?')
    while True:
        print(
            f'1: No filtering\n'
            f'2: To filtering menu\n'
            f'b: Previous menu\n'
            f'q: Exit program\n'
            f'Please select what you want to do\n'
        )
        user_input = check_for_quit(input('Your choice: '))
        if user_input.lower() in BACK_WORDS:
            return 'back'
        elif user_input not in ('1', '2'):
            print('Please select viable option\n')
            continue
        else:
            return user_input


def delete_vacancy(saver: JSONSaver, vac_list: list):
    while True:
        print(
            f'Please type in number of vacancy you want to delete\n'
            f'b: Previous menu\n'
            f'q: Exit program\n'
        )
        user_input = check_for_quit(input('Vacancy number: '))
        if user_input in BACK_WORDS:
            return 'back'
        elif not user_input.isdigit():
            print('Please type in a number\n')
            continue
        elif int(user_input) not in range(1, (len(vac_list)+1)):
            print('Please type in viable number\n')
            continue
        else:
            deleted_vacancy = vac_list.pop((int(user_input)-1))
            is_deleted = saver.delete_vacancy(deleted_vacancy)
            if is_deleted is None:
                print('Something went wrong, please try again\n')
                continue
            return vac_list


def add_vacancy(vac_list: list):
    while True:
        print(
            f'Please type in number of vacancy you want to add\n'
            f'b: Previous menu\n'
            f'q: Exit program\n'
        )
        user_input = check_for_quit(input('Vacancy number: '))
        if user_input in BACK_WORDS:
            return 'back'
        elif not user_input.isdigit():
            print('Please type in a number\n')
            continue
        elif int(user_input) not in range(1, (len(vac_list)+1)):
            print('Please type in viable number\n')
            continue
        else:
            vacancy_to_add = vac_list[int(user_input)-1]
            while True:
                print(
                    f'To save vacancy, please input file name that consists only from letters without file type\n'
                    f'b: Previous menu\n'
                    f'q: Exit program\n'
                )
                file_name = check_for_quit(input('File name: '))
                if file_name.lower() in BACK_WORDS:
                    break
                elif not file_name.isalpha():
                    print('File name must consist from only letters\n')
                    continue
                else:
                    saver = JSONSaver(file_name)
                    saver.add_vacancy(vacancy_to_add)
                    print(f'Vacancy {vacancy_to_add.name} is added to {saver.file_path}\n')
                    return True


def print_vacancies(vac_list: list):
    vac_list_len = len(vac_list)
    if vac_list_len % 5 == 0:
        total_page_number = vac_list_len//5
        on_last_page = 5
    else:
        total_page_number = vac_list_len//5 + 1
        on_last_page = vac_list_len % 5
    n1 = 0
    n2 = 5
    page_number_counter = 1
    while True:
        print(f'Vacancies from {n1+1} to {n2}. Page {page_number_counter}/{total_page_number}')
        for index in range(n1, n2):
            print(index+1)
            print(vac_list[index])
        while True:
            print(
                f'1: Previous page\n'
                f'2: Next page\n'
                f'3: Go to page by number\n'
                f'4: Add vacancy to separate file\n'
                f'5: Delete vacancy from current file\n'
                f'b: Previous menu\n'
                f'q: Exit program\n'
                f'Please select what you want to do'
            )
            user_input = check_for_quit(input('Your choice: '))
            if user_input.lower() in BACK_WORDS:
                return 'back'
            elif user_input in ('4', '5'):
                return user_input
            elif user_input == '1':
                if page_number_counter == 1:
                    print('This page is first\n')
                    continue
                else:
                    page_number_counter -= 1
                    n2 = page_number_counter * 5
                    n1 = n2 - 5
                    break
            elif user_input == '2':
                if page_number_counter == total_page_number:
                    print('This page is last\n')
                    continue
                else:
                    page_number_counter += 1
                    if page_number_counter == total_page_number:
                        n1 = (page_number_counter - 1) * 5
                        n2 = n1 + on_last_page
                        break
                    else:
                        n2 = page_number_counter * 5
                        n1 = n2 - 5
                        break
            elif user_input == '3':
                while True:
                    print(f'Please type number of page you want to see from 1 to {total_page_number}')
                    page_number = check_for_quit(input('Page number: '))
                    if not page_number.isdigit() or int(page_number) not in range(1, total_page_number + 1):
                        print('Please type viable page number\n')
                        continue
                    else:
                        page_number_counter = int(page_number)
                        if page_number_counter == total_page_number:
                            n1 = (page_number_counter - 1) * 5
                            n2 = n1 + on_last_page
                            break
                        else:
                            n2 = page_number_counter * 5
                            n1 = n2 - 5
                            break
                break


def previously_found_menu():
    while True:
        print(
            f'Type file name you want to work with without its type(.json)\n. '
            f'b: Previous menu\n'
            f'q: Exit program\n'
              )
        file_name = check_for_quit(input('File name: '))
        if file_name.lower() in BACK_WORDS:
            return 'back'
        elif not file_name.isalpha():
            print('Please enter valid name')
            continue
        elif not os.path.exists(os.path.join('../', 'Vacancies', (file_name + '.json'))):
            print('There is no such file in Vacancies folder, please try again')
            continue
        else:
            return file_name


def filtering_menu():
    while True:
        print(
            f'1: Vacancies by salary from lowest to highest\n'
            f'2: Vacancies by salary from highest to lowest\n'
            f'3: Full time vacancies\n'
            f'4: Part-time vacancies\n'
            f'5: Remote vacancies\n'
            f'b: Previous menu\n'
            f'q: Exit program\n'
            f'Please select what you want to do'
        )
        user_input = check_for_quit(input('Your choice: '))
        if user_input.lower() in BACK_WORDS:
            return 'back'
        elif user_input not in ('1', '2', '3', '4', '5'):
            print('Please select viable option')
            continue
        else:
            return user_input


def user_interaction():
    greetings_menu()
    while True:
        main_menu_user_input = main_menu()
        if main_menu_user_input in ('1', '2', '3'):
            while True:
                search_results = search_screen(main_menu_user_input)
                if search_results is None:
                    print(f'Something went wrong, please try again')
                    continue
                else:
                    while True:
                        search_result_screen_user_input = search_result_menu(search_results)
                        json_saver = JSONSaver()
                        if search_result_screen_user_input == 'back':
                            break
                        elif search_result_screen_user_input == '1':
                            file_name = custom_save_file()
                            if file_name == 'back':
                                continue
                            else:
                                json_saver = JSONSaver(file_name)
                        vac_list = None
                        while True:
                            filtering_choice = view_results_menu()
                            if filtering_choice == 'back':
                                break
                            elif filtering_choice == '1':
                                vac_list = json_saver.get_vacancies()
                                if vac_list is None:
                                    print('Something went wrong, please try again')
                                    continue
                            elif filtering_choice == '2':
                                filtering = filtering_menu()
                                if filtering == 'back':
                                    continue
                                elif filtering == '1':
                                    vac_list = json_saver.get_vacancies_by_salary(True)
                                elif filtering == '2':
                                    vac_list = json_saver.get_vacancies_by_salary(False)
                                elif filtering == '3':
                                    vac_list = json_saver.get_vacancies_by_employment(True)
                                elif filtering == '4':
                                    vac_list = json_saver.get_vacancies_by_employment(False)
                                elif filtering == '5':
                                    vac_list = json_saver.get_remote_vacancies()
                            while True:
                                if vac_list is None or len(vac_list) == 0 or not type(vac_list) == list:
                                    print('Something went wrong, please try again')
                                    break
                                printing_user_input = print_vacancies(vac_list)
                                if printing_user_input == 'back':
                                    break
                                elif printing_user_input == '4':
                                    add_vacancy(vac_list)
                                    continue
                                elif printing_user_input == '5':
                                    vac_list = delete_vacancy(json_saver, vac_list)
                                    continue

        else:
            while True:
                file_name = previously_found_menu()
                if file_name == 'back':
                    break
                else:
                    json_saver = JSONSaver(file_name)
                    vac_list = None
                    while True:
                        filtering_choice = view_results_menu()
                        if filtering_choice == 'back':
                            break
                        elif filtering_choice == '1':
                            vac_list = json_saver.get_vacancies()
                            if vac_list is None:
                                print('Something went wrong, please try again')
                                continue
                        elif filtering_choice == '2':
                            filtering = filtering_menu()
                            if filtering == 'back':
                                continue
                            elif filtering == '1':
                                vac_list = json_saver.get_vacancies_by_salary(True)
                            elif filtering == '2':
                                vac_list = json_saver.get_vacancies_by_salary(False)
                            elif filtering == '3':
                                vac_list = json_saver.get_vacancies_by_employment(True)
                            elif filtering == '4':
                                vac_list = json_saver.get_vacancies_by_employment(False)
                            elif filtering == '5':
                                vac_list = json_saver.get_remote_vacancies()
                        while True:
                            if vac_list is None or len(vac_list) == 0 or not type(vac_list) == list:
                                print('Something went wrong, please try again')
                                break
                            printing_user_input = print_vacancies(vac_list)
                            if printing_user_input == 'back':
                                break
                            elif printing_user_input == '4':
                                add_vacancy(vac_list)
                                continue
                            elif printing_user_input == '5':
                                vac_list = delete_vacancy(json_saver, vac_list)
                                continue
