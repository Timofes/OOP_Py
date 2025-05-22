from models.musical_instrument import MusicalInstrument
from database import Database

class Flute(MusicalInstrument):
    TABLE_NAME = 'flute'
    
    def __init__(self, db: Database, count_hole=None, holder_method=None, musical_instrument=None, id_flute=None):
        super().__init__(db, 
                       body_color=musical_instrument.body_color if musical_instrument else None,
                       body_material=musical_instrument.body_material if musical_instrument else None,
                       id=musical_instrument.id if musical_instrument else None)
        self.id_flute = id_flute
        self.count_hole = count_hole
        self.holder_method = holder_method
        self._musical_instrument = musical_instrument
    
    @property
    def musical_instrument(self):
        return self._musical_instrument
    
    @musical_instrument.setter
    def musical_instrument(self, value):
        self._musical_instrument = value
        self.body_color = value.body_color
        self.body_material = value.body_material
        self.id = value.id
    
    def save(self):
        if not self.musical_instrument:
            raise ValueError("Требуется связанный музыкальный инструмент")
        
        self.musical_instrument.save()
        
        if self.id_flute is None:
            query = f"""
                INSERT INTO {self.TABLE_NAME} (count_hole, holder_method, id_musical) 
                VALUES (%s, %s, %s) RETURNING id_flute
            """
            result = self.db.execute(query, (self.count_hole, self.holder_method, self.id), fetch=True)
            self.id_flute = result[0]['id_flute']
        else:
            query = f"""
                UPDATE {self.TABLE_NAME} 
                SET count_hole = %s, holder_method = %s, id_musical = %s 
                WHERE id_flute = %s
            """
            self.db.execute(query, (self.count_hole, self.holder_method, self.id, self.id_flute))
        return self
    
    def delete(self):
        if self.id_flute is not None:
            query = f"DELETE FROM {self.TABLE_NAME} WHERE id_flute = %s"
            self.db.execute(query, (self.id_flute,))
            self.id_flute = None
        return self
    
    @classmethod
    def get_by_id(cls, db: Database, flute_id):
        query = f"""
            SELECT f.*, mi.body_color, mi.body_material 
            FROM {cls.TABLE_NAME} f
            JOIN musical_instrument mi ON f.id_musical = mi.id
            WHERE f.id_flute = %s
        """
        result = db.execute(query, (flute_id,), fetch=True)
        if not result:
            return None
            
        data = dict(result[0])
        mi = MusicalInstrument(db, 
                             id=data['id_musical'],
                             body_color=data['body_color'],
                             body_material=data['body_material'])
        return cls(db, 
                 id_flute=data['id_flute'],
                 count_hole=data['count_hole'],
                 holder_method=data['holder_method'],
                 musical_instrument=mi)
    
    @classmethod
    def get_all(cls, db: Database):
        query = f"""
            SELECT f.*, mi.body_color, mi.body_material 
            FROM {cls.TABLE_NAME} f
            JOIN musical_instrument mi ON f.id_musical = mi.id
        """
        results = []
        for row in db.execute(query, fetch=True):
            data = dict(row)
            mi = MusicalInstrument(db, 
                                 id=data['id_musical'],
                                 body_color=data['body_color'],
                                 body_material=data['body_material'])
            results.append(cls(db, 
                            id_flute=data['id_flute'],
                            count_hole=data['count_hole'],
                            holder_method=data['holder_method'],
                            musical_instrument=mi))
        return results
    
    def __str__(self):
        return f"Flute(id={self.id_flute}, holes={self.count_hole}, holder={self.holder_method}, instrument={super().__str__()})"
