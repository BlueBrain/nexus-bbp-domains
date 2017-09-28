package ch.epfl.bluebrain.nexus.schema.workbench

import akka.http.scaladsl.model.Uri

final case class SchemaRef(base: Uri, uri: Uri) {
  def stripped: String =
    uri.toString().substring(s"$base/schemas/".length)
}
