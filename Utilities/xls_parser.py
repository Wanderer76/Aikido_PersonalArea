from ctypes import ArgumentError
from typing import BinaryIO

import openpyxl
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction

import PersonalArea.serializations
from PersonalArea import models
from Utilities import password_generantor
from Utilities import services


@transaction.atomic
def parseXlsToDb(event_slug: str, xlsx_file: InMemoryUploadedFile) -> str:
    book = openpyxl.load_workbook(xlsx_file)
    book.iso_dates = True
    sheet = book.active
    event = services.find_event_by_slug(event_slug)

    if event is None:
        return 'Мероприятие не существует'

    services.delete_achievement_if_exists(event.event_name)

    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
        member_id = services.parse_id_from_xls(row[4].value)
        if models.Achievements.objects.filter(event_name=event.event_name, member__id=member_id).exists():
            raise ArgumentError(f"Ячейка заполнена не правильно {row[4]}")

        achievement = models.Achievements()
        achievement.event_name = event.event_name
        achievement.attestation_date = row[12].value
        achievement.received_ku = services.get_ku(row[13].value)
        achievement.is_child = True if row[14].value == '+' else False

        trainer_id = services.parse_id_from_xls(row[9].value)
        services.set_trainer_status(trainer_id)
        if not (models.Aikido_Member.objects.filter(id=member_id).exists()):
            data = {
                'id': int(member_id),
                'password': password_generantor.generate_password(),
                'name': row[1].value,
                'surname': row[0].value,
                'second_name': row[2].value,
                'birthdate': services.parse_eu_date_to_us(str(row[5].value)),
                'region': int(row[6].value),
                'club': row[7].value,
                'photo': None,
                'isTrainer': False,
                'trainer_id': trainer_id
            }
            serializer = PersonalArea.serializations.RegistrationSerializer(data=data)
            if serializer.is_valid():
                aikiboy = serializer.save()
                achievement.member = aikiboy
                achievement.save()
            else:
                raise ArgumentError(f"Ошибка в строке {row}")
        else:
            aikiboy = models.Aikido_Member.objects.get(id=member_id)
            achievement.member = aikiboy
            achievement.save()

    return 'Ведомость загружена'


@transaction.atomic
def createXlsxFromRequests(event_slug: str) -> BinaryIO:
    wb = openpyxl.Workbook(iso_dates=True)
    work_sheet = wb.active
    work_sheet.append(['Фамилия', 'Имя', 'Отчество', 'степень кю/дан', '#ID', 'Дата рождения',
                       'Регион', 'Клуб', 'Тренер', 'id тренера', 'семинар', 'место проведения', 'аттестация',
                       'Присвоенная степень', 'детский', 'Экзаменатор'])

    services.set_blue_row(work_sheet)
    event = models.Events.objects.get(slug=event_slug)

    requests = models.Request.objects.filter(event_name=event.event_name)
    if not requests.exists():
        raise ArgumentError('Заявок на мероприятие нет')

    for request in requests.values():
        if request['member_id'] is not None:
            member = models.Aikido_Member.objects.get(id=request['member_id'])
            work_sheet.append(services.create_row(request, event, member))
        else:
            work_sheet.append(services.create_row(request, event))

    services.set_date_format(work_sheet)
    return services.get_xlsx_file_obj(wb, event_slug)
