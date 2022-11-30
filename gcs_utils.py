"""Utils for Cloud Storage and local file manipulation."""

import zipfile
from google.cloud import storage
from google.oauth2 import service_account

class GcsUtils:
    """Utils for Cloud Storage and local file manipulation."""
    def __init__(
        self,
        creds_path: str,
        project_id: str):

        if creds_path and project_id:
            self.creds = service_account.Credentials.from_service_account_file(creds_path)
            self.gcs_client = storage.Client(credentials=self.creds, project=project_id)

    @staticmethod
    def unzip(agent_zip_file_path: str, extract_path: str):
        """Unzip file locally."""
        with zipfile.ZipFile(agent_zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    @staticmethod
    def check_for_gcs_file(file_path: str) -> bool:
        """Validates GCS path vs. local path."""
        is_gcs_file = False

        file_prefix = file_path.split('/')[0]
        if file_prefix == 'gs:':
            is_gcs_file = True

        return is_gcs_file

    def download_gcs(self, gcs_path: str):
        """Downloads the specified GCS file to local machine."""
        path = gcs_path.split('//')[1]
        bucket = path.split('/', 1)[0]
        gcs_object = path.split('/', 1)[1]
        file_name = gcs_object.split('/')[-1]
        bucket = self.gcs_client.bucket(bucket)
        blob = storage.Blob(gcs_object, bucket)
        blob.download_to_filename(file_name)

        return file_name
