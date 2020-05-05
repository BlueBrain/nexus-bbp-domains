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

lazy val root = project
  .in(file("."))
  .enablePlugins(ParadoxMaterialThemePlugin, ParadoxSitePlugin, GhpagesPlugin)
  .settings(
    name       := "bbp-schema-docs",
    moduleName := "bbp-schema-docs",
    // paradox settings
    sourceDirectory in Paradox := sourceDirectory.value / "main" / "paradox",
    ParadoxMaterialThemePlugin.paradoxMaterialThemeSettings(Paradox),
    paradoxMaterialTheme in Paradox := {
      ParadoxMaterialTheme()
        .withColor("light-blue", "cyan")
        .withFavicon("./assets/img/favicon-32x32.png")
        .withLogo("./assets/img/logo.png")
        .withCustomStylesheet("./assets/css/docs.css")
        .withRepository(uri("https://github.com/BlueBrain/nexus-bbp-domains"))
        .withSocial(
          uri("https://github.com/BlueBrain"),
          uri("https://gitter.im/INCF/neuroshapes"),
          uri("https://gitter.im/BlueBrain/nexus")
        )
        .withCopyright("""The data models are Open Source and available under the CC-BY-4.0 License.<br/>|""".stripMargin)
    },
    paradoxNavigationDepth in Paradox := 4,
    paradoxProperties in Paradox      += ("github.base_url" -> "https://github.com/BlueBrain/nexus-bbp-domains/tree/master"),
    // gh pages settings
    git.remoteRepo  := "git@github.com:BlueBrain/nexus-bbp-domains.git",
    ghpagesNoJekyll := true,
    ghpagesBranch   := "gh-pages",
  )

addCommandAlias("review", ";clean;paradox")
