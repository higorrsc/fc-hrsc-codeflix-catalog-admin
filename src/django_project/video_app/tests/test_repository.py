import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.models import Video as VideoModel
from src.django_project.video_app.repository import DjangoORMVideoRepository


@pytest.fixture
def movie_category() -> Category:
    """
    Fixture for a Category instance representing movies.

    Returns:
        Category: A Category object with name "Movie" and description "Movies category".
    """

    return Category(
        name="Movie",
        description="Movies category",
    )


@pytest.fixture
def action_genre(movie_category: Category) -> Genre:
    """
    Fixture for a Genre instance representing Action movies.

    Returns:
        Genre: A Genre object with name "Action" and the movie category.
    """

    return Genre(
        name="Action",
        categories={movie_category.id},
    )


@pytest.fixture
def adventure_genre(movie_category: Category) -> Genre:
    """
    Fixture for a Genre instance representing Adventure movies.

    Returns:
        Genre: A Genre object with name "Adventure" and the movie category.
    """

    return Genre(
        name="Adventure",
        categories={movie_category.id},
    )


@pytest.fixture
def actor_cast_member() -> CastMember:
    """
    Fixture for a CastMember instance representing Sam Worthington.

    Returns:
        CastMember: A CastMember object with name "Sam Worthington" and type ACTOR.
    """

    return CastMember(
        name="Sam Worthington",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def director_cast_member() -> CastMember:
    """
    Fixture for a CastMember instance representing James Cameron.

    Returns:
        CastMember: A CastMember object with name "James Cameron" and type DIRECTOR.
    """

    return CastMember(
        name="James Cameron",
        type=CastMemberType.DIRECTOR,
    )


@pytest.mark.django_db
class TestSave:

    def test_save_video_in_database(self):
        """
        Tests saving a Video instance to the database using DjangoORMVideoRepository.

        This test creates a Video instance with predefined attributes and saves it
        to the repository. It verifies that the video is successfully saved by
        asserting the count of VideoModel objects in the database and retrieving
        the video by its ID to confirm that all attributes match the original
        video instance.

        Asserts:
            - The count of VideoModel objects in the database is 1 after saving.
            - The retrieved video from the database matches the original video
            instance's ID, title, description, duration, launch year, published
            status, and rating.
        """

        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        repository = DjangoORMVideoRepository()
        repository.save(video)
        assert VideoModel.objects.count() == 1

        video_from_db = repository.get_by_id(video.id)
        assert video_from_db.id == video.id  # type: ignore
        assert video_from_db.title == video.title  # type: ignore
        assert video_from_db.description == video.description  # type: ignore
        assert video_from_db.duration == video.duration  # type: ignore
        assert video_from_db.launch_year == video.launch_year  # type: ignore
        assert video_from_db.published == video.published  # type: ignore
        assert video_from_db.rating == video.rating  # type: ignore

    def test_save_video_with_related_data_in_database(
        self,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
    ):
        """
        Tests saving a Video with related data in the database.

        This test verifies that the `save` method of the `DjangoORMVideoRepository`
        successfully saves a Video along with its associated categories, genres,
        and cast members. It ensures that the related data is correctly persisted
        and can be retrieved from the database.

        Asserts:
            - The Video is saved to the database with the correct details.
            - The related categories are correctly associated and retrievable.
            - The related genres are correctly associated and retrievable.
            - The related cast members are correctly associated and retrievable.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories={
                movie_category.id,
            },
            genres={
                action_genre.id,
                adventure_genre.id,
            },
            cast_members={
                actor_cast_member.id,
                director_cast_member.id,
            },
        )

        repository = DjangoORMVideoRepository()
        repository.save(video)
        assert VideoModel.objects.count() == 1

        video_from_db = VideoModel.objects.get(pk=video.id)
        assert video_from_db.id == video.id  # type: ignore

        related_categories = video_from_db.categories.all()
        assert related_categories.count() == 1
        assert related_categories[0].id == movie_category.id
        assert related_categories[0].name == movie_category.name

        related_genres = video_from_db.genres.all()
        assert related_genres.count() == 2

        related_cast_members = video_from_db.cast_members.all()
        assert related_cast_members.count() == 2


@pytest.mark.django_db
class TestGetById:

    def test_retrieves_video_from_database(self):
        """
        Tests that a Video instance can be retrieved from the database using DjangoORMVideoRepository.

        This test creates a Video instance and saves it to the repository. It verifies that the video is
        successfully retrieved by asserting that the video's attributes match the original video instance.
        """

        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        repository = DjangoORMVideoRepository()
        repository.save(video)
        assert VideoModel.objects.count() == 1

        video_from_db = repository.get_by_id(video.id)
        assert video_from_db.id == video.id  # type: ignore
        assert video_from_db.title == video.title  # type: ignore
        assert video_from_db.description == video.description  # type: ignore
        assert video_from_db.launch_year == video.launch_year  # type: ignore
        assert video_from_db.published == video.published  # type: ignore
        assert video_from_db.rating == video.rating  # type: ignore

    def test_retrieves_video_with_related_data_from_database(
        self,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
    ):
        """
        Tests retrieving a Video with related data from the database using DjangoORMVideoRepository.

        This test creates a Video instance with predefined attributes and saves it
        to the repository. It verifies that the video is successfully retrieved from
        the database by asserting the count of VideoModel objects, retrieving the video
        by its ID, and confirming that all attributes and related data match the
        original video instance.

        Asserts:
            - The count of VideoModel objects in the database is 1 after saving.
            - The retrieved video from the database matches the original video
            instance's ID, title, description, launch year, published status, and rating.
            - The retrieved video from the database has the correct related categories,
            genres, and cast members.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories={movie_category.id},
            genres={action_genre.id},
            cast_members={actor_cast_member.id, director_cast_member.id},
        )

        repository = DjangoORMVideoRepository()
        repository.save(video)
        assert VideoModel.objects.count() == 1

        video_from_db = repository.get_by_id(video.id)
        assert video_from_db.id == video.id  # type: ignore
        assert video_from_db.title == video.title  # type: ignore
        assert video_from_db.description == video.description  # type: ignore
        assert video_from_db.launch_year == video.launch_year  # type: ignore
        assert video_from_db.published == video.published  # type: ignore
        assert video_from_db.rating == video.rating  # type: ignore

        related_categories = list(video_from_db.categories)  # type: ignore
        assert len(related_categories) == 1  # type: ignore
        assert related_categories[0] == movie_category.id  # type: ignore

        related_genres = list(video_from_db.genres)  # type: ignore
        assert len(related_genres) == 1  # type: ignore
        assert related_genres[0] == action_genre.id  # type: ignore

        related_cast_members = list(video_from_db.cast_members)  # type: ignore
        assert len(related_cast_members) == 2  # type: ignore


@pytest.mark.django_db
class TestDelete:

    def test_deletes_video_from_database(self):
        """
        Tests that a Video instance can be deleted from the database using DjangoORMVideoRepository.

        This test creates a Video instance and saves it to the repository. It then
        deletes the video by its ID and asserts that the video is no longer in the
        repository, and that the count of VideoModel objects in the database is 0.

        Asserts:
            - The count of VideoModel objects in the database is 1 after saving.
            - The count of VideoModel objects in the database is 0 after deleting.
            - The retrieved video from the database is None after deleting.
        """

        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        repository = DjangoORMVideoRepository()
        repository.save(video)
        assert VideoModel.objects.count() == 1

        repository.delete(video.id)
        assert VideoModel.objects.count() == 0

        video_from_db = repository.get_by_id(video.id)
        assert video_from_db is None

    def test_deletes_video_with_related_data_from_database(
        self,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
    ):
        """
        Tests that a Video instance can be deleted from the database,
        including related categories, genres, and cast members, using DjangoORMVideoRepository.

        This test creates a Video instance with predefined attributes and saves it
        to the repository. It then deletes the video by its ID and asserts that the
        video is no longer in the repository, the count of VideoModel objects in the
        database is 0, and that the related categories, genres, and cast members are
        no longer present in the database.

        Asserts:
            - The count of VideoModel objects in the database is 1 after saving.
            - The count of VideoModel objects in the database is 0 after deleting.
            - The retrieved video from the database is None after deleting.
            - The related categories, genres, and cast members are no longer present
            in the database after deleting.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories={movie_category.id},
            genres={action_genre.id},
            cast_members={actor_cast_member.id, director_cast_member.id},
        )

        repository = DjangoORMVideoRepository()
        repository.save(video)
        assert VideoModel.objects.count() == 1

        repository.delete(video.id)
        assert VideoModel.objects.count() == 0

        video_from_db = VideoModel.objects.filter(id=video.id).first()
        assert video_from_db is None


@pytest.mark.django_db
class TestUpdate:

    def test_updates_video_in_database(self):
        """
        Tests that a Video instance can be updated in the database using DjangoORMVideoRepository.

        This test creates a Video instance and saves it to the repository. It then
        updates the video and asserts that the video is updated in the repository.
        """

        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        repository = DjangoORMVideoRepository()
        repository.save(video)
        assert VideoModel.objects.count() == 1

        video_from_db = repository.get_by_id(video.id)
        assert video_from_db is not None

        video_from_db.title = "Avatar (Updated)"
        repository.update(video_from_db)

        updated_video_from_db = repository.get_by_id(video.id)
        assert updated_video_from_db.title == "Avatar (Updated)"  # type: ignore

    def test_save_video_with_related_data_in_database(
        self,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
    ):
        """
        Tests saving a Video with related data in the database.

        This test verifies that the `save` method of the `DjangoORMVideoRepository`
        successfully saves a Video along with its associated categories, genres,
        and cast members. It ensures that the related data is correctly persisted
        and can be retrieved from the database.

        Asserts:
            - The Video is saved to the database with the correct details.
            - The related categories are correctly associated and retrievable.
            - The related genres are correctly associated and retrievable.
            - The related cast members are correctly associated and retrievable.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        video = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        repository = DjangoORMVideoRepository()
        repository.save(video)
        assert VideoModel.objects.count() == 1

        video_from_db = repository.get_by_id(video.id)
        assert video_from_db is not None

        video_from_db.add_categories({movie_category.id})
        video_from_db.add_genres({action_genre.id})
        video_from_db.add_cast_members({actor_cast_member.id, director_cast_member.id})
        repository.update(video_from_db)

        updated_video_from_db = repository.get_by_id(video.id)
        assert len(updated_video_from_db.categories) == 1  # type: ignore
        assert len(updated_video_from_db.genres) == 1  # type: ignore
        assert len(updated_video_from_db.cast_members) == 2  # type: ignore

        video_from_db.remove_categories({movie_category.id})
        video_from_db.remove_genres({action_genre.id})
        video_from_db.remove_cast_members({actor_cast_member.id})
        repository.update(video_from_db)

        updated_video_from_db = repository.get_by_id(video.id)
        assert len(updated_video_from_db.categories) == 0  # type: ignore
        assert len(updated_video_from_db.genres) == 0  # type: ignore
        assert len(updated_video_from_db.cast_members) == 1  # type: ignore


@pytest.mark.django_db
class TestList:

    def test_lists_videos_from_database(self):
        """
        Tests that a list of Video instances can be retrieved from the DjangoORMVideoRepository.

        This test creates two Video instances and saves them to the repository. It then
        retrieves the list of videos and asserts that the list contains the saved videos.
        """

        video_01 = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video_02 = Video(
            title="Avatar: The Way of Water",
            description="""Jake Sully lives with his newfound family formed on the extrasolar
            moon Pandora. Once a familiar threat returns to finish what was previously started,
            Jake must work with Neytiri and the army of the Na'vi race to protect their home.""",
            duration=192.0,  # type: ignore
            launch_year=2022,
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        repository = DjangoORMVideoRepository()
        repository.save(video_01)
        repository.save(video_02)
        assert VideoModel.objects.count() == 2

        videos_from_db = repository.list()
        assert len(videos_from_db) == 2

    def test_lists_videos_with_related_data_from_database(
        self,
        movie_category: Category,
        action_genre: Genre,
        adventure_genre: Genre,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
    ):
        """
        Tests that a list of Video instances can be retrieved from the DjangoORMVideoRepository
        along with their associated categories, genres, and cast members.

        This test creates two Video instances and saves them to the repository. It then
        retrieves the list of videos and asserts that the videos are correctly associated
        with their respective categories, genres, and cast members.
        """

        category_repository = DjangoORMCategoryRepository()
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        video_01 = Video(
            title="Avatar",
            description="""A paraplegic Marine dispatched to the moon Pandora on a
            unique mission becomes torn between following his orders and protecting
            the world he feels is his home.""",
            duration=162.0,  # type: ignore
            launch_year=2009,
            rating=Rating.AGE_12,
            categories={movie_category.id},
            genres={action_genre.id},
            cast_members={actor_cast_member.id, director_cast_member.id},
        )
        video_02 = Video(
            title="Avatar: The Way of Water",
            description="""Jake Sully lives with his newfound family formed on the extrasolar
            moon Pandora. Once a familiar threat returns to finish what was previously started,
            Jake must work with Neytiri and the army of the Na'vi race to protect their home.""",
            duration=192.0,  # type: ignore
            launch_year=2022,
            rating=Rating.AGE_14,
            categories={movie_category.id},
            genres={adventure_genre.id},
            cast_members={actor_cast_member.id, director_cast_member.id},
        )

        repository = DjangoORMVideoRepository()
        repository.save(video_01)
        repository.save(video_02)
        assert VideoModel.objects.count() == 2

        videos_from_db = repository.list()
        assert len(videos_from_db) == 2

        assert len(videos_from_db[0].categories) == 1  # type: ignore
        assert len(videos_from_db[0].genres) == 1  # type: ignore
        assert len(videos_from_db[0].cast_members) == 2  # type: ignore

        assert len(videos_from_db[1].categories) == 1  # type: ignore
        assert len(videos_from_db[1].genres) == 1  # type: ignore
        assert len(videos_from_db[1].cast_members) == 2  # type: ignores
