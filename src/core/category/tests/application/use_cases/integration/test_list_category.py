from src.config import DEFAULT_PAGE_SIZE
from src.core._shared.application.use_cases.list import (
    ListRequest,
    ListResponse,
    ListResponseMeta,
)
from src.core.category.application.use_cases.list_category import ListCategory
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestListCategory:
    """
    Suite of tests for the `list_category` use case.
    """

    def test_return_empty_list(self):
        """
        Test that the `list_category` use case returns an empty list when no categories
        exist in the repository.

        This test verifies that the `list_category` use case successfully returns an
        empty `ListCategoryResponse` when the repository contains no categories.
        """

        repository = InMemoryCategoryRepository(categories=[])
        use_case = ListCategory(repository)
        request = ListRequest()

        response = use_case.execute(request)

        response: ListResponse = use_case.execute(request)

        assert response == {
            "data": [],
            "meta": ListResponseMeta(
                current_page=1,
                per_page=DEFAULT_PAGE_SIZE,
                total=0,
            ),
        }

    def test_return_existing_categories(self):
        """
        Test that the `list_category` use case returns a list of categories when categories
        exist in the repository.

        This test verifies that the `list_category` use case successfully returns a
        `ListCategoryResponse` containing a list of categories when the repository contains
        categories.
        """

        category_action = Category(
            name="Action",
            description="Action movies",
        )
        category_adventure = Category(
            name="Adventure",
            description="Adventure movies",
        )

        repository = InMemoryCategoryRepository()
        repository.save(category_action)
        repository.save(category_adventure)

        use_case = ListCategory(repository)
        request = ListRequest(order_by="name")

        response: ListResponse = use_case.execute(request)

        assert response == {
            "data": [
                category_action,
                category_adventure,
            ],
            "meta": ListResponseMeta(
                current_page=1,
                per_page=DEFAULT_PAGE_SIZE,
                total=2,
            ),
        }
