from src.api import HeadHunterAPI, SuperJobAPI
from src.vacancy import Vacancy
from src.filsaver import JSONSaver
import constants
import os


def greetings_menu():
    print(
        f'Hi! You can search vacancies by keyword on Head Hunter or SuperJob, '
        f'or you can work with previously found vacancies'
        f'To select action please type its number in console\n'
        f'To stop program you can type {constants.QUIT_WORDS} in ANY menu\n'
        f'You can get to previous page if you type {constants.BACK_WORDS} in menus with constants.BACK option'
    )


def main_menu():
    while True:
        print(
            f'{constants.SEARCH_ON_HH_RESPONSE}: Search on HeadHunter\n'
            f'{constants.SEARCH_ON_SJ_RESPONSE}: Search on SuperJob\n'
            f'{constants.SEARCH_BOTH_RESPONSE}: Search on both\n'
            f'{constants.WORK_WITH_PREV_RESPONSE}: Work with previously found vacancies\n'
            f'{constants.EXIT_MENU_OPTION}\n'
            f'{constants.SELECT_MESSAGE}'
        )
        user_input = check_for_quit(input(f'{constants.YOUR_CHOICE_MESSAGE}'))
        if user_input not in (
                constants.SEARCH_ON_HH_RESPONSE, constants.SEARCH_ON_SJ_RESPONSE,
                constants.SEARCH_BOTH_RESPONSE, constants.WORK_WITH_PREV_RESPONSE
        ):
            print(f'{constants.VIABLE_OPTION_MESSAGE}')
            continue
        else:
            return user_input


def check_for_quit(user_input):
    if user_input.lower() in constants.QUIT_WORDS:
        quit('Thanks for using')
    else:
        return user_input


def search_screen(previous_choice):
    if previous_choice == constants.SEARCH_ON_HH_RESPONSE:
        print('To start search for vacancies on HeadHunter, please enter search keyword')
        user_input = check_for_quit(input('Search keyword:'))
        if user_input in constants.BACK_WORDS:
            return constants.BACK
        print(f'Parsing HeadHunter for vacancies with keyword {user_input}')
        search_results = HeadHunterAPI(user_input).get_vacancies()
        if search_results is None:
            return None
        return [Vacancy.init_from_json(vacancy) for vacancy in search_results]
    if previous_choice == constants.SEARCH_ON_SJ_RESPONSE:
        print('To start search for vacancies on SuperJob, please enter search keyword')
        user_input = check_for_quit(input('Search keyword:'))
        if user_input in constants.BACK_WORDS:
            return constants.BACK
        print(f'Parsing SuperJob for vacancies with keyword {user_input}')
        search_results = SuperJobAPI(user_input).get_vacancies()
        if search_results is None:
            return None
        return [Vacancy.init_from_json(vacancy) for vacancy in search_results]
    if previous_choice == constants.SEARCH_BOTH_RESPONSE:
        print('To start search for vacancies on HeadHunter and SuperJob, please enter search keyword')
        user_input = check_for_quit(input('Search keyword:'))
        if user_input in constants.BACK_WORDS:
            return constants.BACK
        print(f'Parsing HeadHunter and SuperJob for vacancies with keyword {user_input}')
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
        print(f'{constants.SAVE_IN_FILE_RESPONSE}: Save in file. '
              f'You can select file to save vacancies with this option. After you can View results\n'
              f'{constants.VIEW_RESULTS_RESPONSE}: View results. File vacancies.json will be overwritten\n'
              f'{constants.BACK_RESPONSE}: Main menu\n'
              f'{constants.EXIT_MENU_OPTION}\n'
              f'{constants.SELECT_MESSAGE}\n'
              )
        user_input = check_for_quit(input(f'{constants.YOUR_CHOICE_MESSAGE}'))
        if user_input.lower() in constants.BACK_WORDS:
            return constants.BACK
        elif user_input not in (constants.SAVE_IN_FILE_RESPONSE, constants.VIEW_RESULTS_RESPONSE):
            print(f'{constants.VIABLE_OPTION_MESSAGE}\n')
            continue
        else:
            return user_input


def custom_save_file():
    while True:
        print(
            f'To save vacancies, please input file name that consists only from letters without file type\n'
            f'{constants.PREVIOUS_MENU_MENU_OPTION}\n'
            f'{constants.EXIT_MENU_OPTION}\n'
        )
        file_name = check_for_quit(input('File name: '))
        if file_name.lower() in constants.BACK_WORDS:
            return constants.BACK
        elif not file_name.isalpha():
            print(f'{constants.ONLY_LETTERS_MESSAGE}\n')
            continue
        elif os.path.exists(os.path.join('Vacancies', (file_name + '.json'))):
            print(
                f'File {file_name}.json already exists. Do you want to overwrite this file?\n'
                f'{constants.YES_RESPONSE}: Yes\n'
                f'{constants.NO_RESPONSE}: No \n'
                f'{constants.EXIT_MENU_OPTION}\n'
                f'{constants.SELECT_MESSAGE}\n'
            )
            user_input = check_for_quit(input(f'{constants.YOUR_CHOICE_MESSAGE}'))
            if user_input.lower() in constants.YES_WORDS:
                return file_name
            elif user_input.lower() in constants.NO_WORDS:
                continue
            else:
                print(f'{constants.VIABLE_OPTION_MESSAGE}\n')
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
            f'{constants.RESULTS_NO_FILTERING_RESPONSE}: No filtering\n'
            f'{constants.RESULTS_FILTERING_RESPONSE}: To filtering menu\n'
            f'{constants.PREVIOUS_MENU_MENU_OPTION}\n'
            f'{constants.EXIT_MENU_OPTION}\n'
            f'{constants.SELECT_MESSAGE}\n'
        )
        user_input = check_for_quit(input(f'{constants.YOUR_CHOICE_MESSAGE}'))
        if user_input.lower() in constants.BACK_WORDS:
            return constants.BACK
        elif user_input not in (constants.RESULTS_NO_FILTERING_RESPONSE, constants.RESULTS_FILTERING_RESPONSE):
            print(f'{constants.VIABLE_OPTION_MESSAGE}\n')
            continue
        else:
            return user_input


def delete_vacancy(saver: JSONSaver, vac_list: list):
    while True:
        print(
            f'Please type in number of vacancy you want to delete\n'
            f'{constants.PREVIOUS_MENU_MENU_OPTION}\n'
            f'{constants.EXIT_MENU_OPTION}\n'
        )
        user_input = check_for_quit(input('Vacancy number: '))
        if user_input in constants.BACK_WORDS:
            return vac_list
        elif not user_input.isdigit():
            print(f'{constants.ONLY_NUMBERS_MESSAGE}\n')
            continue
        elif int(user_input) not in range(1, (len(vac_list) + 1)):
            print(f'{constants.VIABLE_NUMBER_MESSAGE}\n')
            continue
        else:
            deleted_vacancy = vac_list.pop((int(user_input) - 1))
            is_deleted = saver.delete_vacancy(deleted_vacancy)
            if is_deleted is None:
                print(f'{constants.SOMETHING_WRONG_MESSAGE}')
                continue
            return vac_list


def add_vacancy(vac_list: list):
    while True:
        print(
            f'Please type in number of vacancy you want to add\n'
            f'{constants.PREVIOUS_MENU_MENU_OPTION}\n'
            f'{constants.EXIT_MENU_OPTION}\n'
        )
        user_input = check_for_quit(input('Vacancy number: '))
        if user_input in constants.BACK_WORDS:
            return constants.BACK
        elif not user_input.isdigit():
            print(f'{constants.ONLY_NUMBERS_MESSAGE}\n')
            continue
        elif int(user_input) not in range(1, (len(vac_list) + 1)):
            print(f'{constants.VIABLE_NUMBER_MESSAGE}\n')
            continue
        else:
            vacancy_to_add = vac_list[int(user_input) - 1]
            while True:
                print(
                    f'To save vacancy, please input file name that consists only from letters without file type\n'
                    f'{constants.PREVIOUS_MENU_MENU_OPTION}\n'
                    f'{constants.EXIT_MENU_OPTION}\n'
                )
                file_name = check_for_quit(input('File name: '))
                if file_name.lower() in constants.BACK_WORDS:
                    break
                elif not file_name.isalpha():
                    print(f'{constants.ONLY_LETTERS_MESSAGE}\n')
                    continue
                else:
                    saver = JSONSaver(file_name)
                    saver.add_vacancy(vacancy_to_add)
                    print(f'Vacancy {vacancy_to_add.name} is added to {saver.file_path}\n')
                    return True


def print_vacancies(vac_list: list):
    vac_list_len = len(vac_list)
    if vac_list_len % 5 == 0:
        total_page_number = vac_list_len // 5
        on_last_page = 5
    else:
        total_page_number = vac_list_len // 5 + 1
        on_last_page = vac_list_len % 5
    first_vacancy_on_page = 0
    if vac_list_len < 5:
        last_vacancy_on_page = vac_list_len
    else:
        last_vacancy_on_page = 5
    page_number_counter = 1
    while True:
        print(
            f'Vacancies from {first_vacancy_on_page + 1} to {last_vacancy_on_page}. '
            f'Page {page_number_counter}/{total_page_number}'
        )
        for index in range(first_vacancy_on_page, last_vacancy_on_page):
            print(index + 1)
            print(vac_list[index])
        while True:
            print(
                f'{constants.PRINT_PREVIOUS_PAGE_RESPONSE}: Previous page\n'
                f'{constants.PRINT_NEXT_PAGE_RESPONSE}: Next page\n'
                f'{constants.PRINT_GO_TO_PAGE_RESPONSE}: Go to page by number\n'
                f'{constants.PRINT_ADD_VAC_RESPONSE}: Add vacancy to separate file\n'
                f'{constants.PRINT_DEL_VAC_RESPONSE}: Delete vacancy from current file\n'
                f'{constants.PREVIOUS_MENU_MENU_OPTION}\n'
                f'{constants.EXIT_MENU_OPTION}\n'
                f'{constants.SELECT_MESSAGE}'
            )
            user_input = check_for_quit(input(f'{constants.YOUR_CHOICE_MESSAGE}'))
            if user_input.lower() in constants.BACK_WORDS:
                return constants.BACK
            elif user_input in (constants.PRINT_ADD_VAC_RESPONSE, constants.PRINT_DEL_VAC_RESPONSE):
                return user_input
            elif user_input == constants.PRINT_PREVIOUS_PAGE_RESPONSE:
                if page_number_counter == 1:
                    print('This page is first\n')
                    continue
                else:
                    page_number_counter -= 1
                    last_vacancy_on_page = page_number_counter * 5
                    first_vacancy_on_page = last_vacancy_on_page - 5
                    break
            elif user_input == constants.PRINT_NEXT_PAGE_RESPONSE:
                if page_number_counter == total_page_number:
                    print('This page is last\n')
                    continue
                else:
                    page_number_counter += 1
                    if page_number_counter == total_page_number:
                        first_vacancy_on_page = (page_number_counter - 1) * 5
                        last_vacancy_on_page = first_vacancy_on_page + on_last_page
                        break
                    else:
                        last_vacancy_on_page = page_number_counter * 5
                        first_vacancy_on_page = last_vacancy_on_page - 5
                        break
            elif user_input == constants.PRINT_GO_TO_PAGE_RESPONSE:
                while True:
                    print(f'Please type number of page you want to see from 1 to {total_page_number}')
                    page_number = check_for_quit(input('Page number: '))
                    if not page_number.isdigit() or int(page_number) not in range(1, total_page_number + 1):
                        print('Please type viable page number\n')
                        continue
                    else:
                        page_number_counter = int(page_number)
                        if page_number_counter == total_page_number:
                            first_vacancy_on_page = (page_number_counter - 1) * 5
                            last_vacancy_on_page = first_vacancy_on_page + on_last_page
                            break
                        else:
                            last_vacancy_on_page = page_number_counter * 5
                            first_vacancy_on_page = last_vacancy_on_page - 5
                            break
                break


def previously_found_menu():
    while True:
        print(
            f'Type file name you want to work with without its type(.json)\n. '
            f'{constants.PREVIOUS_MENU_MENU_OPTION}\n'
            f'{constants.EXIT_MENU_OPTION}\n'
        )
        file_name = check_for_quit(input('File name: '))
        if file_name.lower() in constants.BACK_WORDS:
            return constants.BACK
        elif not file_name.isalpha():
            print(f'{constants.ONLY_LETTERS_MESSAGE}')
            continue
        elif not os.path.exists(os.path.join('Vacancies', (file_name + '.json'))):
            print('There is no such file in Vacancies folder, please try again')
            continue
        else:
            return file_name


def filtering_menu():
    while True:
        print(
            f'{constants.FILTERING_FROM_LOWEST_RESPONSE}: Vacancies by salary from lowest to highest\n'
            f'{constants.FILTERING_FROM_HIGHEST_RESPONSE}: Vacancies by salary from highest to lowest\n'
            f'{constants.FILTERING_FULL_TIME_RESPONSE}: Full time vacancies\n'
            f'{constants.FILTERING_PART_TIME_RESPONSE}: Part-time vacancies\n'
            f'{constants.FILTERING_REMOTE_RESPONSE}: Remote vacancies\n'
            f'{constants.PREVIOUS_MENU_MENU_OPTION}\n'
            f'{constants.EXIT_MENU_OPTION}\n'
            f'{constants.SELECT_MESSAGE}'
        )
        user_input = check_for_quit(input(f'{constants.YOUR_CHOICE_MESSAGE}'))
        if user_input.lower() in constants.BACK_WORDS:
            return constants.BACK
        elif user_input not in (
                constants.FILTERING_FROM_LOWEST_RESPONSE, constants.FILTERING_FROM_HIGHEST_RESPONSE,
                constants.FILTERING_FULL_TIME_RESPONSE, constants.FILTERING_PART_TIME_RESPONSE,
                constants.FILTERING_REMOTE_RESPONSE
        ):
            print(f'{constants.VIABLE_OPTION_MESSAGE}')
            continue
        else:
            return user_input


def output_menu(json_saver: JSONSaver):
    vac_list = None
    while True:
        filtering_choice = view_results_menu()
        if filtering_choice == constants.BACK:
            break
        elif filtering_choice == constants.RESULTS_NO_FILTERING_RESPONSE:
            vac_list = json_saver.get_vacancies()
            if vac_list is None:
                print(f'{constants.SOMETHING_WRONG_MESSAGE}')
                continue
        elif filtering_choice == constants.RESULTS_FILTERING_RESPONSE:
            filtering = filtering_menu()
            if filtering == constants.BACK:
                continue
            elif filtering == constants.FILTERING_FROM_LOWEST_RESPONSE:
                vac_list = json_saver.get_vacancies_by_salary(False)
            elif filtering == constants.FILTERING_FROM_HIGHEST_RESPONSE:
                vac_list = json_saver.get_vacancies_by_salary(True)
            elif filtering == constants.FILTERING_FULL_TIME_RESPONSE:
                vac_list = json_saver.get_vacancies_by_employment(True)
            elif filtering == constants.FILTERING_PART_TIME_RESPONSE:
                vac_list = json_saver.get_vacancies_by_employment(False)
            elif filtering == constants.FILTERING_REMOTE_RESPONSE:
                vac_list = json_saver.get_remote_vacancies()
        while True:
            if vac_list is None or len(vac_list) == 0 or not type(vac_list) == list:
                print(f'{constants.SOMETHING_WRONG_MESSAGE}')
                break
            printing_user_input = print_vacancies(vac_list)
            if printing_user_input == constants.BACK:
                break
            elif printing_user_input == constants.PRINT_ADD_VAC_RESPONSE:
                add_vacancy(vac_list)
                continue
            elif printing_user_input == constants.PRINT_DEL_VAC_RESPONSE:
                vac_list = delete_vacancy(json_saver, vac_list)
                continue


def user_interaction():
    greetings_menu()
    while True:
        main_menu_user_input = main_menu()
        if main_menu_user_input in (
                constants.SEARCH_ON_HH_RESPONSE,
                constants.SEARCH_ON_SJ_RESPONSE,
                constants.SEARCH_BOTH_RESPONSE
        ):
            while True:
                search_results = search_screen(main_menu_user_input)
                if search_results is None:
                    print(f'{constants.SOMETHING_WRONG_MESSAGE}')
                    continue
                elif search_results == constants.BACK:
                    break
                while True:
                    search_result_screen_user_input = search_result_menu(search_results)
                    file_name = None
                    if search_result_screen_user_input == constants.BACK:
                        break
                    elif search_result_screen_user_input == constants.SAVE_IN_FILE_RESPONSE:
                        file_name = custom_save_file()
                        if file_name == constants.BACK:
                            continue
                    json_saver = save_file(search_results, file_name)
                    output_menu(json_saver)

        else:
            while True:
                file_name = previously_found_menu()
                if file_name == constants.BACK:
                    break
                else:
                    json_saver = JSONSaver(file_name)
                    output_menu(json_saver)
