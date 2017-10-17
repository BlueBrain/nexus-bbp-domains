package ch.epfl.bluebrain.nexus.schema.nexus

import akka.http.scaladsl.model.Uri
import akka.http.scaladsl.model.Uri.Path
import cats.instances.try_._
import ch.epfl.bluebrain.nexus.commons.shacl.validator.ShaclValidator
import ch.epfl.bluebrain.nexus.bbp.domains.core.BuildInfo
import ch.epfl.bluebrain.nexus.schema.workbench.{ClasspathResolver, ResourceLoader, SchemaSpec}
import org.scalatest.Suites

import scala.util.Try

class NexusSpec extends Suites {

  private val loader    = new ResourceLoader[Try](Uri(BuildInfo.base), Map("{{base}}" -> BuildInfo.base))
  private val resolver  = new ClasspathResolver[Try](loader)
  private val validator = ShaclValidator(resolver)

  private val schemas = BuildInfo.schemas.foldLeft(Vector.empty[Uri]) {
    case (acc, e) => acc :+ Uri(s"""${BuildInfo.base}${e.substring(0, e.lastIndexOf(".json"))}""")
  }

  private val valid = BuildInfo.data.foldLeft(List.empty[Uri]) {
    case (acc, e) => s"""${BuildInfo.base}${e.substring(0, e.lastIndexOf(".json"))}""" :: acc
  }

  private val invalid = BuildInfo.invalid.foldLeft(List.empty[Uri]) {
    case (acc, e) => s"""${BuildInfo.base}${e.substring(0, e.lastIndexOf(".json"))}""" :: acc
  }

  override val nestedSuites = schemas.map { schemaUri =>
    val id          = schemaId(schemaUri)
    val validUris   = valid.filter(_.toString.startsWith(s"${BuildInfo.base}/data/$id"))
    val invalidUris = invalid.filter(_.toString.startsWith(s"${BuildInfo.base}/invalid/$id"))
    new SchemaSpec(validator, loader, Uri(BuildInfo.base), schemaUri, validUris, invalidUris)
  }

  private def schemaId(schemaUri: Uri): Path =
    Path(schemaUri.toString().substring(s"${BuildInfo.base}/schemas/".length))
}
