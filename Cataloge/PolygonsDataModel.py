from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal, Union, Optional

class PolygonGeometry(BaseModel):
    type: Literal["Polygon"]
    coordinates: List[List[List[float]]]


class MultiPolygonGeometry(BaseModel):
    type: Literal["MultiPolygon"]
    coordinates: List[List[List[List[float]]]]

class PolygonProperties(BaseModel):
    location_id: str
    display_name: str
    route_type: str

    midpoint_lat: float
    midpoint_lon: float

    area_sqm: float
    length_m: float

    surface: Optional[str] = None
    access: Optional[str] = None
    leisure: Optional[str] = None
    landuse: Optional[str] = None
    highway: Optional[str] = None
    sac_scale: Optional[str] = None
    trail_visibility: Optional[str] = None
    incline: Optional[str] = None

    route_count: int

    size_score: float
    route_score: float
    surface_score: float
    type_score: float
    compactness_score: float
    access_score: float
    pqs: float



class TurinPolygonModel(BaseModel):
    id: str = Field(alias="_id")
    geometry: Union[PolygonGeometry, MultiPolygonGeometry]
    properties: PolygonProperties