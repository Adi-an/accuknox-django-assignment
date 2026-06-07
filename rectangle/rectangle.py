class Rectangle:
    """
    A simple Rectangle class that supports iteration.
    Iterating over an instance yields length first, then width —
    each as a dictionary with a descriptive key.
    """

    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        # Yield length first, then width — as required
        yield {'length': self.length}
        yield {'width': self.width}

    def __repr__(self):
        return f"Rectangle(length={self.length}, width={self.width})"


# ── Quick demo (run this file directly to see it work) ──
if __name__ == "__main__":
    r = Rectangle(10, 5)
    print(f"Created: {r}")
    print("Iterating:")
    for item in r:
        print(f"  {item}")
