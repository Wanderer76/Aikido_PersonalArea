import os
from ctypes import ArgumentError

import openpyxl
from django.db import transaction
from openpyxl.styles import numbers
import PersonalArea.serializations
from PersonalArea import models
from Utilities import password_generantor
from Utilities import services

@transaction.atomic
def parseXlcToDb(xlsxFile):
    book = openpyxl.open(xlsxFile, read_only=True)
    book.iso_dates = True
    sheet = book.active
    fileName = os.path.basename(xlsxFile)
    event_name = fileName[0:fileName.find('.')]

    services.check_event_for_exists(event_name)

    seminars = models.Seminar.objects.filter(name=event_name).values_list('member_id')

    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
        member_id = services.get_id(row[4].value)

        if seminars.filter(member_id=member_id).exists():
            continue

        seminar = models.Seminar()
        seminar.name = event_name
        seminar.club = row[7].value
        seminar.trainer = row[8].value
        seminar.city = row[11].value
        seminar.start_date = row[10].value
        seminar.attestation_date = row[12].value
        seminar.oldKu = services.get_ku(row[3].value)
        seminar.newKu = services.get_ku(row[13].value)
        seminar.isChild = True if row[14].value == '+' else False
        seminar.examiner = row[15].value

        trainer_id = services.get_id(row[9].value)
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
                seminar.member = aikiboy
                seminar.save()
            else:
                raise ArgumentError(f"Ошибка в строке {row[0].row}")
        else:
            aikiboy = models.Aikido_Member.objects.get(id=member_id)
            seminar.member = aikiboy
            seminar.save()



@transaction.atomic
def createXlsxFromRequests(eventName):
    wb = openpyxl.Workbook(iso_dates=True)
    workSheet = wb.active
    workSheet.append(['Фамилия', 'Имя', 'Отчество', 'степень кю/дан', '#ID', 'Дата рождения',
                      'Регион', 'Клуб', 'Тренер', 'id тренера', 'семинар', 'место проведения', 'аттестация',
                      'Присвоенная степень', 'детский', 'Экзаменатор'])
    services.set_blue_row(workSheet)
    requests = models.Request.objects.filter(event_name=eventName)
    if not requests.exists():
        raise ArgumentError('Не существует такого мероприятия')

    event = models.Events.objects.get(event_name=eventName)

    for request in requests.values():
        if request['member_id'] is not None:
            member = models.Aikido_Member.objects.get(id=request['member_id'])
            workSheet.append(services.create_row(request, event, member))
        else:
            workSheet.append(services.create_row(request, event))

    for i in workSheet.iter_rows(min_row=1, max_row=workSheet.max_row):
        i[5].number_format = numbers.FORMAT_DATE_DDMMYY
        i[10].number_format = numbers.FORMAT_DATE_DDMMYY
        i[12].number_format = numbers.FORMAT_DATE_DDMMYY

    wb.save(f"{eventName}.xlsx")
    wb.close()
    return f"{eventName}.xlsx"
