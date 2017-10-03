package ch.epfl.bluebrain.nexus.schema.workbench

import akka.http.scaladsl.model.Uri
import akka.http.scaladsl.model.Uri.Path
import ch.epfl.bluebrain.nexus.common.types.Err
import io.circe.Json

sealed abstract class WorkbenchErr(reason: String) extends Err(reason)

object WorkbenchErr {

  final case class NonAbsoluteUri(uri: Uri) extends WorkbenchErr(s"Cannot load non absolute uri '$uri'.")

  final case class InvalidJson(address: Path)
      extends WorkbenchErr(s"Cannot parse resource '$address' to a json format.")

  final case class UnableToLoad(address: Path)
      extends WorkbenchErr(s"Unable to load resource '$address', validate it exists and that is readable.")

  final case class IllegalResourceAddress(address: Uri, base: Uri)
      extends WorkbenchErr(s"Illegal resource address '$address', must start with '$base'.")

  final case class IllegalContextValue(ctx: Json) extends WorkbenchErr(s"Illegal context definition: '${ctx.spaces2}'")

}
