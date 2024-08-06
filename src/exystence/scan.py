from constants import URL, console

from .scrape import Album, get_albums_data, get_last_album


def get_albums_list(
    user_categories: list[str] = None, max_entries: int = 20
) -> list[Album] | bool:
    """This functions agregate whole functions in this file returning the
    final list requested by user to be added in his spotify library.

        If there is a pickle file with the last album, this functions will search
    for new albums until to complete the max_entries.

        If there is no a last album, it will search for the last new albums to
    complete the max_entries.

    Args:
        user_categories (list[str]): List of genres/tags defined by user.
        max_entries (int, optional): Max albums to be collected. Defaults to 20.

    Returns:
        list[Album] | bool: List of albums to be add in user's spotify library.
    """

    if last_album := get_last_album():
        console.print(
            f'\nYour last 💿 saved was [bold]"{last_album.title}[/]". '
            f'We will try the {max_entries} first albums since it.\n'
        )
    else:
        console.print(
            "\nWe didn't find the last 💿 saved. Collecting new ones until page 20.\n"
        )

    page = 1
    new_entries = list()

    with console.status('[bold green]Working on pages...') as _:
        while page <= 20:
            console.print(f'Colleting new albums from the page {page}...')

            albums = get_albums_data(f'{URL}/{page}')
            filtered_albums = filter_categories(albums, user_categories)

            new_entries.extend(filtered_albums)

            if last_album in new_entries:
                pos_last_album = new_entries.index(last_album)
                new_entries = new_entries[:pos_last_album]
                break

            if len(new_entries) >= max_entries:
                new_entries = new_entries[:max_entries]
                break

            page += 1

    if new_entries:
        console.print(f'\n🚨 {len(new_entries)} new albums collected!')
        return new_entries

    console.print('\n:🔴 There is no albums to be collected.')
    return False


def filter_categories(
    albums: list[Album], user_categories: list[str]
) -> list[Album]:
    """Return a list filtered by tags/categories defined by user.

    Args:
        albums (dataclass): An album dataclass.
        user_categories (list[str]): List of tags defined by user.

    Returns:
        list[str]: List of album's titles.
    """

    if user_categories:
        return [
            album
            for album in albums
            if bool(set(album.categories) & set(user_categories))
        ]

    return albums
