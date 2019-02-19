/*
scalafmt: {
  style = defaultWithAlign
  maxColumn = 150
  align.tokens = [
    { code = "=>", owner = "Case" }
    { code = "?", owner = "Case" }
    { code = "extends", owner = "Defn.(Class|Trait|Object)" }
    { code = "//", owner = ".*" }
    { code = "{", owner = "Template" }
    { code = "}", owner = "Template" }
    { code = ":=", owner = "Term.ApplyInfix" }
    { code = "++=", owner = "Term.ApplyInfix" }
    { code = "+=", owner = "Term.ApplyInfix" }
    { code = "%", owner = "Term.ApplyInfix" }
    { code = "%%", owner = "Term.ApplyInfix" }
    { code = "%%%", owner = "Term.ApplyInfix" }
    { code = "->", owner = "Term.ApplyInfix" }
    { code = "?", owner = "Term.ApplyInfix" }
    { code = "<-", owner = "Enumerator.Generator" }
    { code = "?", owner = "Enumerator.Generator" }
    { code = "=", owner = "(Enumerator.Val|Defn.(Va(l|r)|Def|Type))" }
  ]
}
 */
val nshVersion = "1.0.3"

lazy val neuroshapes = "ch.epfl.bluebrain.nexus" %% "neuroshapes" % nshVersion

lazy val bbpschemas = project
  .in(file("."))
  .settings(
    name       := "bbp-schemas",
    moduleName := "bbp-schemas",
    resolvers  += Resolver.bintrayRepo("neuroshapes", "maven"),
    resolvers  += Resolver.bintrayRepo("bbp", "nexus-releases"),
    resolvers  += Resolver.bintrayRepo("bogdanromanx", "maven"),
    libraryDependencies ++= Seq(
      neuroshapes
    )
  )

inThisBuild(
  Seq(
    bintrayOmitLicense := true,
    homepage           := Some(url("https://incf.github.io/neuroshapes")),
    licenses           := Seq("Attribution" -> url("https://github.com/BlueBrain/nexus-bbp-domains/blob/master/LICENSE")),
    developers := List(
      Developer("MFSY", "Mohameth François Sy", "noreply@epfl.ch", url("https://incf.github.io/neuroshapes/")),
      Developer("annakristinkaufmann", "Anna-Kristin Kaufmann", "noreply@epfl.ch", url("https://incf.github.io/neuroshapes/")),
      Developer("huanxiang", "Lu Huanxiang", "noreply@epfl.ch", url("https://incf.github.io/neuroshapes/"))
    ),
    scmInfo := Some(ScmInfo(url("https://github.com/BlueBrain/nexus-bbp-domains"), "scm:git:git@github.com:BlueBrain/nexus-bbp-domains.git")),
    // These are the sbt-release-early settings to configure
    releaseEarlyWith              := BintrayPublisher,
    releaseEarlyNoGpg             := true,
    releaseEarlyEnableSyncToMaven := false
  )
)


//from https://stackoverflow.com/questions/31406471/get-resource-file-from-dependency-in-sbt

val copyResourcesFromJar = TaskKey[Unit]("copyResourcesFromJar", "Copy resources from jar dependencies")
copyResourcesFromJar := {
  import scala.io.Source
  import sbt.Keys._

  def copyResourceFromJar(classpathEntry: Attributed[File], jarName: String) = {
    classpathEntry.get(artifact.key) match {
      case Some(entryArtifact) => {
        // searching artifact
        if (entryArtifact.name.startsWith(jarName)) {
          // unpack artifact's jar to tmp directory
          val jarFile = classpathEntry.data
          IO.withTemporaryDirectory { tmpDir =>
            IO.unzip(jarFile, tmpDir)
            // copy to project's target directory
            tmpDir.listFiles.filter(_.isDirectory).toList.map(domainDir => IO.copyDirectory(
              tmpDir / domainDir.name,
              target.value / domainDir.name
            ))
          }
        }
      }
      case _ =>
    }
  }
  for(entry <- (dependencyClasspath in Compile).value) yield {
    copyResourceFromJar(entry, "neuroshapes")
  }
}

lazy val noPublish = Seq(
  publishLocal    := {},
  publish         := {},
  publishArtifact := false
)

addCommandAlias("review", ";clean;test")
