"""
    File containing mock values for tests that use mocks since these values are
    too large to include in the actual tests.
"""
MOCK_FILE_NAME = "en_ulb_b06_jos_c01_v01-03_t02.wav"
MOCK_FILE_LOCATION = "media/dump/1540049.2991178e/en_ulb_b06_jos_c01_v01-03_t02.wav"
MOCKFILECONTENTS = [
    {
        {
            "language" :
            {
                "slug" : "en",
                "name" : "English"
            },
            "book" :
            {
                "slug"   : "jos",
                "name"   : "Joshua",
                "number" : 6
            },
            "version" :
            {
                "slug" : "ot",
                "name" : "old testament"
            },
            "mode" :
            {
                "slug" : "chunk",
                "name" : "chunk",
                "type" : "MULTI"
            },
            "users" : [],
            "manifest" :
            [
                {
                    "chapter"       : 1,
                    "cheking_level" : 0,
                    "published"     : false,
                    "chunks"        :
                    [
                        { "startv"   : 1,
                            "endv"     : 3,
                            "comments" : [],
                            "takes"    :
                            [
                                {
                                    "name"     : MOCK_FILE_NAME,
                                    "location" : MOCK_FILE_LOCATION,
                                    "rating"   : 3,
                                    "published": false,
                                    "user_id"  : null,
                                    "comments" : []
                                }
                            ]
                        }
                    ],
                    "comments"        : []
                }
            ]
        }
    }
]
