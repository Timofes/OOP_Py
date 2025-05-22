from database import Database

class MusicalInstrument:
    TABLE_NAME = 'musical_instrument'
    
    def __init__(self, db: Database, body_color=None, body_material=None, id=None):
        self.db = db
        self.id = id
        self.body_color = body_color
        self.body_material = body_material
    
    def save(self):
        if self.id is None:
            query = f"""
                INSERT INTO {self.TABLE_NAME} (body_color, body_material) 
                VALUES (%s, %s) RETURNING id
            """
            result = self.db.execute(query, (self.body_color, self.body_material), fetch=True)
            self.id = result[0]['id']
        else:
            query = f"""
                UPDATE {self.TABLE_NAME} 
                SET body_color = %s, body_material = %s 
                WHERE id = %s
            """
            self.db.execute(query, (self.body_color, self.body_material, self.id))
        return self
    
    def delete(self):
        if self.id is not None:
            query = f"DELETE FROM {self.TABLE_NAME} WHERE id = %s"
            self.db.execute(query, (self.id,))
            self.id = None
        return self
    
    @classmethod
    def get_by_id(cls, db: Database, instrument_id):
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE id = %s"
        result = db.execute(query, (instrument_id,), fetch=True)
        return cls(db, **result[0]) if result else None
    
    @classmethod
    def get_all(cls, db: Database):
        query = f"SELECT * FROM {cls.TABLE_NAME}"
        return [cls(db, **row) for row in db.execute(query, fetch=True)]
    
    def __str__(self):
        return f"Instrument(id={self.id}, color={self.body_color}, material={self.body_material})"
