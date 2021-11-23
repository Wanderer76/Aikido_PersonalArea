import datetime
from openpyxl.styles import PatternFill
from PersonalArea import models
from ctypes import ArgumentError


def get_id(record):
    if record is None:
        return generate_id()
    if isinstance(record, int):
        return int(record)
    else:
        if isinstance(record, str):
            if record[0] == '№':
                return int(record[1::])
            else:
                return int(record)
        raise ArgumentError(f"Ячейка заполнена не правильно {record}")


def get_ku(record):
    if isinstance(record, int):
        return record
    else:
        if "дан" in record:
            ku = record.replace('дан', '')
            if isinstance(ku, int):
                return 10 + ku
            else:
                return 10 + len(list(ku))
        elif 'кю' in record:
            return int(record.replace(' ', '').replace("кю", ""))
        else:
            raise ArgumentError(f'Не правильно заполнена ячейка {record}')


def parse_eu_date_to_us(record):
    if len(record.split(' ')) > 1:
        return record.split(' ')[0]
    return datetime.datetime.strptime(record, "%d.%m.%Y").strftime("%Y-%m-%d")


def set_trainer_status(trainer_id):
    if models.Aikido_Member.objects.filter(id=trainer_id).exists():
        trainer = models.Aikido_Member.objects.get(id=trainer_id)
        trainer.isTrainer = True
        trainer.save()


def create_row(request, event, member=None):
    trainer = models.Aikido_Member.objects.get(id=request['trainer_id'])
    oldKu = ''
    if member is not None:
        lastSeminar = models.Seminar.objects.filter(member=member).order_by('attestation_date').values_list('newKu')
        if lastSeminar.exists():
            oldKu = lastSeminar[0][0]
    second_name = '' if request['second_name'] is None else request['second_name']
    member_id = member.id if member is not None else ''
    return [
        request['surname'], request['name'], second_name, oldKu, member_id,
        request['birthdate'],
        trainer.region,
        trainer.club,
        f"{trainer.surname} {trainer.name[0]}.{trainer.second_name[0]}",
        trainer.id,
        event.start_record_date, event.city,
        event.date_of_event, '', '', '']


def set_blue_row(workSheet):
    for row in workSheet.iter_rows(min_row=1, max_row=1):
        for cell in row:
            cell.fill = PatternFill(patternType='solid', start_color='538dd5', end_color='538dd5')


def generate_id():
    ids = sorted(models.Aikido_Member.objects.values_list("id", flat=True))
    limit = ids[-1]
    missingNumbers = list(set(range(1, limit + 1)) - set(ids))
    return missingNumbers[0]


def check_event_for_exists(event_name):
    if models.Seminar.objects.filter(name=event_name).exists():
        return True
    return False

def get_day_before(date_of_event):
    return datetime.datetime(date_of_event.year, date_of_event.month, date_of_event.day - 1, 23, 59, 59, 0)
