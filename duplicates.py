import os


def get_files_in_path(path):
    files_list = list()
    for entry in os.scandir(path):
        if entry.is_file(follow_symlinks=False):
            file_statistic = (entry.name, entry.stat().st_size, entry.path)
            files_list.append(file_statistic)
        elif entry.is_dir(follow_symlinks=False):
            files_list.extend(get_files_in_path(entry.path))
    return files_list


def are_files_duplicates(file_statistic1, file_statistic2):
    return file_statistic1[0] == file_statistic2[0] and file_statistic1[1] == file_statistic2[1]


def get_duplicates_paths(files_list):
    duplicates = list()
    for file_statistic1_num, file_statistic1 in enumerate(files_list):
        current_file_duplicates = list()
        for file_statistic2 in files_list[file_statistic1_num:]:
            if are_files_duplicates(file_statistic1, file_statistic2):
                current_file_duplicates.append(file_statistic2)
        if len(current_file_duplicates) > 1:
            duplicates.append(current_file_duplicates)
    return duplicates


def get_duplicates(path):
    files_list = get_files_in_path(path)
    return get_duplicates_paths(files_list)


def print_duplicates(path):
    try:
        duplicates = get_duplicates(path)
        if duplicates:
            for block_of_duplicates in duplicates:
                print('Name:', block_of_duplicates[0][1], 'Size:', block_of_duplicates[0][2], 'byte')
                print('Duplicates:')
                for duplicate in block_of_duplicates:
                    print(duplicate[0])
    except PermissionError:
        print('Permission error!')
    except FileNotFoundError:
        print('Path not found!')
    input('Press enter')

if __name__ == '__main__':
    user_path = input('Directory path: ')
    print_duplicates(user_path)