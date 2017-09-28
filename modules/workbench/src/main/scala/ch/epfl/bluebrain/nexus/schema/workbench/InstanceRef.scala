package ch.epfl.bluebrain.nexus.schema.workbench

import akka.http.scaladsl.model.Uri

final case class InstanceRef(base: Uri, uri: Uri) {
  def stripped: String =
    uri.toString().substring(base.toString().length)

  def isIgnored: Boolean =
    uri.toString().endsWith("-ignored")
}