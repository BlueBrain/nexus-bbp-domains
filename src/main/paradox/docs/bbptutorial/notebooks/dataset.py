import json

class Dataset(object):
    def __init__(self, identifier,name, _type=None, description=None, context=None):
        super(Dataset, self).__init__()
        self.id= identifier
        self.type = ["Dataset"]
        if _type:
            self.type.append(_type)
        self.name = name
        self.description = description
        self.hasPart = None

        if context:
            self.context = context
        else:
            self.context = "https://bbp.neuroshapes.org"
        self.contribution = None

    def toJSON(self):

        return json.dumps(self.__dict__, cls=ComplexEncoder)

    def jsonable(self):
        a_dict = {(k if k is not "context" else "@context"): v for k, v in self.__dict__.items() }
        a_dict = {(k if k is not "id" else "@id"): v for k, v in a_dict.items() }
        a_dict = {(k if k is not "type" else "@type"): v for k, v in a_dict.items() }
        return sort_json_keys(a_dict)


    def addPart(self,identifier, _type, contentUrl=None, name=None, rev=None):
        if not self.hasPart:
            self.hasPart = []
        final_identifier = "=".join([identifier+"?rev",rev]) if rev is not None else identifier
        entity = {
            "@id":final_identifier,
            "_type":_type
        }

        if contentUrl:
            distribution = {
                "contentUrl": "=".join([contentUrl+"?rev",rev])
            }
            entity["distribution"]=distribution

        if name:
            entity["name"] = name
        self.hasPart.append(entity)


    def addContributor(self, agent, role=None):
        if not self.contribution:
            self.contribution = []

        contribution_object = {
            "agent":agent
        }
        if role:
            contribution_object["role"]=role
        self.contribution.append(contribution_object)

def ComplexHandler(Obj):
    if hasattr(Obj, 'jsonable'):
        return Obj.jsonable()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj)))

def sort_json_keys(json_object):
    sorted_dict=dict()
    for key in sorted(json_object.keys()):
        sorted_dict[key]=json_object[key]
    return sorted_dict