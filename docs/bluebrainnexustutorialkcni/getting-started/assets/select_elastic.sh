nexus views query-es --data \
'{
     "size":5,
     "sort" : [
       {
        "_createdAt" : {"order" : "desc"}
       }
     ],
     "query": {
     	"terms" : {"@type":["https://sandbox.bluebrainnexus.io/v1/vocabs/tutorialnexus/$PROJECTLABEL/Organization"]}
     }
 }'
