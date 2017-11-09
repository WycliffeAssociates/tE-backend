from rest_framework import views
from rest_framework.parsers import JSONParser

from .zip_file_processor import zip_it


class ZipProjectFiles(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data
        zip_it(data)

        # code flow
        """
        //dealing with data received
        1.Check project is in the data
        2.If project is not in data check language,version,book is not in data,then return not enough parameter
        3.Create an empty dictionary
        4.Check if project is in data
        5.if project is in data assign it to dictionary created,else
        6.check if language,book,version is in data
        7.If language,book,version is in data assign them to the created dictionary

        //dealing with database
        8.Fetch project(which is array of chunks with array of takes),database query
        9.Check if project exist

        //dealing with file system
        10.If porject exists,construct project_path
        11.Create directory for project(project_path) if it doesn't exist
        12.Loop through Chunks and create chapter_path
        13.Loop through takes in chunk
        14.Create array of takes location(source and destination)
        15.Copy takes to destination from source location

        //data manupulation and informing
        16.Converts moved .wav file to .mp3
        17.Zip the files and send response with location of files,else
        18.Send Response with status 400
        """
