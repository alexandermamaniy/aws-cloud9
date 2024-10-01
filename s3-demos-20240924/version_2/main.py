from aws_bucket import AWSBucket 


def main():
   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument('bucket_name', help='The name of the bucket.')
   parser.add_argument('--file_name', help='The name of the file to upload.')
   parser.add_argument('--object_key', help='The object key')
   parser.add_argument('--path_download_file', help='Path where the downloaded file will be saved')
   parser.add_argument('--region', help='Region where the bucket will be created')
   args = parser.parse_args()
   

   aws_bucket_object = AWSBucket(args.bucket_name, args.region)
   
   # AWSBucket'
   # create bucket
   # aws_bucket_object.create_bucket()
   

   # list_buckets
   # AWSBucket.list_buckets()


   
   # upload_file
   # aws_bucket_object.upload_file(args.file_name, args.object_key)
   
   # AWSBucket's object methods
   # list_objects
   # aws_bucket_object.list_objects()
   
   # download_file
   # aws_bucket_object.download_file(args.object_key, args.path_download_file)
    
   # activate_versioning
   # aws_bucket_object.activate_versioning()

   # desactivate_versioning
   # aws_bucket_object.desactivate_versioning()

   # delete_object
   # aws_bucket_object.delete_object(args.object_key)
   
   # Delete bucket
   aws_bucket_object.delete_bucket()
   

if __name__ == '__main__':
   main()