package ch.epfl.bluebrain.nexus.schema.workbench

import java.util.regex.Pattern

import akka.http.scaladsl.model.Uri
import akka.http.scaladsl.model.Uri.Path
import cats.MonadError
import cats.instances.list._
import cats.syntax.flatMap._
import cats.syntax.functor._
import cats.syntax.traverse._
import ch.epfl.bluebrain.nexus.schema.workbench.WorkbenchErr._
import io.circe.parser._
import io.circe.{Json, ParsingFailure}

import scala.annotation.tailrec
import scala.io.Source
import scala.util.control.NonFatal
import scala.util.{Failure, Success, Try}

class ResourceLoader[F[_]](base: Uri, replacements: Map[String, String])(implicit F: MonadError[F, Throwable]) {
  require(base.isAbsolute, "The resource loader requires an absolute 'base' uri.")

  def apply(resource: Uri): F[Json] =
    if (!resource.isAbsolute) F.raiseError(NonAbsoluteUri(resource))
    else load(resource)

  final val baseUri: Uri = base.copy(path = stripTrailingSlashes(base.path))

  private val (baseAsString, length) = {
    val str = baseUri.toString()
    (str, str.length)
  }

  private def resolve(resource: Uri): F[Path] = {
    val str = resource.toString()
    if (!str.startsWith(baseAsString)) F.raiseError(IllegalResourceAddress(resource, base))
    else {
      val remainder = str.substring(length)
      Try(Path(s"$remainder.json")) match {
        case Failure(NonFatal(_)) => F.raiseError(IllegalResourceAddress(resource, base))
        case Success(path)        => F.pure(path)
      }
    }
  }

  private def load(resource: Uri): F[Json] = {
    resolve(resource).flatMap { address =>
      val replaced = Try {
        val asString = Source.fromInputStream(getClass.getResourceAsStream(address.toString())).mkString
        replacements.foldLeft(asString) {
          case (acc, (token, replacement)) =>
            acc.replaceAll(Pattern.quote(token), replacement)
        }
      }.toEither
      replaced.flatMap(str => parse(str)) match {
        case Left(_: ParsingFailure) => F.raiseError(InvalidJson(address))
        case Left(NonFatal(_))       => F.raiseError(UnableToLoad(address))
        case Right(json)             => loadContext(json)
      }
    }
  }

  private def loadContext(json: Json): F[Json] = {
    def handleContextObj(ctx: Json): F[Json] = {
      (ctx.asString, ctx.asObject, ctx.asArray) match {
        case (Some(str), _, _) => load(Uri(str))
        case (_, Some(_), _)   => F.pure(ctx)
        case (_, _, Some(arr)) =>
          arr.toList
            .map(v => handleContextObj(v))
            .sequence
            .map { list =>
              list.foldLeft(Json.obj()) {
                case (acc, el) => acc.deepMerge(el)
              }
            }
        case _                 => F.raiseError(IllegalContextValue(ctx))
      }
    }

    val loaded = for {
      obj <- json.asObject
      ctx <- obj("@context")
    } yield handleContextObj(ctx)

    loaded
      .map(_.map(ctx => json.deepMerge(Json.obj("@context" -> ctx))))
      .getOrElse(F.pure(json))
  }

  private def stripTrailingSlashes(path: Path): Path = {
    @tailrec
    def strip(p: Path): Path = p match {
      case Path.Empty       => Path.Empty
      case Path.Slash(rest) => strip(rest)
      case other            => other
    }

    strip(path.reverse).reverse
  }
}
