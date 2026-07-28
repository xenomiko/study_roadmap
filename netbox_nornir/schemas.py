from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, Any

SLUG_PATTERN = r"^[-a-zA-Z0-9_]+$"


class NetBoxBaseSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)


class NetBoxDeviceCreate(NetBoxBaseSchema):
    name: str = Field(min_length=1)
    device_type: int
    role: int
    site: int
    status: Literal[
        "active",
        "offline",
        "staged",
        "decommissioning",
        "failed",
        "inventory",
        "planned",
    ] = "active"
    tenant: Optional[int] = None
    platform: Optional[int] = None
    serial: Optional[str] = Field(default=None, min_length=1)
    asset_tag: Optional[str] = Field(default=None, min_length=1)
    rack: Optional[int] = None
    position: Optional[float] = None
    face: Optional[Literal["front", "rear"]] = None
    location: Optional[int] = None
    custom_fields: Optional[dict[str, Any]] = None


class SiteCreate(NetBoxBaseSchema):
    name: str = Field(min_length=1)
    slug: str = Field(min_length=1, max_length=100, pattern=SLUG_PATTERN)
    status: Optional[
        Literal["active", "planned", "staging", "decommissioning", "retired"]
    ] = None
    region: Optional[int] = None
    group: Optional[int] = None
    time_zone: Optional[str] = Field(default=None, min_length=1)


class RoleCreate(NetBoxBaseSchema):
    name: str = Field(min_length=1)
    slug: str = Field(min_length=1, max_length=100, pattern=SLUG_PATTERN)
    config_template: Optional[int] = None
    vm_role: Optional[bool] = None


class ManufacturerCreate(NetBoxBaseSchema):
    name: str = Field(min_length=1)
    slug: str = Field(min_length=1, max_length=100, pattern=SLUG_PATTERN)


class DeviceTypeCreate(NetBoxBaseSchema):
    model: str = Field(min_length=1)
    slug: str = Field(min_length=1, max_length=100, pattern=SLUG_PATTERN)
    manufacturer: int
    part_number: Optional[str] = Field(default=None, min_length=1)
