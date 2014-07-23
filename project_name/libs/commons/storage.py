from django.contrib.staticfiles.storage import StaticFilesStorage


class OverwriteStaticFilesStorage(StaticFilesStorage):
    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            self.delete(name)
        return name
