import os

from django.test import TestCase

from .common import ImageSteganography
from .common import ImageSteganographyException as ISE


class ImageSteganographyTest(TestCase):
    def setUp(self):
        self.obj = ImageSteganography(
            BASE_PATH="testImages", SAVE_IMAGE_DIR="testImagesOutput"
        )

    def test_encode_text_in_image_success(self):
        message_to_hide = "This message is hidden by automated  tests"
        input_image_name = "testImage.jpg"
        output_image_name = "enc-testImage.jpg"

        encrypted_image_path = self.obj.encode_text_into_image(
            message_to_hide=message_to_hide,
            input_image_name=os.path.join(self.obj.BASE_PATH, input_image_name),
            output_image_name=output_image_name,
        )

        self.assertEqual(
            os.path.join(self.obj.SAVE_IMAGE_DIR, output_image_name),
            encrypted_image_path,
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.obj.FULL_PATH, output_image_name))
        )

    def test_encode_text_in_invalid_image(self):
        with self.assertRaises(ISE) as ise:
            message_to_hide = "This message is hidden by automated  tests"
            input_image_name = "testTextFile.txt"
            output_image_name = "enc-testImage.jpg"

            encrypted_image_path = self.obj.encode_text_into_image(
                message_to_hide=message_to_hide,
                input_image_name=os.path.join(self.obj.BASE_PATH, input_image_name),
                output_image_name=output_image_name,
            )

        self.assertRaisesMessage(
            ise, "Not an Image File! Please only select image file."
        )

    def test_decode_text_from_image_success(self):
        image_name = "enc-testImage.jpg"

        decrypted_message = self.obj.decode_text_from_image(
            image_name=os.path.join(self.obj.FULL_PATH, image_name),
        )

        self.assertEqual(
            "This message is hidden by automated  tests", decrypted_message
        )

    def test_decode_text_from_wrong_image(self):
        with self.assertRaises(ISE) as ise:
            image_name = "testImage.jpg"

            decrypted_message = self.obj.decode_text_from_image(
                image_name=os.path.join(self.obj.FULL_PATH, image_name),
            )

        self.assertRaisesMessage(ise, "Something Happened! Can't find hidden message.")

    def test_decode_text_from_invalid_image(self):
        with self.assertRaises(ISE) as ise:
            image_name = "enc-testTextFile.txt"

            decrypted_message = self.obj.decode_text_from_image(
                image_name=os.path.join(self.obj.FULL_PATH, image_name),
            )

        self.assertRaisesMessage(
            ise, "Not an Image File! Please only select image file."
        )


# class RSATest(TestCase):
#     def setUp(self):
#         self.obj = RSA()

#     def test_encrypting_text(self):
#         encrypted_text = self.obj.encrypt_text(
#             "This is sample text", self.obj.public_key
#         )
#         self.assertEqual(encrypted_text, "ldskjfustfulfgdgfkjhfkgfkgfyawrtwtr6wtrg sfg")

#     def test_decrypting_text(self):
#         decrypted_text = self.obj.decrypt_text(
#             "flkjfasfgksuagfkfgfkjshfgkgf", self.obj.private_key
#         )
