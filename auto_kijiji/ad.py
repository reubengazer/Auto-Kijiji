# Class for an advertisement on Kijiji, to hold all ad parameters


class Ad:

    def __init__(self, title: str, price: float, description: str, tags: list, image_fps: list, category_id: str):
        self.category_id = category_id  # the number representing the posting category.
                                        # this can be found by clicking through to it once
                                        # and observing the categoryId={} in browser
        self.title = title  # title of ad
        self.price = price  # price of ad
        self.description = description  # text description of the ad
        self.tags = tags  # tags to turn up in more searches (keywords)
        self.image_fps = image_fps  # a list of the filepaths to images for the ad