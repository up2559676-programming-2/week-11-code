from dataclasses import dataclass


@dataclass()
class Artist:
    name: str


class ArtPiece:
    def __init__(self, title: str, artist: str, price: float) -> None:
        self.title = title
        self.artist = Artist(artist)
        self._initial_price = int(price * 100)
        self._current_price = self._initial_price

    def __post_init__(self):
        self._current_price = self._initial_price

    @property
    def price(self) -> float:
        return self._current_price / 100

    @price.setter
    def price(self, value: float):
        if value <= self._initial_price:
            return

        self._current_price = int(value * 100)


class Exhibition:
    def __init__(self, name: str) -> None:
        self.name = name
        self.art_pieces: list[ArtPiece] = []

    def __str__(self) -> str:
        return f"Name: {self.name} | Art: {self.art_pieces}"

    def total_value(self) -> float:
        return sum(art.price for art in self.art_pieces)

    def add_art(self, art: ArtPiece):
        self.art_pieces

    def remove_art(self, art: ArtPiece):
        self.art_pieces.remove(art)

    def remove_art_by_title(self, title: str):
        self.art_pieces = [art for art in self.art_pieces if art.title != title]


class Gallery:
    def __init__(self, name: str) -> None:
        self.name = name
        self.exhibitions = []

    def host_exhibition(self, exhibition: Exhibition) -> None:
        self.exhibitions.append(exhibition)


def test():
    # Create gallery
    gallery = Gallery("Modern Art Gallery")

    # Create art pieces
    p1 = ArtPiece("Sunrise", "Alice", 1000.0)
    p2 = ArtPiece("Abstract Thoughts", "Bob", 1500.0)
    p3 = ArtPiece("Ocean Blue", "Alice", 2000.0)

    # Create exhibitions
    ex1 = Exhibition(
        "Spring Exhibition",
    )
    ex2 = Exhibition(
        "Summer Exhibition",
    )

    # Add art pieces to exhibitions
    ex1.add_art(p1)
    ex1.add_art(p2)

    ex2.add_art(p2)
    ex2.add_art(p3)

    # Verify total values
    assert ex1.total_value() == 2500.0
    assert ex2.total_value() == 3500.0

    # Remove and recheck
    ex1.remove_art(p2)
    assert ex1.total_value() == 1000.0

    # Update prices (increase only)
    p1.price = 1200.0
    p3.price = 2500.0

    # Verify updated totals
    assert ex1.total_value() == 1200.0
    assert ex2.total_value() == 4000.0

    # Host exhibitions in gallery
    gallery.host_exhibition(ex1)
    gallery.host_exhibition(ex2)

    # View details via __str__
    ex1_str = str(ex1)
    ex2_str = str(ex2)
    gallery_str = str(gallery)

    # Basic sanity checks on string output
    assert "Spring Exhibition" in ex1_str
    assert "Summer Exhibition" in ex2_str
    assert "Modern Art Gallery" in gallery_str
    assert "Sunrise" in ex1_str
    assert "Ocean Blue" in ex2_str
