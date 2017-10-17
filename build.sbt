lazy val commonsVersion = "0.4.5"
lazy val scalaTestVersion = "3.0.4"
lazy val akkaHttpVersion = "10.0.10"
lazy val nexusProvVersion = "0.1.0"


lazy val shaclValidator = "ch.epfl.bluebrain.nexus" %% "shacl-validator" % commonsVersion
lazy val akkaHttpCore = "com.typesafe.akka" %% "akka-http-core" % akkaHttpVersion
lazy val scalaTest = "org.scalatest" %% "scalatest" % scalaTestVersion
lazy val nexusProv = "ch.epfl.bluebrain.nexus" %% "nexus-prov" % nexusProvVersion


val baseUri = "http://localhost/v0"

lazy val docs = project
  .in(file("docs"))
  .enablePlugins(DocsPackagingPlugin)
  .settings(common)
  .settings(name := "bbp-domains-docs",
    moduleName := "bbp-domains-docs",
    paradoxTheme := Some(builtinParadoxTheme("generic")),
    packageName in Docker := "bbp-domains-docs")

lazy val workbench = project
  .in(file("modules/workbench"))
  .settings(common, noPublish)
  .settings(name := "bbp-schemas-workbench",
    moduleName := "bbp-schemas-workbench",
    libraryDependencies ++= Seq(shaclValidator, akkaHttpCore, scalaTest))

lazy val core = project
  .in(file("modules/bbp-core"))
  .enablePlugins(BuildInfoPlugin)
  .dependsOn(kgschemas, workbench % Test)
  .settings(common, buildInfoSettings)
  .settings(
    name := "bbp-core-schemas",
    moduleName := "bbp-core-schemas",
    libraryDependencies ++= Seq(
      nexusProv,
      scalaTest % Test
    ),
    buildInfoPackage := "ch.epfl.bluebrain.nexus.bbp.domains.core"
  )


lazy val kgschemas = project.in(file("modules/kg-schemas"))
  .enablePlugins(BuildInfoPlugin)
  .dependsOn(workbench % Test)
  .settings(common, noPublish)
  .settings(
    name := "kg-schemas",
    moduleName := "kg-schemas",
    libraryDependencies ++= Seq(
      "org.scalatest" %% "scalatest" % scalaTestVersion % Test))


lazy val experiment = project
  .in(file("modules/bbp-experiment"))
  .enablePlugins(BuildInfoPlugin)
  .dependsOn(core, workbench % Test)
  .settings(common, buildInfoSettings)
  .settings(
    name := "bbp-experiment-schemas",
    moduleName := "bbp-experiment-schemas",
    libraryDependencies ++= Seq(scalaTest % Test),
    buildInfoPackage := "ch.epfl.bluebrain.nexus.bbp.domains.experiment"
  )

lazy val atlas = project
  .in(file("modules/bbp-atlas"))
  .enablePlugins(BuildInfoPlugin)
  .dependsOn(experiment, workbench % Test)
  .dependsOn(workbench % Test)
  .settings(common, buildInfoSettings)
  .settings(
    name := "bbp-atlas-schemas",
    moduleName := "bbp-atlas-schemas",
    libraryDependencies ++= Seq(scalaTest % Test),
    buildInfoPackage := "ch.epfl.bluebrain.nexus.bbp.domains.atlas"
  )

lazy val electrophysiology = project
  .in(file("modules/bbp-electrophysiology"))
  .enablePlugins(BuildInfoPlugin)
  .dependsOn(experiment, workbench % Test)
  .dependsOn(workbench % Test)
  .settings(common, buildInfoSettings)
  .settings(
    name := "bbp-electrophysiology-schemas",
    moduleName := "bbp-electrophysiology-schemas",
    libraryDependencies ++= Seq(scalaTest % Test),
    buildInfoPackage := "ch.epfl.bluebrain.nexus.bbp.domains.electrophysiology"
  )

lazy val morphology = project
  .in(file("modules/bbp-morphology"))
  .enablePlugins(BuildInfoPlugin)
  .dependsOn(experiment, workbench % Test)
  .dependsOn(workbench % Test)
  .settings(common, buildInfoSettings)
  .settings(
    name := "bbp-morphology-schemas",
    moduleName := "bbp-morphology-schemas",
    libraryDependencies ++= Seq(scalaTest % Test),
    buildInfoPackage := "ch.epfl.bluebrain.nexus.bbp.domains.morphology"
  )
  
lazy val root = project
  .in(file("."))
  .settings(name := "bbp-schemas", moduleName := "bbp-schemas")
  .settings(common, noPublish)
  .aggregate(docs, workbench, core, experiment, atlas, electrophysiology)

lazy val buildInfoSettings = Seq(
  buildInfoKeys := Seq[BuildInfoKey](
    BuildInfoKey("base" -> baseUri),
    BuildInfoKey.map(resources.in(Compile)) {
      case (_, v) =>
        val resourceBase = resourceDirectory.in(Compile).value.getAbsolutePath
        val dirsWithJson = (v * "schemas" ** "*.json").get
        val schemas = dirsWithJson.map(_.getAbsolutePath.substring(resourceBase.length))
        "schemas" -> schemas
    },
    BuildInfoKey.map(resources.in(Compile)) {
      case (_, v) =>
        val resourceBase = resourceDirectory.in(Compile).value.getAbsolutePath
        val dirsWithJson = (v * "contexts" ** "*.json").get
        val contexts = dirsWithJson.map(_.getAbsolutePath.substring(resourceBase.length))
        "contexts" -> contexts
    },
    BuildInfoKey.map(resources.in(Test)) {
      case (_, v) =>
        val resourceBase = resourceDirectory.in(Test).value.getAbsolutePath
        val dirsWithJson = (v * "data" ** "*.json").get
        val data = dirsWithJson.map(_.getAbsolutePath.substring(resourceBase.length))
        "data" -> data
    },
    BuildInfoKey.map(resources.in(Test)) {
      case (_, v) =>
        val resourceBase = resourceDirectory.in(Test).value.getAbsolutePath
        val dirsWithJson = (v * "invalid" ** "*.json").get
        val invalid = dirsWithJson.map(_.getAbsolutePath.substring(resourceBase.length))
        "invalid" -> invalid
    }
  ))

lazy val common = Seq(scalacOptions in(Compile, console) ~= (_ filterNot (_ == "-Xfatal-warnings")),
  resolvers += Resolver.bintrayRepo("bogdanromanx", "maven"))

lazy val noPublish = Seq(publishLocal := {}, publish := {})

addCommandAlias("review", ";clean;test")
addCommandAlias("rel", ";release with-defaults skip-tests")
