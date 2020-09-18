from uuid import uuid4

class FilterDefaults:
    default_geometry_filter = {  
                "type":"Polygon",
                "coordinates":[  
                    [  
                        [  
                        -120.27282714843749,
                        38.348118547988065
                        ],
                        [  
                        -120.27282714843749,
                        38.74337300148126
                        ],
                        [  
                        -119.761962890625,
                        38.74337300148126
                        ],
                        [  
                        -119.761962890625,
                        38.348118547988065
                        ],
                        [  
                        -120.27282714843749,
                        38.348118547988065
                        ]
                    ]
                ]
            }
class Strings:
    @staticmethod
    def random(l=16):
        out = ""
        while len(out) < l:
            out += str(uuid4())
        return out[:l-1]
        