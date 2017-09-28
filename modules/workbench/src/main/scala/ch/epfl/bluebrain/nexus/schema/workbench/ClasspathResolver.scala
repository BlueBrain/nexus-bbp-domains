package ch.epfl.bluebrain.nexus.schema.workbench

import java.io.ByteArrayInputStream
import java.util.regex.Pattern

import akka.http.scaladsl.model.Uri
import cats.MonadError
import cats.instances.list._
import cats.syntax.applicativeError._
import cats.syntax.flatMap._
import cats.syntax.functor._
import cats.syntax.traverse._
import ch.epfl.bluebrain.nexus.commons.shacl.validator.ShaclValidatorErr._
import ch.epfl.bluebrain.nexus.commons.shacl.validator.{ImportResolver, ShaclSchema}
import org.apache.jena.rdf.model.{ModelFactory, ResourceFactory}
import org.apache.jena.riot.{Lang, RDFDataMgr}

import scala.collection.JavaConverters._

class ClasspathResolver[F[_]](loader: ResourceLoader[F])
                             (implicit F: MonadError[F, Throwable]) extends ImportResolver[F] {

  private lazy val imports = ResourceFactory.createProperty("http://www.w3.org/2002/07/owl#imports")

  override def apply(schema: ShaclSchema): F[Set[ShaclSchema]] = {
    def loadImports(loaded: Map[String, ShaclSchema], imp: Set[String]): F[Set[ShaclSchema]] = {
      if (imp.isEmpty) F.pure(loaded.values.toSet)
      else {
        val diff = imp.filterNot(i => loaded.contains(i))
        if (diff.isEmpty) F.pure(loaded.values.toSet)
        else {
          for {
            seq <- diff.toList.map(i => load(i).map(sch => (i, sch))).sequence[F, (String, ShaclSchema)]
            sch = seq.map(_._2)
            imp <- importsOfAll(sch)
            res <- loadImports(loaded ++ seq, imp)
          } yield res
        }
      }
    }

    importsOf(schema).flatMap(imps => loadImports(Map.empty, imps)).recoverWith {
      case e: WorkbenchErr.UnableToLoad => F.raiseError(CouldNotFindImports(Set(e.address.toString())))
      case e: WorkbenchErr              => F.raiseError(FailedToLoadShaclSchema(e))
    }
  }

  private def importsOfAll(schemas: List[ShaclSchema]): F[Set[String]] =
    schemas.foldLeft[F[Set[String]]](F.pure(Set.empty[String])) {
      case (acc, elem) =>
        for {
          set <- acc
          imp <- importsOf(elem)
        } yield set ++ imp
    }

  private val prefix = Pattern.quote(loader.baseUri.toString())
  private val any = "[a-zA-Z0-9]+"
  private val num = "[0-9]+"
  private val dot = "\\."
  private val regex = s"^$prefix/schemas/$any/$any/$any/v$num$dot$num$dot$num$$".r

  private def importsOf(schema: ShaclSchema): F[Set[String]] = {
    val model = ModelFactory.createDefaultModel()
    RDFDataMgr.read(model, new ByteArrayInputStream(schema.value.noSpaces.getBytes), Lang.JSONLD)
    val nodes = model.listObjectsOfProperty(imports).asScala.toSet
    val illegalImports = nodes.filter(!_.isURIResource)
    val uris = nodes.filter(_.isURIResource)
    val missingImports = uris.filterNot(n => n.asResource().getURI.matches(regex.regex))
    if (illegalImports.nonEmpty) F.raiseError(IllegalImportDefinition(illegalImports.map(n => n.toString)))
    else if(missingImports.nonEmpty) F.raiseError(CouldNotFindImports(missingImports.map(n => n.toString)))
    else F.pure(nodes.map(_.asResource().getURI))
  }

  private def load(uri: String): F[ShaclSchema] = {
    if (uri.startsWith(loader.baseUri.toString())) {
      loader(Uri(uri)).map(json => ShaclSchema(json))
    } else F.raiseError(CouldNotFindImports(Set(uri)))
  }
}
