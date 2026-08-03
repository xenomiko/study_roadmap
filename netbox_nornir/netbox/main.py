# main.py
from schemas import (
    SiteCreate,
    ManufacturerCreate,
    RoleCreate,
    DeviceTypeCreate,
    NetBoxDeviceCreate,
    ConfigContextCreate,
)
from netbox_services import (
    get_netbox_client,
    load_device_data,
    resolve_object_id,
    sync_resources,
)
from dotenv import load_dotenv


def main():
    load_dotenv()
    nb = get_netbox_client()
    data = load_device_data("netbox.yaml")

    sync_resources(nb.dcim.sites, data.get("sites", []), SiteCreate)
    sync_resources(
        nb.dcim.manufacturers, data.get("manufacturers", []), ManufacturerCreate
    )
    sync_resources(nb.dcim.device_roles, data.get("roles", []), RoleCreate)

    device_types_data = data.get("device_types", [])
    for dt in device_types_data:
        dt["manufacturer"] = resolve_object_id(
            nb.dcim.manufacturers, dt["manufacturer"]
        )

    sync_resources(
        nb.dcim.device_types,
        device_types_data,
        DeviceTypeCreate,
    )

    devices_data = data.get("devices", [])
    for dev in devices_data:
        dev["site"] = resolve_object_id(nb.dcim.sites, dev["site"])
        dev["device_type"] = resolve_object_id(nb.dcim.device_types, dev["device_type"])
        dev["role"] = resolve_object_id(nb.dcim.device_roles, dev["role"])

    sync_resources(
        nb.dcim.devices, devices_data, NetBoxDeviceCreate, lookup_field="name"
    )
    config_contexts_data = data.get("config_contexts", [])
    relation_endpoints = {
        "regions": nb.dcim.regions,
        "site_groups": nb.dcim.site_groups,
        "sites": nb.dcim.sites,
        "locations": nb.dcim.locations,
        "device_types": nb.dcim.device_types,
        "roles": nb.dcim.device_roles,
        "platforms": nb.dcim.platforms,
        "cluster_groups": nb.virtualization.cluster_groups,
        "clusters": nb.virtualization.clusters,
        "tenant_groups": nb.tenancy.tenant_groups,
        "tenants": nb.tenancy.tenants,
    }
    for cc in config_contexts_data:
        for field, endpoint in relation_endpoints.items():
            if field in cc and cc[field]:
                cc[field] = [resolve_object_id(endpoint, slug) for slug in cc[field]]
    sync_resources(
        nb.extras.config_contexts,
        config_contexts_data,
        ConfigContextCreate,
        lookup_field="name",
    )


if __name__ == "__main__":
    main()
