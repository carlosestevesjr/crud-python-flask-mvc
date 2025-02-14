from app import db

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    tz_id = db.Column(db.String(100), nullable=False)
    localtime_epoch = db.Column(db.Integer, nullable=False)
    localtime = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'region': self.region,
            'country': self.country,
            'lat': self.lat,
            'lon': self.lon,
            'tz_id': self.tz_id,
            'localtime_epoch': self.localtime_epoch,
            'localtime': self.localtime,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class Forecast(db.Model):
    __tablename__ = 'forecasts'

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    date_epoch = db.Column(db.Integer, nullable=False)
    maxtemp_c = db.Column(db.Float, nullable=False)
    maxtemp_f = db.Column(db.Float, nullable=False)
    mintemp_c = db.Column(db.Float, nullable=False)
    mintemp_f = db.Column(db.Float, nullable=False)
    avgtemp_c = db.Column(db.Float, nullable=False)
    avgtemp_f = db.Column(db.Float, nullable=False)
    maxwind_mph = db.Column(db.Float, nullable=False)
    maxwind_kph = db.Column(db.Float, nullable=False)
    totalprecip_mm = db.Column(db.Float, nullable=False)
    totalprecip_in = db.Column(db.Float, nullable=False)
    avgvis_km = db.Column(db.Float, nullable=False)
    avgvis_miles = db.Column(db.Float, nullable=False)
    avghumidity = db.Column(db.Integer, nullable=False)
    condition_text = db.Column(db.String(200), nullable=False)
    condition_icon = db.Column(db.String(200), nullable=False)
    uv = db.Column(db.Float, nullable=False)

    location = db.relationship('Location', backref=db.backref('forecasts', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'location_id': self.location_id,
            'date': self.date,
            'date_epoch': self.date_epoch,
            'maxtemp_c': self.maxtemp_c,
            'maxtemp_f': self.maxtemp_f,
            'mintemp_c': self.mintemp_c,
            'mintemp_f': self.mintemp_f,
            'avgtemp_c': self.avgtemp_c,
            'avgtemp_f': self.avgtemp_f,
            'maxwind_mph': self.maxwind_mph,
            'maxwind_kph': self.maxwind_kph,
            'totalprecip_mm': self.totalprecip_mm,
            'totalprecip_in': self.totalprecip_in,
            'avgvis_km': self.avgvis_km,
            'avgvis_miles': self.avgvis_miles,
            'avghumidity': self.avghumidity,
            'condition_text': self.condition_text,
            'condition_icon': self.condition_icon,
            'uv': self.uv,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class Astro(db.Model):
    __tablename__ = 'astros'

    id = db.Column(db.Integer, primary_key=True)
    forecast_id = db.Column(db.Integer, db.ForeignKey('forecasts.id'), nullable=False)
    sunrise = db.Column(db.String(50), nullable=False)
    sunset = db.Column(db.String(50), nullable=False)
    moonrise = db.Column(db.String(50), nullable=False)
    moonset = db.Column(db.String(50), nullable=False)
    moon_phase = db.Column(db.String(50), nullable=False)
    moon_illumination = db.Column(db.Integer, nullable=False)

    forecast = db.relationship('Forecast', backref=db.backref('astro', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'forecast_id': self.forecast_id,
            'sunrise': self.sunrise,
            'sunset': self.sunset,
            'moonrise': self.moonrise,
            'moonset': self.moonset,
            'moon_phase': self.moon_phase,
            'moon_illumination': self.moon_illumination,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
