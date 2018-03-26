import com.typesafe.sbt.packager.MappingsHelper

val commonsVersion = "0.10.8"
val provVersion    = "0.1.6"
val kgVersion      = "0.9.9"

lazy val prov           = "ch.epfl.bluebrain.nexus" %% "nexus-prov"      % provVersion
lazy val commonsSchemas = "ch.epfl.bluebrain.nexus" %% "commons-schemas" % commonsVersion
lazy val kgSchemas      = "ch.epfl.bluebrain.nexus" %% "kg-schemas"      % kgVersion

lazy val docs = project
  .in(file("docs"))
  .enablePlugins(ParadoxPlugin, UniversalPlugin)
  .settings(
    name                           := "bbp-domains-docs",
    moduleName                     := "bbp-domains-docs",
    paradoxTheme                   := Some(builtinParadoxTheme("generic")),
    target in (Compile, paradox)   := (resourceManaged in Compile).value / "docs",
    topLevelDirectory in Universal := None,
    packageName in Universal       := name.value,
    mappings in Universal          := MappingsHelper.contentOf((paradox in Compile).value)
  )

lazy val core = project
  .in(file("modules/bbp-core"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin, DocumentationPlugin)
  .dependsOn(kgbbpschemas)
  .settings(
    name                := "bbp-core-schemas",
    moduleName          := "bbp-core-schemas",
    libraryDependencies += prov
  )

lazy val kgbbpschemas = project
  .in(file("modules/kg-bbp-schemas"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin, DocumentationPlugin)
  .settings(noPublish)
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
  .settings(
    name       := "bbp-experiment-schemas",
    moduleName := "bbp-experiment-schemas"
  )

lazy val atlas = project
  .in(file("modules/bbp-atlas"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin, DocumentationPlugin)
  .dependsOn(experiment)
  .settings(
    name       := "bbp-atlas-schemas",
    moduleName := "bbp-atlas-schemas"
  )

lazy val electrophysiology = project
  .in(file("modules/bbp-electrophysiology"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin, DocumentationPlugin)
  .dependsOn(experiment)
  .settings(
    name       := "bbp-electrophysiology-schemas",
    moduleName := "bbp-electrophysiology-schemas"
  )

lazy val morphology = project
  .in(file("modules/bbp-morphology"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin, DocumentationPlugin)
  .dependsOn(experiment)
  .settings(
    name       := "bbp-morphology-schemas",
    moduleName := "bbp-morphology-schemas"
  )

lazy val simulation = project
  .in(file("modules/bbp-simulation"))
  .enablePlugins(WorkbenchPlugin)
  .disablePlugins(ScapegoatSbtPlugin, DocumentationPlugin)
  .dependsOn(core)
  .settings(
    name       := "bbp-simulation-schemas",
    moduleName := "bbp-simulation-schemas"
  )

lazy val root = project
  .in(file("."))
  .settings(name := "bbp-schemas", moduleName := "bbp-schemas")
  .settings(noPublish)
  .aggregate(docs, core, experiment, atlas, morphology, electrophysiology, simulation, kgbbpschemas)

lazy val noPublish = Seq(
  publishLocal    := {},
  publish         := {},
  publishArtifact := false
)

inThisBuild(
  Seq(
    resolvers          += Resolver.bintrayRepo("bogdanromanx", "maven"),
    autoScalaLibrary   := false,
    workbenchVersion   := "0.2.2",
    bintrayOmitLicense := true,
    homepage           := Some(url("https://github.com/BlueBrain/nexus-prov")),
    licenses           := Seq("CC-4.0" -> url("https://github.com/BlueBrain/nexus-bpp-domains/blob/master/LICENSE")),
    scmInfo := Some(
      ScmInfo(url("https://github.com/BlueBrain/nexus-prov"),
              "scm:git:git@github.com:BlueBrain/nexus-bbp-domains.git")),
    developers := List(Developer("MFSY", "Mohameth François Sy", "noreply@epfl.ch", url("https://bluebrain.epfl.ch/"))),
    // These are the sbt-release-early settings to configure
    releaseEarlyWith              := BintrayPublisher,
    releaseEarlyNoGpg             := true,
    releaseEarlyEnableSyncToMaven := false
  )
)

addCommandAlias("review", ";clean;test")
