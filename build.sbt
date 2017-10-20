lazy val nexusProv = "ch.epfl.bluebrain.nexus" %% "nexus-prov" % "0.1.1"

lazy val docs = project
  .in(file("docs"))
  .enablePlugins(DocsPackagingPlugin)
  .settings(common)
  .settings(
    name := "bbp-domains-docs",
    moduleName := "bbp-domains-docs",
    paradoxTheme := Some(builtinParadoxTheme("generic")),
    packageName in Docker := "bbp-domains-docs"
  )

lazy val core = project
  .in(file("modules/bbp-core"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin)
  .dependsOn(kgschemas)
  .settings(
    common,
    name := "bbp-core-schemas",
    moduleName := "bbp-core-schemas",
    libraryDependencies += nexusProv
  )

lazy val kgschemas = project
  .in(file("modules/kg-schemas"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin)
  .settings(
    common,
    noPublish,
    name := "kg-schemas",
    moduleName := "kg-schemas"
  )

lazy val experiment = project
  .in(file("modules/bbp-experiment"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin)
  .dependsOn(core)
  .settings(
    common,
    name := "bbp-experiment-schemas",
    moduleName := "bbp-experiment-schemas"
  )

lazy val atlas = project
  .in(file("modules/bbp-atlas"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin)
  .dependsOn(experiment)
  .settings(
    common,
    name := "bbp-atlas-schemas",
    moduleName := "bbp-atlas-schemas"
  )

lazy val electrophysiology = project
  .in(file("modules/bbp-electrophysiology"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin)
  .dependsOn(experiment)
  .settings(
    common,
    name := "bbp-electrophysiology-schemas",
    moduleName := "bbp-electrophysiology-schemas"
  )

lazy val morphology = project
  .in(file("modules/bbp-morphology"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin)
  .dependsOn(experiment)
  .settings(
    common,
    name := "bbp-morphology-schemas",
    moduleName := "bbp-morphology-schemas"
  )

lazy val root = project
  .in(file("."))
  .settings(name := "bbp-schemas", moduleName := "bbp-schemas")
  .settings(common, noPublish)
  .aggregate(docs, core, experiment, atlas, electrophysiology)

lazy val common = Seq(
  scalacOptions in (Compile, console) ~= (_ filterNot (_ == "-Xfatal-warnings")),
  resolvers += Resolver.bintrayRepo("bogdanromanx", "maven"),
  autoScalaLibrary := false,
  workbenchVersion := "0.2.0"
)

lazy val noPublish = Seq(publishLocal := {}, publish := {})

addCommandAlias("review", ";clean;test")
addCommandAlias("rel", ";release with-defaults skip-tests")
