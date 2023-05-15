import shutil

from app.core import utils


def get_services(app_id: str = None) -> dict:
    docker_client = utils.get_docker_client()

    images = docker_client.images.list()
    containers = docker_client.containers.list()

    if app_id is None:
        services = utils.SERVICES
    else:
        services = [service for service in utils.SERVICES if app_id in service["apps"]]

    rich_services = []
    for service in services:
        service["running"] = False
        service["downloaded"] = False
        for container in containers:
            if container.name == service["id"]:
                service["running"] = True
        for image in images:
            print(image.tags)
            if image.tags[0] == service["dockerImage"]:
                service["downloaded"] = True
        rich_services.append(service)

    return rich_services


def get_service_by_id(service_id: str) -> dict:
    docker_client = utils.get_docker_client()

    images = docker_client.images.list()
    containers = docker_client.containers.list()

    for service in utils.SERVICES:
        if service["id"] == service_id:
            service["running"] = False
            service["downlaoded"] = False
            for container in containers:
                if container.name == service["id"]:
                    service["running"] = True
            for image in images:
                if image.tags[0] == service["dockerImage"]:
                    service["downloaded"] = True
            return service


def get_apps():
    return utils.APPS


def get_docker_stats(container_name: str):
    total, used, _ = shutil.disk_usage("/")
    client = utils.get_docker_client()
    container = client.containers.get(container_name)
    value = container.stats(stream=False)
    cpu_percentage, memory_usage, memory_limit, memory_percentage = utils.format_stats(
        value
    )
    return {
        "cpu_percentage": cpu_percentage,
        "memory_usage": memory_usage,
        "memory_limit": memory_limit,
        "memory_percentage": memory_percentage,
        "storage_percentage": (used / total) * 100,
        "storage_usage": used // (2**30),
        "storage_limit": total // (2**30),
    }
