import random
from flask_bcrypt import Bcrypt as bc
from FarmCalculator import db
from FarmCalculator.models import User, Feed, CurrentValues, Movement


# pas = bc.generate_password_hash('asd').decode('utf-8')
# user = User(username='asd', password=pas, email='asd@asd.asd')
# db.session.add(user)

db.drop_all()
db.create_all()

r_types = ['Молодняк','Взрослый','Старый']
cur_vals = [db.session.add(CurrentValues(rabbit_type=x, amount=0)) for x in r_types]


feed_list = ['Зелёный корм','Корнеклубнеплоды','Сено','Веточный корм','Концентрированный корм','Минеральный корм']
feed = [db.session.add(Feed(name=x, amount=0))  for x in feed_list ]


providers = ['Счастливый Кроль','Корм-о-база','Поставщик №4','КрольСельПо']
movs = ['Transfer', 'Receit']
mov = [db.session.add(Movement(type='Transfer', feed_type=x, amount=0, provider=random.choice(providers))) for x in feed_list]
mov2 = [db.session.add(Movement(type='Receits', feed_type=x, amount=0, provider=random.choice(providers))) for x in feed_list]

db.session.commit()
