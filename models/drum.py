from models.musical_instrument import MusicalInstrument
from database import Database

class Drum(MusicalInstrument):
    TABLE_NAME = 'drum'
    
    def __init__(self, db: Database, form=None, diameter=None, musical_instrument=None, id_drum=None):
        super().__init__(db, 
                       body_color=musical_instrument.body_color if musical_instrument else None,
                       body_material=musical_instrument.body_material if musical_instrument else None,
                       id=musical_instrument.id if musical_instrument else None)
        self.id_drum = id_drum
        self.form = form
        self.diameter = diameter
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
        
        if self.id_drum is None:
            query = f"""
                INSERT INTO {self.TABLE_NAME} (form, diameter, id_musical) 
                VALUES (%s, %s, %s) RETURNING id_drum
            """
            result = self.db.execute(query, (self.form, self.diameter, self.id), fetch=True)
            self.id_drum = result[0]['id_drum']
        else:
            query = f"""
                UPDATE {self.TABLE_NAME} 
                SET form = %s, diameter = %s, id_musical = %s 
                WHERE id_drum = %s
            """
            self.db.execute(query, (self.form, self.diameter, self.id, self.id_drum))
        return self
    
    def delete(self):
        if self.id_drum is not None:
            query = f"DELETE FROM {self.TABLE_NAME} WHERE id_drum = %s"
            self.db.execute(query, (self.id_drum,))
            self.id_drum = None
        return self
    
    @classmethod
    def get_by_id(cls, db: Database, drum_id):
        query = f"""
            SELECT d.*, mi.body_color, mi.body_material 
            FROM {cls.TABLE_NAME} d
            JOIN musical_instrument mi ON d.id_musical = mi.id
            WHERE d.id_drum = %s
        """
        result = db.execute(query, (drum_id,), fetch=True)
        if not result:
            return None
            
        data = dict(result[0])
        mi = MusicalInstrument(db, 
                             id=data['id_musical'],
                             body_color=data['body_color'],
                             body_material=data['body_material'])
        return cls(db, 
                 id_drum=data['id_drum'],
                 form=data['form'],
                 diameter=data['diameter'],
                 musical_instrument=mi)
    
    @classmethod
    def get_all(cls, db: Database):
        query = f"""
            SELECT d.*, mi.body_color, mi.body_material 
            FROM {cls.TABLE_NAME} d
            JOIN musical_instrument mi ON d.id_musical = mi.id
        """
        results = []
        for row in db.execute(query, fetch=True):
            data = dict(row)
            mi = MusicalInstrument(db, 
                                 id=data['id_musical'],
                                 body_color=data['body_color'],
                                 body_material=data['body_material'])
            results.append(cls(db, 
                            id_drum=data['id_drum'],
                            form=data['form'],
                            diameter=data['diameter'],
                            musical_instrument=mi))
        return results
    
    def __str__(self):
        return f"Drum(id={self.id_drum}, form={self.form}, diameter={self.diameter}, instrument={super().__str__()})"
