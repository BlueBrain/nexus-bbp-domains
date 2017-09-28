package ch.epfl.bluebrain.nexus.schema.workbench

import ch.epfl.bluebrain.nexus.commons.shacl.validator.{ShaclValidatorErr, ValidationReport}
import io.circe.Json
import org.scalactic.source
import org.scalatest._
import org.scalatest.exceptions.{StackDepthException, TestFailedException}

import scala.util.{Failure, Success, Try}

trait ValidationMatchers extends Matchers { self: WordSpecLike =>

  def validate: AfterWord = afterWord("validate instances")
  def notValidate: AfterWord = afterWord("NOT validate instances")

  implicit def conformantOrNotFromTry(vtry: Try[ValidationReport])(implicit
    pos: source.Position,
    schemaRef: SchemaRef,
    instanceRef: InstanceRef): ConformantOrNot = {
    vtry match {
      case Success(report)            => new ConformantOrNot(report)
      case Failure(e: ShaclValidatorErr.FailedToLoadShaclSchema) =>
        val message = s"Failed to load schema '${schemaRef.stripped}' into the validator"
        throw new TestFailedException((_: exceptions.StackDepthException) => Some(message), Some(e.cause), pos)
      case Failure(th)                =>
        val message = "Unexpected failure of the Shacl validator"
        throw new TestFailedException((_: exceptions.StackDepthException) => Some(message), Some(th), pos)
    }
  }

  class ConformantOrNot(report: ValidationReport)(implicit pos: source.Position, schemaRef: SchemaRef, instanceRef: InstanceRef) {
    def shouldConform: Assertion = {
      if (report.conforms) Succeeded
      else {
        val violations = "  - " + report.result.map(_.reason).mkString("\n  - ")
        val message =
          s"""
             |Instance '${instanceRef.stripped}' did not conform to schema '${schemaRef.stripped}'
             |Violations:
             |$violations
           """.stripMargin
        throw new TestFailedException((_: exceptions.StackDepthException) => Some(message), None, pos)
      }
    }

    def shouldNotConform: Assertion = {
      if (report.conforms) {
        val message = s"Instance '${instanceRef.stripped}' conformed to schema '${schemaRef.stripped}'"
        throw new TestFailedException((_: exceptions.StackDepthException) => Some(message), None, pos)
      }
      else Succeeded
    }
  }

  implicit def loadedOrNotFromTry(ltry: Try[Json])(implicit pos: source.Position): LoadedOrNot =
    new LoadedOrNot(ltry)

  class LoadedOrNot(ltry: Try[Json])(implicit pos: source.Position) {
    def value: Json = ltry match {
      case Success(json)                => json
      case Failure(wbe: WorkbenchErr) =>
        val message = wbe.message
        throw new TestFailedException((_: exceptions.StackDepthException) => Some(message), Some(wbe), pos)
      case Failure(th) =>
        val message = "Resource loading failed unexpectedly"
        throw new TestFailedException((_: StackDepthException) => Some(message), Some(th), pos)
    }
  }

}
