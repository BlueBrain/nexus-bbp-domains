package ch.epfl.bluebrain.nexus.schema.workbench

import akka.http.scaladsl.model.Uri
import ch.epfl.bluebrain.nexus.commons.shacl.validator.{ShaclSchema, ShaclValidator}
import org.scalatest.WordSpecLike

import scala.util.Try

class SchemaSpec(validator: ShaclValidator[Try],
                 loader: ResourceLoader[Try],
                 base: Uri,
                 schema: Uri,
                 validInstanceUris: List[Uri],
                 invalidInstanceUris: List[Uri])
    extends WordSpecLike
    with ValidationMatchers {

  private implicit val schemaRef: SchemaRef = SchemaRef(base, schema)

  s"The '${schemaRef.stripped}' schema" should {
    val shaclSchema = ShaclSchema(loader(schema).value)

    if (validInstanceUris.nonEmpty) {
      "validate when applied to an instance" when {
        validInstanceUris
          .map(uri => InstanceRef(base, uri))
          .foreach { implicit ref =>
            if (ref.isIgnored) {
              s"using '${ref.stripped}'" ignore {
                val instance = loader(ref.uri).value
                validator(shaclSchema, instance).shouldConform
              }
            } else {
              s"using '${ref.stripped}'" in {
                val instance = loader(ref.uri).value
                validator(shaclSchema, instance).shouldConform
              }
            }
          }
      }
    }

    if (invalidInstanceUris.nonEmpty) {
      "NOT validate when applied to an instance" when {
        invalidInstanceUris
          .map(uri => InstanceRef(base, uri))
          .foreach { implicit ref =>
            if (ref.isIgnored) {
              s"using '${ref.stripped}'" ignore {
                val instance = loader(ref.uri).value
                validator(shaclSchema, instance).shouldNotConform
              }
            } else {
              s"using '${ref.stripped}'" in {
                val instance = loader(ref.uri).value
                validator(shaclSchema, instance).shouldNotConform
              }
            }
          }
      }
    }
  }
}
