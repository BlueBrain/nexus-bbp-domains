nexus views query-sparql --data \
'
PREFIX vocab: <https://sandbox.bluebrainnexus.io/v1/vocabs/demo/$PROJECTLABEL/>
PREFIX nxv: <https://bluebrain.github.io/nexus/vocabulary/>
Select ?org ?name ?createdAt
 WHERE  {

    ?org a vocab:Organization.
    ?org vocab:name  ?name.
    ?org nxv:createdAt ?createdAt
}
ORDER BY DESC (?createdAt)
LIMIT 5'