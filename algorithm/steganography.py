import os
import uuid
from typing import Optional

import numpy as np
from PIL import Image, UnidentifiedImageError


class ImageSteganographyException(Exception):
    pass


class ImageSteganography:
    """
    Class that implements actual logic to hide and reveal text in image itself
    """
    def __init__(
        self,
        STOP_INDICATOR="<<END_ENCRYPTED_MESSAGE>>",
        BASE_PATH="uploads",
        SAVE_IMAGE_DIR="encrypted",
    ):
        self.STOP_INDICATOR = STOP_INDICATOR
        self.SAVE_IMAGE_DIR = SAVE_IMAGE_DIR
        self.BASE_PATH = BASE_PATH
        self.FULL_PATH = os.path.join(self.BASE_PATH, self.SAVE_IMAGE_DIR)

        if not os.path.exists(self.FULL_PATH):
            os.mkdir(self.FULL_PATH)

    def encode_text_into_image(
        self,
        message_to_hide: str,
        input_image_name: str,
        output_image_name: Optional[str] = f"{uuid.uuid4()}.png",
    ) -> str:
        """
        Method that encodes text in an image
        """
        try:
            image = Image.open(input_image_name, "r")
        except UnidentifiedImageError as e:
            raise ImageSteganographyException(
                "Not an Image File! Please only select image file."
            )

        width, height = image.size

        img_arr = np.array(list(image.getdata()))

        if image.mode == "p":
            raise ImageSteganographyException(
                "Image Not Supported! Please try with another image."
            )

        channels = 4 if image.mode == "RGBA" else 3

        pixels = img_arr.size // channels

        message_to_hide = str(message_to_hide) + self.STOP_INDICATOR

        message_bits = "".join(f"{ord(c):08b}" for c in message_to_hide)
        total_bits = len(message_bits)

        if total_bits > pixels:
            raise ImageSteganographyException(
                "Not Enough Space! Image size must be larger than text size."
            )
        else:
            index = 0
            for i in range(pixels):
                for j in range(3):
                    if index < total_bits:
                        img_arr[i][j] = int(
                            bin(img_arr[i][j])[2:-1] + message_bits[index], 2
                        )
                        index += 1

        img_arr = img_arr.reshape((height, width, channels))
        result = Image.fromarray(img_arr.astype("uint8"), image.mode)
        result.save(os.path.join(self.FULL_PATH, output_image_name))
        return os.path.join(self.SAVE_IMAGE_DIR, output_image_name)

    def decode_text_from_image(self, image_name: str) -> str:
        """
        Method that dencodes text from an image
        """
        try:
            image = Image.open(image_name, "r")
        except UnidentifiedImageError as e:
            raise ImageSteganographyException(
                "Not an Image File! Please only select image file."
            )

        img_arr = np.array(list(image.getdata()))

        if image.mode == "p":
            raise ImageSteganographyException(
                "Image Not Supported! Please try with another image."
            )

        channels = 4 if image.mode == "RGBA" else 3

        pixels = img_arr.size // channels

        secret_bits_list = [
            bin(img_arr[i][j])[-1] for i in range(pixels) for j in range(3)
        ]
        secret_bits = "".join(secret_bits_list)

        secret_bytes = [secret_bits[i : i + 8] for i in range(0, len(secret_bits), 8)]

        secret_message_list = [
            chr(int(secret_bytes[i], 2)) for i in range(len(secret_bytes))
        ]
        secret_message = "".join(secret_message_list)

        if self.STOP_INDICATOR in secret_message:
            return secret_message[: secret_message.index(self.STOP_INDICATOR)]

        raise ImageSteganographyException(
            "Something Happened! Cannot find hidden message."
        )
