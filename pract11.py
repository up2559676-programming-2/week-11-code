class Laptop:
    ram_options = {4: 0, 8: 50, 16: 100, 32: 200}

    ssd_options: dict[int, int] = {256: 0, 512: 30, 1024: 100}

    def __init__(self, brand: str, base_price: float):
        self.brand = brand
        self.base_price = base_price
        self._ram: int = 4
        self._ssd: int = self.ssd_options[0]

    @property
    def ram(self):
        return self._ram

    @ram.setter
    def ram(self, new_ram: int):
        if new_ram in self.ram_options:  # Use class variable
            self._ram = new_ram

    @property
    def ssd(self):
        return self._ssd

    @ssd.setter
    def ssd(self, new_ssd: int):
        if new_ssd in self.ssd_options:
            self._ssd = new_ssd

    def calculate_price(self):
        ram_price = self.ram_options[self.ram]
        total_price = self.base_price + ram_price
        return total_price

    def __str__(self):
        output = f"{self.brand} Laptop with {self.ram} GB RAM and {self.ssd} GB storage"
        output += f" priced at £{self.calculate_price()}"
        return output


class ShoppingCart:
    def __init__(self):
        self.laptops: list[Laptop] = []
        self.total = 0

    def add_laptop(self, laptop: Laptop):
        self.laptops.append(laptop)
        laptop_price = laptop.calculate_price()
        self.total += laptop_price

    def __str__(self):
        output = "Shopping cart contains:\n"
        for laptop in self.laptops:
            output += f"{laptop}\n"
        output += f"Total price is £{self.total}"
        return output


class GamingLaptop(Laptop):
    gpu_options = {
        "NVIDIA GTX 1650": 0,
        "NVIDIA RTX 3070": 250,
        "NVIDIA RTX 4080": 350,
        "AMD RX 6800M": 280,
    }

    def __init__(self, brand: str, base_price: float):
        super().__init__(brand, base_price)
        self._gpu: str = "NVIDIA GTX 1650"

    @property
    def gpu(self):
        return self._gpu

    @gpu.setter
    def gpu(self, new_gpu: str):
        if new_gpu in self.gpu_options:
            self._gpu = new_gpu

    def calculate_price(self):
        gpu_price = self.gpu_options[self.gpu]
        laptop_price = super().calculate_price()
        total_price = laptop_price + gpu_price
        return total_price

    def __str__(self):
        output = f"{self.brand} Laptop with {self.ram} GB RAM "
        output += f"and {self.gpu} priced at £{self.calculate_price()}"
        return output


def test_gaming_laptop():
    gaming_laptop = GamingLaptop("Razer", 2399.99)
    print(f"Gaming laptop's brand is {gaming_laptop.brand}")
    print(f"Gaming laptop's GPU is {gaming_laptop.gpu}")
    print(f"Gaming laptop's RAM is {gaming_laptop.ram} GB")

    gaming_laptop.gpu = "NVIDIA RTX 3070"
    gaming_laptop.ram = 16

    print(f"Gaming laptop's price is £{gaming_laptop.calculate_price()}")

    print(gaming_laptop)


def test_shopping_cart():
    cart = ShoppingCart()
    dell_laptop = Laptop("Dell", 999.99)
    apple_laptop = Laptop("Apple", 1349.00)
    cart.add_laptop(dell_laptop)
    cart.add_laptop(apple_laptop)

    print(f"Shopping cart's total is £{cart.total}")
    print(cart)


def test_laptop():
    laptop = Laptop("Dell", 999.99)
    print(f"Laptop's brand is {laptop.brand}")
    print(f"Laptop's RAM is {laptop.ram} GB")
    print(f"Laptop's price is £{laptop.calculate_price()}")

    laptop.ram = 99  # 'Laptop' has no attribute 'ram'
    print(f"Laptop's RAM is {laptop.ram} GB")

    print(f"Laptop's price is £{laptop.calculate_price()}")  # 999.99

    print(laptop)

    laptop.ssd = 1024
    print(laptop)
