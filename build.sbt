val commonsVersion = "0.5.30"
val provVersion    = "0.1.6"
val kgVersion      = "0.8.8"

lazy val prov           = "ch.epfl.bluebrain.nexus" %% "nexus-prov"      % provVersion
lazy val commonsSchemas = "ch.epfl.bluebrain.nexus" %% "commons-schemas" % commonsVersion
lazy val kgSchemas      = "ch.epfl.bluebrain.nexus" %% "kg-schemas"      % kgVersion

lazy val docs = project
  .in(file("docs"))
  .enablePlugins(DocsPackagingPlugin)
  .settings(common)
  .settings(
    name                  := "bbp-domains-docs",
    moduleName            := "bbp-domains-docs",
    paradoxTheme          := Some(builtinParadoxTheme("generic")),
    packageName in Docker := "bbp-domains-docs"
  )

lazy val core = project
  .in(file("modules/bbp-core"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin, DocumentationPlugin)
  .dependsOn(kgbbpschemas)
  .settings(common)
  .settings(
    name                := "bbp-core-schemas",
    moduleName          := "bbp-core-schemas",
    libraryDependencies += prov
  )

lazy val kgbbpschemas = project
  .in(file("modules/kg-bbp-schemas"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin, DocumentationPlugin)
  .settings(common, noPublish)
  .settings(
    noPublish,
    name       := "kg-bbp-schemas",
    moduleName := "kg-bbp-schemas",
    libraryDependencies ++= Seq(
      commonsSchemas,
      kgSchemas
    )
  )

lazy val experiment = project
  .in(file("modules/bbp-experiment"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin, DocumentationPlugin)
  .dependsOn(core)
  .settings(common)
  .settings(
    name       := "bbp-experiment-schemas",
    moduleName := "bbp-experiment-schemas"
  )

lazy val atlas = project
  .in(file("modules/bbp-atlas"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin, DocumentationPlugin)
  .dependsOn(experiment)
  .settings(common)
  .settings(
    name       := "bbp-atlas-schemas",
    moduleName := "bbp-atlas-schemas"
  )

lazy val electrophysiology = project
  .in(file("modules/bbp-electrophysiology"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin, DocumentationPlugin)
  .dependsOn(experiment)
  .settings(common)
  .settings(
    name       := "bbp-electrophysiology-schemas",
    moduleName := "bbp-electrophysiology-schemas"
  )

lazy val morphology = project
  .in(file("modules/bbp-morphology"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin, DocumentationPlugin)
  .dependsOn(experiment)
  .settings(common)
  .settings(
    name       := "bbp-morphology-schemas",
    moduleName := "bbp-morphology-schemas"
  )

lazy val simulation = project
  .in(file("modules/bbp-simulation"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin, DocumentationPlugin)
  .dependsOn(core)
  .settings(common)
  .settings(
    name       := "bbp-simulation-schemas",
    moduleName := "bbp-simulation-schemas"
  )

lazy val root = project
  .in(file("."))
  .settings(name := "bbp-schemas", moduleName := "bbp-schemas")
  .settings(common, noPublish)
  .aggregate(docs, core, experiment, atlas, morphology, electrophysiology, simulation, kgbbpschemas)

lazy val common = Seq(
  scalacOptions in (Compile, console) ~= (_ filterNot (_ == "-Xfatal-warnings")),
  autoScalaLibrary   := false,
  workbenchVersion   := "0.2.2",
  bintrayOmitLicense := true,
  homepage           := Some(url("https://github.com/BlueBrain/nexus-prov")),
  licenses           := Seq("CC-4.0" -> url("https://github.com/BlueBrain/nexus-prov/blob/master/LICENSE")),
  scmInfo := Some(
    ScmInfo(url("https://github.com/BlueBrain/nexus-prov"), "scm:git:git@github.com:BlueBrain/nexus-prov.git"))
)

lazy val noPublish = Seq(publishLocal := {}, publish := {})

addCommandAlias("review", ";clean;test")
addCommandAlias("rel", ";release with-defaults skip-tests")
