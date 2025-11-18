import json
import os
import sys
import xml.etree.ElementTree as ET

import keyboard
from colorama import Fore, Style, init, AnsiToWin32

# Настройки
class AppSettings:
    # Каталог верхнего уровня *.vpr
    folder_process: str = ''

    # Путь к Gal
    folder_galaktika: str = ''

    # Лицензионный файл Support
    path_lic_support: str = ''

    # Ключ
    folder_hwkey: str = ''

    # Путь к компилятору Vip
    folder_viper: str = ''

    # Соединение с сервером SQL
    sql_server: str = ''

    # База сборки SQL
    sql_database: str = ''

    def __init__(self):
        self.folder_process = 'C:\\ClientProjects'
        self.folder_galaktika = 'C:\\Galaktika'
        self.path_lic_support = 'C:\\Galaktika\\Support\\sup_sql.lic'
        self.folder_hwkey = '192.168.X.x:55555'
        self.folder_viper = 'c:\\Program Files (x86)\\Galaktika Corp\\Viper 5.5\\bin\\5.5.41.0'
        self.sql_server = 'ncacn_ip_tcp:192.168.X.X[1997]'
        self.sql_database = 'DBName'


# Чтение или создание файла настроек
# False - создан файл, True - прочитан файл
def read_settings(settings_file_name):
    app_settings = AppSettings()
    members = [attr for attr in dir(app_settings) if
               not callable(getattr(app_settings, attr)) and not attr.startswith("__")]

    # Create settings file
    if not os.path.exists(settings_file_name):
        print(f'{Fore.BLUE}Create new {settings_file_name}...', file=stream)

        default = {}

        # Default json value
        for member in members:
            default[member] = getattr(app_settings, member)

        # Write default value to json file
        with open(settings_file_name, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=2)

        # Return default value
        return False, app_settings

    with open(settings_file_name, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    for member in members:
        setattr(app_settings, member, cfg.get(member, getattr(app_settings, member)))

    return True, app_settings


# Скрипт преобразовывает старые проекты в нормальный вид, заменяя параметры
def indent(elem, level=0):
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def main():
    settings_file_name = os.path.join(os.getcwd(), 'config.json')
    is_exist, app_settings = read_settings(settings_file_name)

    if not is_exist:
        print(f'{Fore.RED}Созданы настройки по умолчанию: {Fore.BLUE}{settings_file_name}', file=stream)
        print(f'{Fore.GREEN}Нажмите пробел (Space) для продолжения...')
        keyboard.wait("space")
        sys.exit(0)
    elif not os.path.isdir(app_settings.folder_process):
        print(f'{Fore.RED}Каталог не найден: {Fore.BLUE}{app_settings.folder_process}', file=stream)
        print(f'{Fore.GREEN}Нажмите пробе (Space) для продолжения...')
        keyboard.wait("space")
        sys.exit(0)
    else:
        print(f'{Fore.CYAN}Настройки:', file=stream)
        print(f'    {Fore.GREEN}Каталог верхнего уровня *.vpr: {Fore.BLUE}{app_settings.folder_process}', file=stream)
        print(f'    {Fore.GREEN}Путь к Gal: {Fore.BLUE}{app_settings.folder_galaktika}', file=stream)
        print(f'    {Fore.GREEN}Путь к компилятору Vip: {Fore.BLUE}{app_settings.folder_viper}', file=stream)
        print(f'    {Fore.GREEN}База сборки SQL: {Fore.BLUE}{app_settings.sql_database}', file=stream)
        print(f'    {Fore.GREEN}Соединение с сервером SQL: {Fore.BLUE}{app_settings.sql_server}', file=stream)
        print(f'    {Fore.GREEN}Ключ: {Fore.BLUE}{app_settings.folder_hwkey}', file=stream)
        print(f'    {Fore.GREEN}Лицензионный файл Support: {Fore.BLUE}{app_settings.path_lic_support}', file=stream)

        print(f'{Fore.CYAN}Нажмите пробел для продолжения...', file=stream)
        key_name = keyboard.read_key()
        if key_name != "space":
            print(f'{Fore.CYAN}Отмена обработки...\n*Нажмите пробел (space) для выхода...')
            keyboard.wait("space")
            sys.exit(0)

        print(f'{Fore.CYAN}Начало обновления *.vpr в {Fore.BLUE}{app_settings.folder_process}', file=stream)

        for path, sub_dirs, files in os.walk(app_settings.folder_process):
            for name in files:
                if name.find('_project.vpr') != -1:
                    # проектный файл
                    _file_name = os.path.join(path, name)

                    # временный файл, в который будем писать новые данные
                    _file_name_new = os.path.join(path, '_project_tmp.vpr')

                    # Удаление tmp файла _project_tmp.vpr
                    if os.path.exists(_file_name_new.lower()):
                        os.remove(_file_name_new.lower())

                    print(f'    {Fore.GREEN}Обработка файла: {Fore.BLUE}{_file_name}', file=stream)

                    try:
                        et_doc = ET.parse(_file_name)
                        root = et_doc.getroot()

                        # Настройки сборки
                        _CoreVipXML = ET.Element('CoreVip')

                        # Структура файлов
                        _ProjectItemsXML = ET.Element('ProjectItems')

                        # Позиции курсора?
                        _MarkerListXML = ET.Element('MarkerList')

                        for _item in root:
                            # Получаем блоки внутри ProjectManager
                            for _sub_item in _item:

                                if _sub_item.tag == 'CoreVip' and _item.tag == 'ProjectManager':
                                    _CoreVipXML = _sub_item

                                if _sub_item.tag == 'ProjectItems' and _item.tag == 'ProjectManager':
                                    _ProjectItemsXML = _sub_item

                                if _sub_item.tag == 'MarkerList' and _item.tag == 'ProjectManager':
                                    _MarkerListXML = _sub_item

                        _ViperXML = ET.Element('Viper', Version='5005020000')
                        _ProjectManagerXML = ET.SubElement(_ViperXML, 'ProjectManager')

                        _ProjectNameXML = ET.SubElement(_ProjectManagerXML, 'ProjectName')
                        _ProjectNameXML.text = 'ViperProject'

                        _ActiveIndexXML = ET.SubElement(_ProjectManagerXML, 'ActiveIndex')
                        _ActiveIndexXML.text = '1'

                        _ProjectVarListXML = ET.SubElement(_ProjectManagerXML, 'ProjectVarList')
                        _ProjectVarXML = ET.SubElement(_ProjectVarListXML, 'ProjectVar', Name='$[GalPath]',
                                                       Value=app_settings.folder_galaktika)

                        # Создание нового блока 'FileList' внутри _ProjectManagerXML ('ProjectItems')
                        _FileList = ET.SubElement(_ProjectManagerXML, 'FileList')  # Открытые файлы
                        # Создание нового элемента 'File' внутри блока 'FileList'
                        ET.SubElement(_FileList, 'File', Name='prj.prj', PosX="1", PosY="1", OpenEditor="True",
                                      Active="True")

                        ## Удаление лишних элементов -------------------------------------------------------------------
                        for _node in _CoreVipXML.findall('./VipDebug'):
                            _CoreVipXML.remove(_node)
                        ## Удаление лишних элементов -------------------------------------------------------------------
                        for _node in _CoreVipXML.findall('./VipLicense'):
                            _CoreVipXML.remove(_node)

                        ##-------------------------------------------------------------------
                        for _CoreLs in _CoreVipXML:
                            ##-------------------------------------------------------------------
                            if _CoreLs.tag == 'VipParameters':
                                for _CoreLsSp in _CoreLs:
                                    if _CoreLsSp.tag == 'AtlDir':
                                        _CoreLsSp.text = app_settings.folder_viper
                            ##-------------------------------------------------------------------
                            if _CoreLs.tag == 'VipDatabase':
                                for _node in _CoreLs.findall('./'):
                                    _CoreLs.remove(_node)
                                _SP_CoreVipXML = ET.SubElement(_CoreLs, 'Name')
                                _SP_CoreVipXML.text = app_settings.sql_database
                            ##-------------------------------------------------------------------
                            if _CoreLs.tag == 'VipFiles':
                                for _CoreLsSp in _CoreLs:
                                    if _CoreLsSp.tag == 'SubServientResource':
                                        _CoreLsSp.text = r'$[ProjectPath]\tmp\Atlantis.res'
                                    if _CoreLsSp.tag == 'ConfWorkResource':
                                        _CoreLsSp.text = r'$[ProjectPath]\tmp\Viper.crf'
                                    if _CoreLsSp.tag == 'OutputDirectory':
                                        _CoreLsSp.text = r'$[ProjectPath]\tmp\\'[:-1]
                                    if _CoreLsSp.tag == 'TemporaryDirectory':
                                        _CoreLsSp.text = r'$[ProjectPath]\tmp\\'[:-1]
                                    if _CoreLsSp.tag == 'LoadIds':
                                        _CoreLsSp.text = r'True'
                                    if _CoreLsSp.tag == 'StartPathDirectory':
                                        _CoreLsSp.text = r'$[GalPath]\exe'
                                    if _CoreLsSp.tag == 'RepoSystemName':
                                        _CoreLsSp.text = r'galnet'
                                if len(_CoreLs.findall('LoadIds')) == 0:
                                    _SP_CoreVipXML = ET.SubElement(_CoreLs, 'LoadIds')
                                    _SP_CoreVipXML.text = r'True'
                                if len(_CoreLs.findall('StartPathDirectory')) == 0:
                                    _SP_CoreVipXML = ET.SubElement(_CoreLs, 'StartPathDirectory')
                                    _SP_CoreVipXML.text = r'$[GalPath]\exe'
                                if len(_CoreLs.findall('RepoSystemName')) == 0:
                                    _SP_CoreVipXML = ET.SubElement(_CoreLs, 'RepoSystemName')
                                    _SP_CoreVipXML.text = r'galnet'
                            ##-------------------------------------------------------------------

                        _ProjectManagerXML.append(_CoreVipXML)

                        _DatabaseConfigurationXML = ET.SubElement(_ProjectManagerXML, 'DatabaseConfiguration')
                        _ConfigurationListXML = ET.SubElement(_DatabaseConfigurationXML, 'ConfigurationList')
                        _VipDatabaseXML = ET.SubElement(_ConfigurationListXML, 'VipDatabase')
                        _SP_VipDatabaseXML = ET.SubElement(_VipDatabaseXML, 'Name')
                        _SP_VipDatabaseXML.text = app_settings.sql_database
                        _SP_VipDatabaseXML = ET.SubElement(_VipDatabaseXML, 'DatabaseDriver')
                        _SP_VipDatabaseXML.text = '1'
                        _SP_VipDatabaseXML = ET.SubElement(_VipDatabaseXML, 'DatabaseID')
                        _SP_VipDatabaseXML.text = app_settings.sql_database
                        _SP_VipDatabaseXML = ET.SubElement(_VipDatabaseXML, 'SqlServerParameters')
                        _SP_VipDatabaseXML.text = app_settings.sql_server
                        _SP_VipDatabaseXML = ET.SubElement(_VipDatabaseXML, 'FullLoginName')
                        _SP_VipDatabaseXML.text = 'True'
                        _SP_VipDatabaseXML = ET.SubElement(_VipDatabaseXML, 'HwKeyTransport')
                        _SP_VipDatabaseXML.text = '1'
                        _SP_VipDatabaseXML = ET.SubElement(_VipDatabaseXML, 'HwKeyDirectory')
                        _SP_VipDatabaseXML.text = app_settings.folder_hwkey
                        _SP_VipDatabaseXML = ET.SubElement(_VipDatabaseXML, 'LicFileName')
                        _SP_VipDatabaseXML.text = app_settings.path_lic_support

                        _ProjectManagerXML.append(_ProjectItemsXML)
                        _ProjectManagerXML.append(_MarkerListXML)

                        indent(_ViperXML)

                        ET.ElementTree(_ViperXML).write(_file_name_new, encoding='windows-1251', xml_declaration=True)

                        _file_name_old = os.path.join(path, r'_project_save.vpr')

                        # del _project_save.vpr
                        if os.path.exists(_file_name_old.lower()):
                            os.remove(_file_name_old.lower())

                        # buckup file (_project.vpr >> _project_save.vp)
                        os.rename(_file_name, _file_name_old)

                        os.rename(_file_name_new, _file_name)
                    except Exception as e:
                        print(f'    {Fore.RED}Error process file: {Fore.BLUE}{_file_name}\n{e}', file=stream)

        print(f'{Fore.CYAN}Процесс завершен, нажмите пробел (Space) для входа...', file=stream)
        keyboard.wait("space")


if __name__ == '__main__':
    init(wrap=False)
    stream = AnsiToWin32(sys.stderr).stream
    main()
