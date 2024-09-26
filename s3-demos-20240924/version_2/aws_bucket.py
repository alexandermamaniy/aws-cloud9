import logging
import boto3
from botocore.exceptions import ClientError
from bucket_exceptions import AWSBucketCreateException 

class AWSBucket:

    def __init__(self, bucket_name, region):
        self._bucket_name = bucket_name
        if region is None:
            region="us-west-2"
            
        self._region = region
        self._s3_resource = boto3.resource('s3')
        self._s3_client = boto3.client('s3', region_name=region)
        
        
    def create_bucket(self):
        try:
            location = {'LocationConstraint': self._region}
            self._s3_client.create_bucket(Bucket=self._bucket_name, CreateBucketConfiguration=location)
        except ClientError as e:
            print(e)
            raise AWSBucketCreateException(e["Error"]["Message"], e["Error"]["Code"])
    
    
    def list_objects(self):
        """List objects a given S3 bucket
        """
        response = self._s3_client.list_objects_v2(Bucket=self.bucket_name)
        if response['KeyCount'] != 0:
            for content in response['Contents']:
                print('\t', content['Key'])


    # retornar una exception
    def upload_file(self, file_name, object_key=None, **extraArgs) -> bool:
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param key: S3 object key. If not specified then file_name is used
        :return: True if file was uploaded, else Exception
        """

        # If S3 key was not specified, use file_name
        if object_key is None:
            object_key = file_name

        # Upload the file
        try:
            response = self._s3_client.upload_file(file_name, self._bucket_name, object_key, extraArgs)
            '''
            # an example of using the ExtraArgs optional parameter to set the ACL (access control list) value 'public-read' to the S3 object
            response = s3_client.upload_file(file_name, bucket, key, 
                ExtraArgs={'ACL': 'public-read'})
            '''
            
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def activate_versioning(self):
        """
        bucket_name (string) – The BucketVersioning’s bucket_name identifier. This must be set.
        """
        bucket_versioning = self._s3_resource.BucketVersioning(self.bucket_name)
        bucket_versioning.enable()

    def desactivate_versioning(self):
        """
        bucket_name (string) – The BucketVersioning’s bucket_name identifier. This must be set.
        """
        bucket_versioning = self._s3_resource.BucketVersioning(self.bucket_name)
        bucket_versioning.suspend()


    def download_file(self, object_key, filename):
        """
        Bucket (str) – The name of the bucket to download from.
        Key (str) – The name of the key to download from.
        Filename (str) – The path to the file to download to.   
        """
    
        # s3.download_file('mybucket', 'hello.txt', '/tmp/hello.txt')
        self._s3_client.download_file(Bucket=self.bucket_name, Key=object_key, Filename=filename)
        


    def delete_bucket(self) -> None:
        s3_resource = boto3.resource('s3')
        bucket_versioning = s3_resource.BucketVersioning(self._bucket_name)
        
        if bucket_versioning.status == "Suspended" or bucket_versioning.status == "Enabled":
            bucket = s3_resource.Bucket(self._bucket_name)
            bucket.object_versions.delete()
        
        s3_client = boto3.client('s3')
    
        # first delete all the objects from a bucket, if any objects exist
        response = s3_client.list_objects_v2(Bucket=self._bucket_name)
        if response['KeyCount'] != 0:
            for content in response['Contents']:
                object_key = content['Key']
                print('\t Deleting object...', object_key)
                s3_client.delete_object(Bucket=self._bucket_name, Key=object_key)
        # delete the bucket
        print('\t Deleting bucket...', self._bucket_name)
        response = s3_client.delete_bucket(Bucket=self._bucket_name)

    
    def delete_object(self, object_key) -> None:
        """Delete a given object from an S3 bucket
        """
        response = self._s3_client.delete_object(Bucket=self._bucket_name, Key=object_key)
        print(response)    

    @staticmethod
    def list_buckets() -> None:
        # Retrieve the list of existing buckets
        s3_client = boto3.client('s3')
        response = s3_client.list_buckets()

        # Output the bucket names
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print('\t', bucket["Name"])

    @property
    def bucket_name(self):
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, new_bucket_name):
        self._bucket_name = new_bucket_name
    
    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, new_region):
        self._region = new_region
    