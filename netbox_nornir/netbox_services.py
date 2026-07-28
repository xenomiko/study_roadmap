import yaml
from pathlib import Path
import pynetbox
from dotenv import load_dotenv
import os
import logging
from pynetbox import RequestError
from typing import Any, Dict
from pynetbox.core.endpoint import Endpoint
from schemas import (
    NetBoxDeviceCreate,
    SiteCreate,
    RoleCreate,
    ManufacturerCreate,
    DeviceTypeCreate,
)
from typing import Union, List, Type
from pydantic import BaseModel, ValidationError
import csv

logger = logging.getLogger(__name__)


def get_netbox_client(validate_connection: bool = True) -> pynetbox.core.api.Api:
    NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")
    NETBOX_URL = os.getenv("NETBOX_URL")
    if not NETBOX_TOKEN or not NETBOX_URL:
        error_msg = (
            "Missing required environment variables: NETBOX_URL and/or" " NETBOX_TOKEN"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)
    if validate_connection:
        try:
            nb.status()
        except RequestError as e:
            error_msg = (
                f"Failed to connect or authenticate with NetBox at {NETBOX_URL}: {e}"
            )
            logger.error(error_msg)
            raise ConnectionError(error_msg) from e
    return nb


def load_device_data(file_path: Union[str, Path]):
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"yaml file not found at {path.resolve()}")
    ext = path.suffix.lower()
    try:
        with open(path, "r", encoding="utf-8-sig") as file:
            if ext in (".yaml", ".yml"):
                data = yaml.safe_load(file)
                return data if data is not None else {}
            elif ext == ".csv":
                reader = csv.DictReader(file)
                return list(reader)
            else:
                raise ValueError(
                    f"Unsupported extension '{ext}'. Use .yaml, .yml, or .csv"
                )
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file '{path.name}': {e}") from e
    except csv.Error as e:
        raise ValueError(f"Error parsing CSV file '{path.name}': {e}") from e


def resolve_object_id(
    endpoint: Endpoint, lookup_value: str, lookup_field: str = "slug"
) -> int:
    search_kwargs = {lookup_field: lookup_value}
    obj = endpoint.get(**search_kwargs)
    if obj is None:
        raise ValueError(
            f"Could not find '{lookup_value}' in '{endpoint.name}' using field '{lookup_field}'."
        )
    return obj.id


def get_or_create_object(
    endpoint: Endpoint, lookup_kwargs: Dict[str, Any], payload: BaseModel
):
    payload_dict = payload.model_dump(exclude_none=True)
    try:
        existing_obj = endpoint.get(**lookup_kwargs)
        if existing_obj:
            logger.info(
                f"[{endpoint.name}] Object already exists matching {lookup_kwargs}."
            )
            return existing_obj
        created_obj = endpoint.create(payload_dict)
        logger.info(
            f"[{endpoint.name}] Successfully created object ID {created_obj.id}."
        )
        return created_obj
    except RequestError as e:
        logger.error(
            f"[{endpoint.name}] NetBox API request failed for {lookup_kwargs}. Error: {e}"
        )
        raise


def sync_resources(
    endpoint: Endpoint,
    items: List[Dict[str, Any]],
    model_class: Type[BaseModel],
    lookup_field: str = "slug",
):
    created_or_found_objects = []
    for raw_item in items:
        try:
            validated_payload = model_class.model_validate(raw_item)
        except ValidationError as err:
            logger.error(f"Validation failed for item {raw_item}: {err}")
            continue
        lookup_value = getattr(validated_payload, lookup_field)
        lookup_kwargs = {lookup_field: lookup_value}
        obj = get_or_create_object(
            endpoint=endpoint,
            lookup_kwargs=lookup_kwargs,
            payload=validated_payload,
        )

        created_or_found_objects.append(obj)
    return created_or_found_objects
