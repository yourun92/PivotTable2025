import pandas as pd
import re



def cities_process(city):
    if not isinstance(city, str):
        return pd.NaT  # или city, если хочешь оставить значение


    city = city.lower().strip()

    cities = {'МО': 'Московская область',
              'Новочеркасск, Ростовская обл.': 'Новочеркасск',
              'Аксайск': 'Аксай',
              'Алтай': 'Алтайский край',
              'Амурская обл': 'Амурская область',
              'Артем': 'Артём',
              'Арханг.обл': 'Архангельская область',
              'Астраханская обл': 'Астраханская область',
              'Астахань': 'Астрахань',
              'Башкирия': 'Башкортостан',
              'Братск (Иркутск)': 'Братск',
              'В.Луки': 'Великие Луки',
              'В.Новгород': 'Великий Новгород',
              'вел нов.': 'Великий Новгород',
              'Владик': 'Владивосток',
              'Владимир обл': 'Владимирская область',
              'Выкса, Нижний': 'Выкса',
              'Джержинский': 'Дзержинский',
              'Дзнржинск': 'Дзержинск',
              'Димитров': 'Дмитров',
              'екат': 'Екатеринбург',
              'Екатерианбург': 'Екатеринбург',
              'ЕКБ': 'Екатеринбург',
              'Йоршкар-Ола': 'Йошкар-Ола',
              'Кабицино': 'Кабицыно',
              'Каменск шахтинск': 'Каменск-Шахтинский',
              'Каменск Шахтинский': 'Каменск-Шахтинский',
              'Комсомольск на Амуре': 'Комсомольск-на-Амуре',
              'Котдас': 'Котлас',
              'Крастоярск': 'Красноярск',
              'Лен обл': 'Ленинградская область',
              'Лен.обл': 'Ленинградская область',
              'Магнитогорс': 'Магнитогорск',
              'Махачкала аэродром': 'Махачкала',
              'МО Руза': 'Московская область',
              'МО, Химки': 'Московская область',
              'Москвва': 'Москва',
              'мс': 'Москва',
              'мск': 'Москва',
              'Н. Тагил': 'Нижний Тагил',
              'Н. Челны': 'Набережные Челны',
              'Н.Новгорд': 'Нижний Новгород',
              'Н.Новгород': 'Нижний Новгород',
              'Н.Тагил': 'Нижний Тагил',
              'Н.Фоминск': 'Наро-Фоминск',
              'Н.Челны': 'Набережные Челны',
              'Наб. Челны': 'Набережные Челны',
              'Наб.Челны': 'Набережные Челны',
              'Наро Фоминск': 'Наро-Фоминск',
              'Невинномысск': 'Невиномысск',
              'Нижний': 'Нижний Новгород',
              'Нижний нов': 'Нижний Новгород',
              'Нижний новгород': 'Нижний Новгород',
              'НН': 'Нижний Новгород',
              'Новорос': 'Новороссийск',
              'новороссийск': 'Новороссийск',
              'Новосиб': 'Новосибирск',
              'Новоссибирск': 'Новосибирск',
              'Н-Челны': 'Набережные Челны',
              'Орел': 'Орёл',
              'Орехово Зуево': 'Орехово-Зуево',
              'П.Посад': 'Павлов Пасад',
              'Павлов.Пасад': 'Павлов Пасад',
              'Пермь, Березняки': 'Березняки',
              'Петр.-Камчатск.': 'Петропавловск-Камчатский',
              'Петропавловск-Камч': 'Петропавловск-Камчатский',
              'П-К': 'Петропавловск-Камчатский',
              'Псеов': 'Псков',
              'Реутов МО': 'Реутов',
              'Р-на-Д': 'Ростов-на-Дону',
              'РнД': 'Ростов-на-Дону',
              'Роств н/д': 'Ростов-на-Дону',
              'Ростов': 'Ростов-на-Дону',
              'Ростов н/д': 'Ростов-на-Дону',
              'Ростов на дону': 'Ростов-на-Дону',
              'Ростов-на-До': 'Ростов-на-Дону',
              'С Посад': 'Сергиев Посад',
              'Сарат': 'Саратов',
              'Сарат.обл.': 'Саратовская область',
              'Семферополь': 'Симферополь',
              'Сергиев-Посад': 'Сергиев Посад',
              'Симферопль': 'Симферополь',
              'С-П': 'Санкт-Петербург',
              'спб': 'Санкт-Петербург',
              'С-Посад': 'Сергиев Посад',
              'Ставрапольский край': 'Ставропольский край',
              'Старица, Твер обл': 'Старица',
              'Тамбрв': 'Тамбов',
              'Тульская обл,гСуворов': 'Суворов',
              'Усть Луг': 'Усть-Луга',
              'Ханты-Манс': 'Ханты-Мансийск',
              'Челяба': 'Челябинск',
              'Чечня, Грозный': 'Грозный',
              'Чечня': 'Грозный',
              'Щелково': 'Щёлково',
              'Южно - Сахалинск': 'Южно-Сахалинск',
              'Южно Сахалинск': 'Южно-Сахалинск',
              'ЮжСахалинск': 'Южно-Сахалинск',
              'Якутия': 'Якутск',
              'Яроссславль': 'ярославль',
              'Нижний новг': 'Нижний Новгород',
              'Новоросийск': 'Новоросcийск',
              'Эсто-садок, сочи': 'Эсто-садок',
              'Эстосадок': 'Эсто-садок',
              'Питер': 'Санкт-Петербург',
              'Новгород обл': 'Новгородская область',
              'Буденовск': 'Будённовск',
              'Мурманская обл': 'Мурманская область',
              'Республика башкортостан': 'Башкортостан',
              'Сахалин': 'Сахалинская область',
              'Свердловск': 'Екатеринбург',
              'Эсто-садок': 'Эстосадок'
        }

    to_delete = list(map(lambda x: x.lower().strip(), [
        '2762доставка', '30.11 -1забор(13т.шт)', '45шт доставили',
        '8208', '9,5м3', 'VJ'
    ]))

    # нормализуем ключи словаря
    normalized_cities = {k.lower().strip(): v for k, v in cities.items()}

    if city in to_delete:
        return pd.NaT
    return normalized_cities.get(city, city).capitalize()


def supplier_process(supplier):
    if not isinstance(supplier, str):
        return pd.NaT  # или city, если хочешь оставить значение

    supplier = supplier.upper().strip()

    # Удаляем организационно-правовую форму (ООО, ИП, ЗАО, ОАО и т.п.)
    supplier = re.sub(r'\b(ООО|ИП|ОАО|ЗАО|ПАО|НАО|АО|ГК|ТД|МСК|-МСК|МОСКВА|ТК)\b\.?', '', supplier, flags=re.IGNORECASE)

    supplier = supplier.replace('"', '').replace("«", '').replace("»", '')
    supplier = re.sub(r'\([^)]*\)', '', supplier)
    supplier = re.sub(r'\s{2,}', ' ', supplier)
    supplier = ' | '.join([part.strip() for part in re.split(r'[{}]'.format(re.escape('+/,\\')), supplier) if part.strip()])

    suppliers = {
        'АКВАБ' : 'АКВАБАРЬЕР',
        'АКВАБАЛЬЕР': 'АКВАБАРЬЕР',
        'АКВАБАРЬНР': 'АКВАБАРЬЕР',
        'АКВАБАРЬР': 'АКВАБАРЬЕР',
        'АКВАБАРЬРЕР': 'АКВАБАРЬЕР',
        'АКВАБОРЬЕР': 'АКВАБАРЬЕР',
        'АКВАБПРЬЕР': 'АКВАБАРЬЕР',
        'АКВАБРЬЕР': 'АКВАБАРЬЕР',
        'АКВА': 'АКВАИНЖИНИРИНГ',
        'АКВА-ИНЖИНИРИНГ': 'АКВАИНЖИНИРИНГ',
        'АКВАИШЖИНИРИНГ': 'АКВАИНЖИНИРИНГ',
        'АКВБАРЬЕР': 'АКВАБАРЬЕР',
        'АЛЬМ ФАЗА': 'АЛЬМ-ФАЗА',
        'АЛЬМФАЗА': 'АЛЬМ-ФАЗА',
        'АМ ГРУП': 'АМ-ГРУП',
        'АМ ГРУПП': 'АМ-ГРУП',
        'АМГ': 'АМ-ГРУП',
        'АМГРУПП': 'АМ-ГРУП',
        'АМ-ГРУПП': 'АМ-ГРУП',
        'АММГРУПП': 'АМ-ГРУП',
        'АММ-ГРУПП': 'АМ-ГРУП',
        'АРОТЕРА': 'АРОТЕРРА',
        'АРТ': 'АРТ-СТРОЙ',
        'АРТ СТРОЙ': 'АРТ-СТРОЙ',
        'АКВАБ | ИЗОМИР': 'АКВАБАРЬЕР',
        'АРТЕГОСТРОЙ': 'АРТЕГО-СТРОЙ',
        'АРТСТОЙ': 'АРТ-СТРОЙ',
        'АРТСТРОЙ': 'АРТ-СТРОЙ',
        'БАУСТРОВ': 'БАУСТОВ',
        'БД': 'БД ГРУПП',
        'БЕРГАЙФ': 'БЕРГАУФ',
        'БИРСС': 'БИРС',
        'БИУРС': 'БИРС',
        'БЕФАСТ': 'БИФАСТ',
        'БКРГАУФ': 'БЕРГАУФ',
        'БТАГРУПП': 'БТА ГРУПП',
        'БУРГАУФ': 'БЕРГАУФ',
        'ВЕНТ СНАБ': 'ВЕНТСНАБ',
        'ВЕНТСТНАБ': 'ВЕНТСНАБ',
        'ВИЛП': 'ВИЛПЕ',
        'ВИЛПИ': 'ВИЛПЕ',
        'ВКС': 'ВКС ГРУПП',
        'ГИДМАКС ТРЕЙД': 'ГИДМАКС',
        'ГИДМАКС-ТРЕЙД': 'ГИДМАКС',
        'ГИДРОГАРАНТ': 'ГИДРО-ГАРАНТ',
        'ГИДРОЗО': 'ГИДРОИЗОЛ',
        'ГИЛРОМИКС': 'ГИДРОМИКС',
        'ПАРТНЕР': 'ПАРТНЕР',
        '-ПАРТНЕР': 'ПАРТНЕР',
        'ГЛОБАЛ- КРЕП': 'ГЛОБАЛ КРЕП',
        'ДЖЕФЛЕС': 'ДЖИ ФЛЕКС',
        'ДЖИФЛЕКС': 'ДЖИ ФЛЕКС',
        'ДИФЕРРО': 'ДИФЕРО',
        'ДЬЮМАРКЕТ': 'ДЬЮМАРК',
        'ДЮМАРК': 'ДЬЮМАРК',
        'ИЗОМИР (135380': 'ИЗОМИР',
        'К ОБСТРОЙТЕХ': 'ОБСТРОЙТЕХ',
        'КАЛЕА ТОРГ': 'КАЛЕА',
        'КАЛЕЯ': 'КАЛЕА',
        'КАЛЬМАТРОН-СПБ': 'КАЛЬМАТРОН',
        'КЕЛЬНЕР': 'КЁЛЬНЕР',
        'КЁЛНЕР': 'КЁЛЬНЕР',
        'КОНТРАСТ-ВАЛЯ': 'КОНТРАСТ',
        'КОЭЛЬНЕР': 'КЁЛЬНЕР',
        'КОЭЛЬНЕР ТРЕЙДИНГ КЛД': 'КЁЛЬНЕР',
        'КРОЗ -ОГНЕЗАЩИТА': 'КРОЗ',
        'КРОЗ-ОГНЕЗАЩИТА': 'КРОЗ',
        'МЕЛПЛАСТ': 'МЕЛТПЛАСТ',
        'МЕЛЬПЛАСТ': 'МЕЛТПЛАСТ',
        'МЕТРОСТОЙСЕРВИС': 'МЕТРОСТРОЙСЕРВИС',
        'МЕТСРОЙ': 'МЕТРОСТРОЙСЕРВИС',
        'МЕТСТРОЙ': 'МЕТРОСТРОЙСЕРВИС',
        'НПО ВКС': 'НПО ВКС ГРУПП',
        'НПП': 'НПП ИЗОЛЯЦИЯ',
        'ОГНЕЗАЩИТНЫЕ РЕШЕНИЯ': 'ОГНЕЗА',
        'ОПТИМЛЬНОЕ РЕШЕНИЕ': 'ОПТИМАЛЬНОЕ РЕШЕНИЕ',
        'РЕДВЕНД': 'РЕДВЕНТ',
        'РОКСЫ': 'РОКС',
        'СВС': 'СВС МАРКЕТ',
        'СВС-МАРКЕТ': 'СВС МАРКЕТ',
        'СЕРДУС': 'СЕДРУС',
        'СКК ХХI': 'СКК',
        'СКОРП': 'СКОРП СИСТЕМ',
        'СКОРПИОН': 'СКОРП СИСТЕМ',
        'СКОРПС': 'СКОРП СИСТЕМ',
        'СКОРПСИСТ.': 'СКОРП СИСТЕМ',
        'СКОРПСИСТЕМ': 'СКОРП СИСТЕМ',
        'СКС': 'СКОРП СИСТЕМ',
        'СТЕКЛОПДАСТИКОВЫЕ ТЕХНОЛОГИИ': 'СТЕКЛОПЛАСТИКОВЫЕ ТЕХНОЛОГИИ',
        'СТЕКЛОПЛ. ТЕХГОЛОГИИ': 'СТЕКЛОПЛАСТИКОВЫЕ ТЕХНОЛОГИИ',
        'СТЕКЛОПЛ.ТЕХНОЛОГИИ': 'СТЕКЛОПЛАСТИКОВЫЕ ТЕХНОЛОГИИ',
        'СТЕКЛОПЛПСТИКОВЫЕ ТЕХНОЛОГИИ': 'СТЕКЛОПЛАСТИКОВЫЕ ТЕХНОЛОГИИ',
        'СТРОЙКРОВ КОМПЛЕКТ': 'СТРОЙКРОВКОМПЛЕКТ',
        'СТРОЙКРОВКОМПЛЕКТ XXI': 'СТРОЙКРОВКОМПЛЕКТ',
        'СТРОЙКРОВКОМПЛЕКТ СЛИСАРЕНКО': 'СТРОЙКРОВКОМПЛЕКТ',
        'СТРОЙ-РЕЗЕРВ )': 'СТРОЙ-РЕЗЕРВ',
        'СТРОЙСЕКЛО': 'СТРОЙСТЕКЛО',
        'СТРОЙТСЕКЛО': 'СТРОЙСТЕКЛО',
        'ТЕНТМАРКЕТ': 'ТЕНТ МАРКЕТ',
        'ТЕНТ-МАРКЕТ': 'ТЕНТ МАРКЕТ',
        'ТЕРМОКЛИП 1': 'ТЕРМОКЛИП',
        'ТЕХНОПЛЛАСТ': 'ТЕХНОПАЛСТ',
        'ТЕХНОПЛЛАСТ': 'ТЕХНОПАЛСТ',
        'ТЕХНОПОАСТ': 'ТЕХНОПАЛСТ',
        'ТЕХНОЭЛАСТ': 'ТЕХНОПАЛСТ',
        'ТИМ ПЛАСТ': 'ТИМПЛАСТ',
        'ТИМ-ПЛАСТ': 'ТИМПЛАСТ',
        'ТПК АЯСКОМ 1198': 'ТПК АЯСКОМ',
        'ФАНГРУПП': 'ФАН ГРУПП',
        'ФАСТЕНГРУП': 'ФАСТЕН',
        'ФАСТЕНГРУПП': 'ФАСТЕН',
        'ФАСТТЕН | СКОРПСИСТЕМ': 'ФАСТЕН',
        'ФАХМАН': 'ФАХМАНН',
        'ФАХМЕН': 'ФАХМАНН',
        'ФИЛИКРОВЛЯ': 'ФИЛИ КРОВЛЯ',
        'ФИЛИМАРКЕТ': '',
        'ХАТСМАН': 'ХАНТСМАН',
        'ХСИ ВАТЕРСТОП': 'ХСИ ВАТЕРС',
        'ХСИ ИЗ БАЛАШИХИ': 'ХСИ',
        'ХСИ СЕМЕНОВА': 'ХСИ',
        'ЦЕНТР СТРОЙ': 'ЦЕНТРСТРОЙ',
        'ЦЕНТРОСТРОЙ': 'ЦЕНТРСТРОЙ',
        'ЮНИРБАУ': 'ЮНИБАУ',
        '1001 КРЕПЁЖ': '1001 КРЕПЕЖ',
        '1001КРЕП': '1001 КРЕПЕЖ',
        '1001КРЕПЕЖ': '1001 КРЕПЕЖ',
        'АВТЛИН': 'АВТОЛИН',
        'АВКАБАРЬЕР': 'АКВАБАРЬЕР',
        'БАУПРОДУКТ СОИНА': 'БАУПРОДУКТ',
        'БАУПРОДУКТ ЧЕРНЫШОВ': 'БАУПРОДУКТ',
        'БИРС-Д': 'БИРС',
        'ВИЛП СПБ': 'ВИЛПЕ',
        'ВИЛПЕ РУС': 'ВИЛПЕ',
        'ГИДМАКС АНТОН': 'ГИДМАКС',
        'ПАРТНЁР': 'ПАРТНЕР',
        '': '',
        '': '',
        '': '',
    }


    supplier = supplier.upper().replace('АНДРЕЙ КАРЧЕМНЫЙ', '').replace('ЮРИЙ КАРТАВЫЙ', '').replace('РОМАН ПВТ', '').replace('ТОРГОВЫЙ ДОМ', '').replace('МАРГАРИТА КАЛАБУХОВА', '').replace('РУСЛАНД', '').replace('РУСCЛАНД', '').replace('120 И 130 МЕТРОВ ШНУРА', '')


    # Приводим названия компаний в общий вид и заразом смотрим компании по несколько в строке
    parts = []

    for co in supplier.split(' | '):
        co = co.strip('-')
        normalized = suppliers.get(co, co)
        parts.append(normalized)


    return ' | '.join(parts).upper().strip()


def customer_process(customer):
    if not isinstance(customer, str):
        return pd.NaT  # или city, если хочешь оставить значение

    customer = customer.upper().strip()

    # Удаляем организационно-правовую форму (ООО, ИП, ЗАО, ОАО и т.п.)
    customer = re.sub(r'\b(ООО|ИП|ТД|АО|СК|ОАО|ГК|ЗАО|СПО|ПАО|ПК|ТК|МОСКВА)\b\.?', '', customer, flags=re.IGNORECASE)

    customer = customer.replace('"', '').replace("«", '').replace("»", '')
    customer = re.sub(r'\s{2,}', ' ', customer)
    customer = re.sub(r'\([^)]*\)', '', customer)
    customer = customer.strip(',.+')
    customer = '-'.join([w.strip() for w in customer.split('-')])
    customers = {
        'АВАН':'АВАНГАРД',
        'АВНГАРД':'АВАНГАРД',
        'АИСС':'АИС',
        'АЙПИДЖИ':'АЙПИДЖИ КЛИМА',
        'АЙСБЕРГ АС ПКФ':'АЙСБЕРГ',
        'АКВА-СТРОЙ':'АКВАСТРОЙ',
        'АКВАТЕХ КОНТР':'АКВАТЕХ',
        'АЛСЕР':'АЛСЕРВИС',
        'АЛЬМИС':'АЛЬМИС-ИНТЕГРАЛ',
        'АЛЬФА СТРОЙ СК':'АЛЬФА-СТРОЙ',
        'АРКОНН ГРУПП':'АРКОНТ ГРУПП',
        'АРСЕНАЛ СТРОЙ':'АРСЕНАЛ-СТРОЙ',
        'АРТЕГО СТРОЙ':'АРТЕГО-СТРОЙ',
        'АРТЕМОВСКИЙ ЗАВОД ЖБИ':'АРТЁМОВСКИЙ ЗАВОД ЖБИ',
        'АРТ-СТРОЙ':'АРТ СТРОЙ',
        'АС-ГРУПП + 100 000':'АС-ГРУПП',
        'АСКОЛД':'АСКОЛЬД',
        'БВБ АЛЬЯНС':'БВБ-АЛЬЯНС',
        'БС-ИНЖИНИРГ':'БС-ИНЖИНИРИНГ',
        'БУНКЕР .РУ':'БУНКЕР РУ',
        'ВЕНТА СТРОЙ':'ВЕНТА-СТРОЙ',
        'ВЕНТОСТРОЙ':'ВЕНТСТРОЙ',
        'ВИКТОРИСТРОЙ':'ВИКТОРИ СТРОЙ',
        'ВИЛЛБАУ':'ВИЛБАУ',
        'ВИПМОНТАЖ':'ВИПМОНТАЖСТРОЙ',
        'ВИСТ ПЯТИГОРСК':'ВИСТ-ПЯТИГОРСК',
        'ВИСТ':'ВИСТ-ПЯТИГОРСК',
        'ВОЛМАКС КОНСТРАКШН':'ВОЛЛМАКС КОНСТРАКШН',
        'ВОСХОД М':'ВОСХОД-М',
        'ГДЕМАТЕРИАЛЫ':'ГДЕМАТЕРИАЛ',
        'ГДЕ МАТЕРИАЛЫ':'ГДЕМАТЕРИАЛ',
        'ГИДРОРЕМОНТ МАХАЧКАЛА':'ГИДРОРЕМОНТ-ВКК',
        'ГЛАСС-КАРКАС':'ГЛАСС-КАРКАС СТРОЙ',
        'ГЛАСС-КАРКАС-СТРОЙ':'ГЛАСС-КАРКАС СТРОЙ',
        'ДИС':'ДИС ГРУПП',
        'ДОМСТРОЙ 36':'ДОМСТРОЙ36',
        'ДОХАН-ТОРГОВЫЙ ДОМ':'ДОРХАН-ТОРГОВЫЙ ДОМ',
        'ДТМ С':'ДТМ-С',
        'ЕВРАЗ СТИЛ':'ЕВРАЗ СТИЛ БИЛДИНГ',
        'ЕВРОСТРОЙГРУП':'ЕВРОСТРОЙГРУПП',
        'ЕДУДА ВЛАДИМИР СМОЛЯКОВ':'ЕДУДА',
        'ЗАВОД СТЕЛКОМ':'ЗАВОД СТЕЛКОН',
        'ЗТО СМ':'ЗТО ССМ',
        'ИВАНУШКИН ДМИТРИЙ ЕВГЕНЬЕВИЧ':'ИВАНУШКИН',
        'ИГБ':'ИГБ ГРУПП',
        'ИЛЬЕЧЕВ':'ИЛЬИЧЕВ',
        'ИНВЕСТИНОПРОЕКТ ЮЗАО':'ИНВЕСТКИНОПРОЕКТ ЮЗАО',
        'ИНВЕСТКИНОПРОЕКТ':'ИНВЕСТКИНОПРОЕКТ ЮЗАО',
        'ИНКО':'ИНКОМ',
        'ИНТЕРТЕХЭНЕРГО':'ИНТЕРТЭХЭНЕРГО',
        'ИНТОРГ АЛЬЯНС':'ИНТОРГАЛЬЯНС',
        'КВОЛИТИБИЛДИНГ':'КВОТИБИЛДИНГ',
        'КНЯЗЕВ':'КНЯЗАВ',
        'КРЕПЁЖ ВОСТОК':'КРЕПЕЖ ВОСТОК',
        'КРЕПТОРГ+':'КРЕПТОРГ',
        'КРОВИНДУСТРИЯ':'КРОВ ИНДУСТРИЯ',
        'ЛАЗЕР ПРОМ':'ЛАЗЕРПРОМ',
        'ЛЕЩИНСКИЙ Д.В':'ЛЕЩИНСКИЙ',
        'ЛЕЩИНСКИЙ ДМИТРИЙ ВИКТОРОВИЧ':'ЛЕЩИНСКИЙ',
        'ЛОКШИН АЛЕКСАНДР':'ЛОКШИН АЛЕКСАНДР ВАЛЕРЬЕВИЧ',
        'МЕГАПОЛС':'МЕГАПОЛИС',
        'МЕТАЛЛИМПРЕС':'МЕТАЛЛИМПРЕСС',
        'МЕТАЛЛЭНЕРГО ХОЛДИНГ':'МЕТАЛЛЭНЕРГОХОЛДИНГ ГК',
        'МОСТОСТРОЙ':'МОСТОСТРОЙ-11',
        'НЕФТЕКАЗКОМПЛЕКТ ПЕНЗА':'НЕФТЕГАЗКОМПЛЕКТ ПЕНЗА',
        'О. СТОЛИЦА':'О.СТОЛИЦА',
        'О, СТОЛИЦА':'О.СТОЛИЦА',
        'ОКБ':'ОКБ ПО ТЕПЛОГЕНЕРАТОРАМ',
        'ОТДЕЛКА':'ОТДЕЛКА Л',
        'ПАЙП ПРАЙС':'ПАЙП-ПРАЙС',
        'ПАЛЬМЕТО':'ПАЛЬМЕТТО ТГМ ИНТЕРНЕШНЛ',
        'ПРОЕКТНЫЕ РЕШ':'ПРОЕКТНЫЕ РЕШЕНИЯ',
        'ПРОЕКТРОЙСЕРВИС':'ПРОЕКТСТРОЙСЕРВИС',
        'ПРОМРАЗВИТИЕ ПКФ':'ПРОМРАЗВИТИЕ',
        'ПРОМ-РАЗВИТИЕ':'ПРОМРАЗВИТИЕ',
        'ПРОМТРЕЙ':'ПРОМТРЕЙД',
        'ПРОФЕССИОНАЛЬ':'ПРОФЕССИОНАЛ',
        'ПЫЛАЕВА':'ПЫЛАЕВА ЮЛИЯ ЮРЬЕВНА',
        'РАДИУСРЕЙД':'РАДИУСТРЕЙД',
        'РАПАРТ':'РАПАРТ СЕРВИСЕЗ',
        'РЕКОНВЕРТ':'РЕКОНВЕР',
        'РЕМОНТТРАНСКОМПЛЕКТ':'РЕМОНТРАНСКОМПЛЕКТ',
        'РОКЕТ СЕАНС':'РОКЕТ САЕНС',
        'РОСТОВСЕРВИС':'РОСТОВ СЕРВИС',
        'РУСЛАН1':'РУСЛАН1',
        'РУСЛАН-1':'РУСЛАН 1',
        'РУССТРОЙ ИНВЕСТ':'РУССТРОЙИНВЕСТ',
        'РЫБИНСККОМ':'РЫБИНСККОМПЛЕКС',
        'САТКРН':'САТУРН',
        'СЕЙФАРТ':'СЕЙФОРТ',
        'СЕМИЛЕТОВ':'СЕМИЛЕТОВА',
        'СИМПЛ КОМПЛ':'СИМПЛ КОМПЛЕКТ',
        'СИМПЛ КОМПЛЕКТ ЛЮБОВЬ ТИМОШИНА':'СИМПЛ КОМПЛЕКТ',
        'СИСТЕМНЫЕ РЕШЕНИЕ':'СИСТЕМНЫЕ РЕШЕНИЯ',
        'СНАБТОРГ+':'СНАБТОРГ',
        'СПЕЦ ПРОДЖЕКТ':'СПЕЦ ПРОЖЕКТ',
        'СТАЙЛ':'СТАЙЛГРУПП',
        'СТАЙЛ ГРУПП':'СТАЙЛГРУПП',
        'СТАНДАРТ-СТРОЙ':'СТАНДАРТСТРОЙ',
        'СТАРТ-СТРОЙ':'СТАРТ СТРОЙ',
        'СТРОИТЕЛЬНЫЙ ДВОР КОМПЛЕКТАЦ':'СТРОИТЕЛЬНЫЙ ДВОР. КОМПЛЕКТАЦИЯ',
        'СТРОИТЕЛЬНЫЙ ДВОР КОМПЛ':'СТРОИТЕЛЬНЫЙ ДВОР. КОМПЛЕКТАЦИЯ',
        'СТРОИТЕЛЬНЫЙ ДВОР КОМПЛЕКТАЦИЯ':'СТРОИТЕЛЬНЫЙ ДВОР. КОМПЛЕКТАЦИЯ',
        'СТРОЙАЛЬЯНСК':'СТРОЙАЛЬЯНС',
        'СТРОЙ-КОМПЛЕКС':'СТРОЙКОМПЛЕКС',
        'СТРОЙРЕСУРС+':'СТРОЙРЕСУРС',
        'СТРОЙ-СНАБ':'СТРОЙСНАБ',
        'СТРОЙСНАБЛОГ':'СТРОЙСНАБЛОГИСТИК',
        'СТРОЙЦЕНТР+':'СТРОЙЦЕНТР',
        'СУПЕРСТРОЙ М':'СУПЕРСТРОЙ-М',
        'СУРСКИЙ ДОМ 000':'СУРСКИЙ ДОМ',
        'СФЕРА СНАБ':'СФЕРА-СНАБ',
        'ТАМБОВАГРОПРОМКОПЛЕКТ':'ТАМБОВАГРОПРОМКОМПЛЕКТ',
        'ТВОЙ ДОМЪ':'ТВОЙ ДОМ',
        'ТВОЙ ИНСТРУМЕНТ ТПК':'ТВОЙ ИНСТРУМЕНТ',
        'ТЕХНОЛОГИЯ OOO':'ТЕХНОЛОГИЯ',
        'Ф/Л':'Физическое лицо',
        'Ф/ЛИЦО':'Физическое лицо',
        'ФБ СТРОЙ':'ФБ-СТРОЙ',
        'ФЗ':'Физическое лицо',
        'ФЗИЧЕСКОЕ ЛИЦО':'Физическое лицо',
        'ФИЗ ЛИЦО':'Физическое лицо',
        'ФИЗ ЛИЦО ГОКТАШ МУРАТ':'Физическое лицо',
        'ФИЗ ЛИЦО ХСИ (':'Физическое лицо',
        'ФИЗИЧЕСКОЕ ЛИЦО С СЕМЕНОВА':'Физическое лицо',
        'ФИЗИЧКСКРЕ ЛИЦЕ': 'Физическое лицо',
        'ФИЗ-ЛИЦО': 'Физическое лицо',
        'ФИЗЛИЦО БЕССОНОВ ВЛАДИМИР': 'Физическое лицо',
        'ФИЗЛИЦО ДЖУРИЧИЧ НЕНАД': 'Физическое лицо',
        'ФИНЭКСПОРТ УРАЛ': 'ФИНЭКСПОРТУРАЛ',
        'ФИНЭКСПОРТ': 'ФИНЭКСПОРТУРАЛ',
        'Ф-Л': 'ФЛ',
        'ФЛАГМЕН ИНЖЕНИРИНГ': 'ФЛАГМАН ИНЖИНИРИНГ',
        'ХОУМ ЭНЕРГО': 'ХОУМ-ЭНЕРГО',
        'ХЭНБАУЭР ГРУПП': 'ХЭНДБАУЭР ГРУПП',
        'ЭКО-СТРОЙ': 'ЭКОСТРОЙ'
    }


    # supplier = supplier.upper().replace('', '')

    return customers.get(customer, customer).upper().strip()