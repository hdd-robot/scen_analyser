from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import mapper, sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql.expression import func
import models

class db_manager:
    def __init__(self):
        self.engine = create_engine("mysql://root:mysqlpass@127.0.0.1/labello_db_v2")
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        session = sessionmaker()
        session.configure(bind=self.engine)
        self.session = session()



    def create_tables(self):
        """ Create tables in database """
        models.Base.metadata.create_all(self.engine)

    def add_color(self, color, hex=""):
        color_obj = models.Color()
        color_obj.col_name = color
        color_obj.col_hex_value = hex
        self.session.add(color_obj)
        self.session.commit()

    def get_colors(self):
        color_res = self.session.query(models.Color).all()
        lst = []
        for e in color_res:
            # dico = {}
            # dico["col_name"] = e.col_name;
            # dico["col_hex_value"] = e.col_hex_value;
            # lst.append(dico)

            dico = []
            dico.append(e.col_name)
            dico.append(e.col_hex_value)
            lst.append(dico)
        return (lst)

    def get_last_object(self):
        last_obj_id = self.session.query(func.max(models.Object.obj_id)).one()
        return last_obj_id[0]

    def get_object_by_id(self, obj_id):
        obj = self.session.query(models.Object).where(models.Object.obj_id == obj_id).one()
        return obj.as_dict()
















