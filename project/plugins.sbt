resolvers += Resolver.bintrayRepo("bbp", "nexus-releases")
resolvers += Resolver.bintrayRepo("neuroshapes", "maven")

addSbtPlugin("ch.epfl.bluebrain.nexus" % "sbt-nexus"     % "0.10.13")
addSbtPlugin("com.eed3si9n"            % "sbt-buildinfo" % "0.7.0")

addSbtPlugin("io.get-coursier"       % "sbt-coursier"               % "1.0.3")
addSbtPlugin("com.geirsson"          % "sbt-scalafmt"               % "1.5.1")
addSbtPlugin("com.typesafe.sbt"      % "sbt-ghpages"                % "0.6.2")
addSbtPlugin("com.lightbend.paradox" % "sbt-paradox"                % "0.4.3")
addSbtPlugin("io.github.jonas"       % "sbt-paradox-material-theme" % "0.5.1")
addSbtPlugin("com.typesafe.sbt"      % "sbt-site"                   % "1.3.2")
