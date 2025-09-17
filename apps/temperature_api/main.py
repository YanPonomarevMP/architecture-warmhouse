import datetime
from enum import Enum
import random

from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict
from starlette import status

app = FastAPI()


class DeviceType(Enum):
    temperature = "temperature"
    gate = "gate"
    lighting = "lighting"


class StatusBody(Enum):
    turn_on = "turn_on"
    turn_off = "turn_off"


class UnitOfMeasurement(Enum):
    fahrenheit = "fahrenheit"
    celsius = "celsius"


class TemperatureData(BaseModel):
    id: str
    ip_address: str
    timestamp: int
    temperature: str
    unit_of_measurement: UnitOfMeasurement


class MonitorResponses(BaseModel):
    id: str
    data: TemperatureData


class Device(BaseModel):
    id: str
    type: DeviceType


class TemperatureResponse(BaseModel):
    value: float = Field(..., alias="Value")
    unit: str = Field("unit", alias="Unit")
    status: str = Field("status", alias="Status")
    timestamp: datetime.datetime = Field(..., alias="Timestamp")
    location: str = Field(..., alias="Location")
    sensorid: str = Field("sensorid", alias="SensorID")
    sensortype: str = Field("sensortype", alias="SensorType")
    description: str = Field("description", alias="Description")

    model_config = ConfigDict(validate_by_name=True, serialize_by_alias=True)


class DeviceBody(BaseModel):
    id: str
    type: DeviceType


class NotFound(BaseModel):
    id: str


@app.get(
    "/devices/{id_or_slug}/monitor",
    response_model=MonitorResponses,
    name="devices:get_device_monitor_by_id",
    status_code=status.HTTP_200_OK,
    summary="Мониторинг устройства по его ID",
)
async def get_device_monitor_by_id(id_or_slug: str):
    pass


@app.post(
    "/devices/",
    response_model=Device,
    name="devices:create_device",
    status_code=status.HTTP_200_OK,
    summary="Создание нового устройства",
)
async def create_device(device_body: DeviceBody):
    pass


@app.delete(
    "/devices/{id_or_slug}",
    response_model=Device,
    name="devices:delete_device",
    status_code=status.HTTP_200_OK,
    summary="Удаление устройства",
)
async def delete_device(id_or_slug: str):
    pass


@app.put(
    "/devices/{id_or_slug}/status",
    response_model=Device,
    name="devices:turn_off_device",
    status_code=status.HTTP_200_OK,
    summary="Включение и выключение устройства",
)
async def turn_off_device(id_or_slug: str, status_body: StatusBody):
    pass


@app.get(
    "/temperature/{location}",
    response_model=TemperatureResponse,
    name="devices:get_temperature_by_location",
    status_code=status.HTTP_200_OK,
    summary="Рандомное значение температуры",
)
async def get_temperature_by_location(location: str):
    temperature = random.randint(-100, 100)
    timestamp = datetime.datetime.now(tz=datetime.timezone.utc)
    return TemperatureResponse(value=temperature, location=location, timestamp=timestamp)
