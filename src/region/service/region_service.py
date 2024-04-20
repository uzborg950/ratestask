import src.region.repository.region_repository as repo


def get_by_slug(slug: str):
    return repo.get_by_slug(slug)

