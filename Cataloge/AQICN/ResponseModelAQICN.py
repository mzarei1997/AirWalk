from typing import List, Optional
from pydantic import BaseModel
 

class AqicnAttribution(BaseModel):
    url: str
    name: str
    logo: Optional[str] = None


class AqicnCity(BaseModel):
    geo: List[float]
    name: str
    url: str
    location: str


class AqicnMeasurement(BaseModel):
    v: float


class AqicnIAQI(BaseModel):
    co: Optional[AqicnMeasurement] = None
    h: Optional[AqicnMeasurement] = None
    no2: Optional[AqicnMeasurement] = None
    o3: Optional[AqicnMeasurement] = None
    p: Optional[AqicnMeasurement] = None
    pm10: Optional[AqicnMeasurement] = None
    pm25: Optional[AqicnMeasurement] = None
    so2: Optional[AqicnMeasurement] = None
    t: Optional[AqicnMeasurement] = None
    w: Optional[AqicnMeasurement] = None
    wg: Optional[AqicnMeasurement] = None


class AqicnTimeInfo(BaseModel):
    s: str
    tz: str
    v: int
    iso: str


class AqicnForecastItem(BaseModel):
    avg: int
    day: str
    max: int
    min: int


class AqicnDailyForecast(BaseModel):
    o3: Optional[List[AqicnForecastItem]] = None
    pm10: Optional[List[AqicnForecastItem]] = None
    pm25: Optional[List[AqicnForecastItem]] = None
    uvi: Optional[List[AqicnForecastItem]] = None


class AqicnForecast(BaseModel):
    daily: AqicnDailyForecast


class DebugInfo(BaseModel):
    sync: str


class AqicnQualityData(BaseModel):
    aqi: int
    idx: int
    attributions: List[AqicnAttribution]
    city: AqicnCity
    dominentpol: str
    iaqi: AqicnIAQI
    time: AqicnTimeInfo
    forecast: AqicnForecast
    debug: DebugInfo


class AqicnResponseModel(BaseModel):
    status: str
    data: AqicnQualityData