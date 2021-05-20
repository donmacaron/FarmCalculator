import random
from FarmCalculator import db
from FarmCalculator.models import Feed, CurrentValues, Movement


db.drop_all()
db.create_all()

r_types = ['Молодняк', 'Взрослый', 'Старый']
cur_vals = [db.session.add(CurrentValues(rabbit_type=x, amount=random.randrange(150, 500))) for x in r_types]
feed_list = ['Зелёный корм', 'Корнеклубнеплоды', 'Сено', 'Веточный корм', 'Концентрированный корм', 'Минеральный корм']
feed = [db.session.add(Feed(name=x, amount=0)) for x in feed_list]
mov = [db.session.add(Movement(type='Transfers', feed_type=x, amount=0, provider='0')) for x in feed_list]
mov2 = [db.session.add(Movement(type='Receits', feed_type=x, amount=0, provider='0')) for x in feed_list]
db.session.commit()
