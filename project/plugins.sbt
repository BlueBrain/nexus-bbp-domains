resolvers += Resolver.bintrayRepo("bbp", "nexus-releases")
resolvers += Resolver.bintrayRepo("neuroshapes", "maven")

addSbtPlugin("ch.epfl.bluebrain.nexus" % "sbt-nexus"     % "0.10.13")
addSbtPlugin("com.eed3si9n"            % "sbt-buildinfo" % "0.7.0")
