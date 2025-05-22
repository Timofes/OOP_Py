from database import Database
from models.musical_instrument import MusicalInstrument
from models.drum import Drum
from models.flute import Flute

class Menu:
    def __init__(self, db_params):
        self.db = Database(**db_params)
    
    def create_instrument(self, body_color, body_material):
        return MusicalInstrument(self.db, body_color, body_material).save()
    
    def get_instrument(self, instrument_id):
        return MusicalInstrument.get_by_id(self.db, instrument_id)
    
    def get_all_instruments(self):
        return MusicalInstrument.get_all(self.db)
    
    def delete_instrument(self, instrument_id):
        instrument = self.get_instrument(instrument_id)
        if instrument:
            return instrument.delete()
        return None
    
    def create_drum(self, form, diameter, instrument_id):
        instrument = self.get_instrument(instrument_id)
        if not instrument:
            raise ValueError("Инструмент не найден")
        return Drum(self.db, form, diameter, instrument).save()
    
    def get_drum(self, drum_id):
        return Drum.get_by_id(self.db, drum_id)
    
    def get_all_drums(self):
        return Drum.get_all(self.db)
    
    def delete_drum(self, drum_id):
        drum = self.get_drum(drum_id)
        if drum:
            return drum.delete()
        return None
    
    def create_flute(self, count_hole, holder_method, instrument_id):
        instrument = self.get_instrument(instrument_id)
        if not instrument:
            raise ValueError("Инструмент не найден")
        return Flute(self.db, count_hole, holder_method, instrument).save()
    
    def get_flute(self, flute_id):
        return Flute.get_by_id(self.db, flute_id)
    
    def get_all_flutes(self):
        return Flute.get_all(self.db)
    
    def delete_flute(self, flute_id):
        flute = self.get_flute(flute_id)
        if flute:
            return flute.delete()
        return None
    
    def close(self):
        self.db.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
