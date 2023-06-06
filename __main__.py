from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Conexión a la base de datos MariaDB
engine = create_engine('mysql+mysqlconnector://root:password@192.168.11.155:3306/bdtestsqlalchemy?charset=utf8mb4&collation=utf8mb4_general_ci')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Definición de las clases de modelo
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    order_number = Column(String(20), nullable=False)
    items = relationship('Item', back_populates='order')

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship('Order', back_populates='items')

# Creación de las tablas en la base de datos
Base.metadata.create_all(engine)

# Creación de un pedido y elementos
order = Order(order_number='ORD-001')
session.add(order)
session.commit()

item1 = Item(name='Item 1', order=order)
item2 = Item(name='Item 2', order=order)
session.add_all([item1, item2])
session.commit()

# Consulta de todos los pedidos y sus elementos
orders = session.query(Order).all()
for order in orders:
    print(f'Pedido: {order.order_number}')
    for item in order.items:
        print(f'Elemento: {item.name}')

# Cierre de la sesión
session.close()
