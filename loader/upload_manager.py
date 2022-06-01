import os, random, logging
from .exceptions import OutOfFreeNamesError, PictureFormatNotSupportedError, PictureNotUploadedError

logger = logging.getLogger("basic")


class UploadManager:

    def is_file_type_valid(self, file_type):
        if file_type.lower() in ["jpeg", "jpg", "gif", "png", "webp", "tiff"]:
            return True
        return False, logger.info("Загруженный файл не картинка")


    def get_free_filename(self, folder, file_type):
        """получаем случайное имя файла"""

        attemps = 0
        range_of_image_numbers = 100
        limit_of_attemps = 1000

        pic_name = str(random.randint(0, range_of_image_numbers))
        filename_save = f"{pic_name}.{file_type}"
        os_path = os.path.join(folder, filename_save)
        is_filename_occupied = os.path.exists(os_path)

        if not is_filename_occupied:
            return filename_save
        attemps += 1

        if attemps > limit_of_attemps:
            raise OutOfFreeNamesError("No free names for image!")


    def save_with_random_name(self, picture):
        filename = picture.filename
        file_type = filename.split(".")[-1]

        # Проверяем валидность картинки
        if not self.is_file_type_valid(file_type):
            raise PictureFormatNotSupportedError(f"Формат {file_type} не поддерживается")


        # Получаем случайное имя для картинки
        folder = os.path.join(".", "uploads", "images")
        filename_save = self.get_free_filename(folder, file_type)

        # Сохраняем картинку под новым именем
        try:
            picture.save(os.path.join(folder, filename_save))
        except FileNotFoundError:
            raise PictureNotUploadedError(f"{folder}, {filename_save}")

        return filename_save
